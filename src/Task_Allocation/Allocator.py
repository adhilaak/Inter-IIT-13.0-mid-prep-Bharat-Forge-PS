#! /usr/bin/env python
import rospy
import pygame
from nav_msgs.msg import OccupancyGrid,Odometry,MapMetaData
from geometry_msgs.msg import PoseStamped
from Task_Allocation import *
from Goal_Publisher import *
import tensorflow as tf
from tensorflow import keras
import sys

#0=empty
#1=robot
#2=goal
#-1=unused

model=tf.keras.models.load_model("Model.keras")

#Parameters
obstacletolerance=0.1
unknowntolerance=0.3
step=5
robot_num=4

#Map Data
mapdimensions=[]
worldmap=[]
raw_position = [] #Raw robot positions, need to be converted
position=[]
#Adding goals
goals = []
robot_submitted=[]

#Pygame Parameters
windowwidth=1200
windowheight=600

#Node Name
rospy.init_node('Collector')

'''PATHFINDING DEFINTIONS'''
def pushNeighbors(priorityq,came_from,start,node,target,reached):
    neighborlist=[]
    reached.append(node)
    
    #Try getting neighbors
    try:
        neighbors=[(node[0]-1,node[1]),(node[0],node[1]-1),(node[0],node[1]+1),(node[0]+1,node[1])]
    except:
        print("Cannot acquire neighbors")

    #iterate through neighbors
    for neighbor in neighbors:
        try:
            if(worldmap[neighbor[0]][neighbor[1]]>=0 and neighbor not in reached):
                neighborlist.append({"heuristic":euclid(start,neighbor)+euclid(neighbor,target),"neighbor":neighbor})
                came_from[neighbor]=node
        except Exception as e:
            print(e)
            print("Could not push")
            continue
    
    #sort neighbors
    try:
        sorted(neighborlist,key=lambda k:k["heuristic"])
    except:
        print("Dictionary Sorting Error")

    for i in neighborlist:
        priorityq.append(i['neighbor'])
    
    return
    
def reconstruct(came_from,node):
    path=[node]

    while node in came_from:
        node=came_from[node]
        path.append(node)
    
    path.reverse()
    return path

#A star definition
def aStar(x,y,tx,ty):
    start=(int(x),int(y))
    target=(int(tx),int(ty))

    came_from={}

    path=[]

    priorityq=[]
    priorityq.append(start)
    reached=[]

    while(priorityq):
        node=priorityq.pop(0)
        if(node in reached):
            continue

        if(node==target):
            path=reconstruct(came_from,node)
            break

        pushNeighbors(priorityq,came_from,start,node,target,reached)


    return path

#Gives us the distance
def aStarDist(x,y,tx,ty):
    return len(aStar(x,y,tx,ty))




#The task allocator
ta = Task_Allocator(aStarDist)



def pose4callback(odom):
    if(4 not in robot_submitted):
        robot_submitted.append(4)
        raw_position.append((odom.pose.pose.position,4))
    
def pose3callback(odom):
    if(3 not in robot_submitted):
        robot_submitted.append(3)
        raw_position.append((odom.pose.pose.position,3))

def pose2callback(odom):
    if(2 not in robot_submitted):
        robot_submitted.append(2)
        raw_position.append((odom.pose.pose.position,2))

def pose1callback(odom):
    if(1 not in robot_submitted):
        robot_submitted.append(1)
        raw_position.append((odom.pose.pose.position,1))
#A function to order our raw positions (so that pos1 belongs to robot 1, pos 2 belongs to robot 2 and so on....)
def orderRawPositions(raw):
    #Sort raw position 
    for i in range(0,len(raw)):
        for j in range(i,len(raw)):
            if(raw[i][1]>raw[j][1]):
                temp = raw[i]
                raw[i]= raw[j]
                raw[j] = temp
    
#Convert grid co-ordinates to real co-ordinates
def gridToReal(gridx,gridy,resolution,scale,originx,originy):
    return (gridx*scale*resolution + originx,gridy*scale*resolution + originy)

#Convert real co-ordinates to grid
def realTogrid(x,y,resolution,step,originx,originy):
    gridx = round(int((x-originx)/(resolution*step)))
    gridy = round(int((y-originy)/(resolution*step)))
    return gridx,gridy



#The mapcallback function
def mapcallback(recievedmap):
    
    #Wait for the initial position of 4 robots to come
    while(len(raw_position)!=4):
        print("Waiting for data from all starting robots")
        

    
        
    print("Map recieved")

    #Get map metadatqa
    global resolution
    global origin_x
    global origin_y
    resolution = recievedmap.info.resolution
    origin_x = recievedmap.info.origin.position.x
    origin_y = recievedmap.info.origin.position.x

   
    createMap(recievedmap.data,recievedmap.info.width,recievedmap.info.width)

    #Order raw robot positions
    orderRawPositions(raw_position)        

    for r in raw_position:
        pos = realTogrid(r[0].x,r[0].y,resolution,step,origin_x,origin_y)
        position.append(pos)

    #Adding all the robots
    for p in position:
        print("P ",p)
        ta.addAgent(p[0],p[1])


    #Add each goal node
    for g in goals:
        print("G ",g)
        converted = realTogrid(g[0],g[1],resolution,step,origin_x,origin_y)

        #Grid is stored as row first, column second... Therefore we switch converted for the sake of calculations
        ta.addNode(converted[0],converted[1],g[0],g[1],g[2])

        


    #Start running the main loop
    run_allocator()
    rospy.signal_shutdown("Data recieved")

#Get data from topics
def subscribeData():
    rospy.Subscriber("robot1/odom",Odometry,pose1callback)
    rospy.Subscriber("robot2/odom",Odometry,pose2callback)
    rospy.Subscriber("robot3/odom",Odometry,pose3callback)
    rospy.Subscriber("robot4/odom",Odometry,pose4callback)
    rospy.Subscriber("map",OccupancyGrid,mapcallback)
    rospy.spin()

#Create a map for calculations
def createMap(map,width,height):

    tempmap=[]
    for i in range(0,len(map),width):
        row=[]
        for j in range(0,width):
            row.append(map[i+j])
        tempmap.append(row)
    


    for i in range(0,width,step):
        row=[]
        for j in range(0,height,step):
            unknowncount=0
            emptycount=0
            obstaclecount=0
            for k in range (step):
                for l in range(step):

                    try:
                        pixel=tempmap[j+l][i+k]
                    except:
                        pixel=-1

                    if pixel==-1:
                        unknowncount+=1
                    elif pixel==0:
                        emptycount+=1
                    elif pixel==100:
                        obstaclecount+=1

            if(obstaclecount>obstacletolerance*step*step):
                row.append(-2)
            elif(unknowncount>unknowntolerance*step*step):
                row.append(-1)
            else:
                row.append(0)
        worldmap.append(row)

    global mapdimensions
    mapdimensions=[int(width/step),int(height/step)]
    

def visualiseMap():
    pygame.init()
    window=pygame.display.set_mode((windowwidth,windowheight))
    
    running=True
    
    black=(0,0,0)
    green=(0,255,0)
    red=(255,0,0)
    blue=(0,0,255)
    gray=(100,100,100)
    cyan=(0,255,255)
    white = (255,255,255)

    blockwidth=windowwidth/step
    blockheight=windowheight/step

    for i in range(mapdimensions[0]):
            color=black
            for j in range(mapdimensions[1]):
               
                if(worldmap[i][j]==0):
                    color=white
                elif(worldmap[i][j]==-2):
                    color=gray
                
                

                pygame.draw.rect(window,color,pygame.Rect(i*step,j*step,blockwidth,blockheight))
                
    

    #Draw paths    print(raw_position)
    for r in ta.robots:
        print("ROBOT")
        if(len(r.taskList)>0):
            x = r.x
            y = r.y
            ex = 0
            ey = 0
            for t in r.taskList:
                
                            
                ex = ta.nodes[t].x
                ey = ta.nodes[t].y

                path = aStar(x,y,ex,ey)

                for p in path:
                    if(p not in position and p not in goals):
                        pygame.draw.rect(window,green,pygame.Rect(p[0]*step,p[1]*step,step,step))
                    print("(",p[0],",",p[1],")")
                x = ex
                y = ey 
    #Draw robot nodes and goal nodes
    for r in ta.robots:
        pygame.draw.rect(window,blue,pygame.Rect(r.x*step,r.y*step,step,step))

    for n in ta.nodes:
        pygame.draw.rect(window,red,pygame.Rect(n.x*step,n.y*step,step,step))
    pygame.display.flip()

    
    while(running):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        

def euclid(a=tuple,b=tuple):
    return pow(pow(a[0]-b[0],2)+pow(a[1]-b[1],2),0.5)





def run_allocator():

    #Solve for initial tasks


    ta.solveGreedy(model)
    #We create a global Goal Publisher object to publish instructions to move our robots
    global gp 
    gp = GoalPublisher()
    

    if(len(ta.robots[0].taskList)>0):
        robot_dest = ta.robots[0].taskList[0]
        gridx = ta.nodes[robot_dest].x_real
        gridy = ta.nodes[robot_dest].y_real
        pos = gridToReal(gridx,gridy,resolution,step,origin_x,origin_y)
        print(pos)
        gp.robot1_goal = gp.getPoseStamped(pos[0],pos[1],0)

    if(len(ta.robots[1].taskList)>0):
        robot_dest = ta.robots[1].taskList[0]
        gridx = ta.nodes[robot_dest].x_real
        gridy = ta.nodes[robot_dest].y_real
        pos = gridToReal(gridx,gridy,resolution,step,origin_x,origin_y)
        print(pos)
        gp.robot2_goal = gp.getPoseStamped(pos[0],pos[1],0)

    if(len(ta.robots[2].taskList)>0):
        robot_dest = ta.robots[2].taskList[0]
        gridx = ta.nodes[robot_dest].x_real
        gridy = ta.nodes[robot_dest].y_real
        pos = gridToReal(gridx,gridy,resolution,step,origin_x,origin_y)
        print(pos)
        gp.robot3_goal = gp.getPoseStamped(pos[0],pos[1],0)

    if(len(ta.robots[3].taskList)>0):
        robot_dest = ta.robots[3].taskList[0]
        gridx = ta.nodes[robot_dest].x_real
        gridy = ta.nodes[robot_dest].y_real
        pos = gridToReal(gridx,gridy,resolution,step,origin_x,origin_y)
        print(pos)
        gp.robot4_goal = gp.getPoseStamped(pos[0],pos[1],0)


    rospy.sleep(1.0)
    gp.pub()
    rospy.loginfo("Goal Published!")


    visualiseMap()


#python3 Allocator.py 5.10 2.1 5  -3 7.2 4 -5 8 6 -3 -5 10 -4 -2 1 8 -3 1 8 6 2 5.3 7 2.3 -7 3 2.4 -10 -6 5^

if __name__ == "__main__":
    #Add all the goals with urgencies
    for i in range(1,len(sys.argv)-2,3):
        goals.append((float(sys.argv[i]),float(sys.argv[i+1]),float(sys.argv[i+2])))  
        
    #Start the process
    subscribeData()
