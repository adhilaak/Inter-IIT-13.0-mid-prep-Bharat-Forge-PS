#! /usr/bin/env python
import numpy as np
import rospy
import pygame
import threading
from nav_msgs.msg import OccupancyGrid,Odometry,MapMetaData
from geometry_msgs.msg import PoseStamped
from Task_Allocation import *
from Goal_Publisher import *

#0=empty
#1=robot
#2=goal
#-1=unused

#Parameters
obstacletolerance=0.1
unknowntolerance=0.3
step=8
robot_num=4

#Map Data
mapdimensions=[]
worldmap=[]
raw_position = [] #Raw robot positions, need to be converted
position=[]
#Adding goals
goals = [(22,16),(14,18),(35,12),(30,12),(53,24),(48,20),(43,40)]
robot_submitted=[]

#Pygame Parameters
windowwidth=1000
windowheight=400

#Node Name
rospy.init_node('Collector')


#A star definition
def astar(x,y,tx,ty):
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

        pushneighbors(priorityq,came_from,start,node,target,reached)


    return path

#Gives us the distance
def AstarDist(x,y,tx,ty):
    return len(astar(x,y,tx,ty))

#The task allocator
ta = Task_Allocator(AstarDist)



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
    return (gridx*scale*resolution + origin_x,gridy*scale*resolution + originy)


#The mapcallback function
def mapcallback(recievedmap:OccupancyGrid):
    
    #Wait for the initial position of 4 robots to come
    while(len(raw_position)!=4):
        pass

    if(True):

        
        print("Map recieved")

        #Get map metadatqa
        global resolution
        global origin_x
        global origin_y
        resolution = recievedmap.info.resolution
        origin_x = recievedmap.info.origin.position.x
        origin_y = recievedmap.info.origin.position.x

        print(resolution)
        print(origin_x)
        print(origin_y)
        createmap(recievedmap.data,recievedmap.info.width,recievedmap.info.width)

        #Convert raw robot position
        print(raw_position)
        orderRawPositions(raw_position)        
        print()
        print(raw_position)

        for r in raw_position:
            pos = (int((r[0].x-origin_x)/(resolution*step)),int((r[0].y-origin_y)/(resolution*step)))
            position.append(pos)

        #Adding all the robots
        for p in position:
            ta.addAgent(p[0],p[1])

        #Add each goal node
        for g in goals:
            ta.addNode(g[0],g[1])

        


        #Start control
        control()
        rospy.signal_shutdown("Data recieved")

#Get data from topics
def getdata():
    rospy.Subscriber("robot1/odom",Odometry,pose1callback)
    rospy.Subscriber("robot2/odom",Odometry,pose2callback)
    rospy.Subscriber("robot3/odom",Odometry,pose3callback)
    rospy.Subscriber("robot4/odom",Odometry,pose4callback)
    rospy.Subscriber("map",OccupancyGrid,mapcallback)
    rospy.spin()

#Create a map for calculations
def createmap(map,width,height):

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
    

def visualisemap():
    pygame.init()
    window=pygame.display.set_mode((windowwidth,windowheight))
    running=True
    
    black=(0,0,0)
    green=(0,255,0)
    red=(255,0,0)
    blue=(0,0,255)
    purple=(255,0,255)
    cyan=(0,255,255)

    blockwidth=windowwidth/step
    blockheight=windowheight/step

    for i in range(mapdimensions[0]):
            color=black
            for j in range(mapdimensions[1]):
               
                if(worldmap[i][j]==0):
                    color=green
                elif(worldmap[i][j]==-2):
                    color=red
                
                for g in goals:

                    if i ==g[0] and j == g[1]:
                        color = purple

                for p in position:
                    if i ==p[0] and j == p[1]:
                        color = blue

                pygame.draw.rect(window,color,pygame.Rect(i*step,j*step,blockwidth,blockheight))
                

    #Draw paths
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

                path = astar(x,y,ex,ey)

                for p in path:
                    if(p not in position and p not in goals):
                        pygame.draw.rect(window,cyan,pygame.Rect(p[0]*step,p[1]*step,step,step))
                    print("(",p[0],",",p[1],")")
                x = ex
                y = ey 

    pygame.display.flip()    
    
    while(running):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

def euclid(a=tuple,b=tuple):
    return pow(pow(a[0]-b[0],2)+pow(a[1]-b[1],2),0.5)

def pushneighbors(priorityq,came_from,start,node,target,reached):
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



def control():
    ta.solveGreedy()
    #We create a global Goal Publisher object to publish instructions to move our robots
    global gp 
    gp = GoalPublisher()
    

    if(len(ta.robots[0].taskList)>0):
        robot_dest = ta.robots[0].taskList[0]
        gridx = ta.nodes[robot_dest].x
        gridy = ta.nodes[robot_dest].y
        pos = gridToReal(gridx,gridy,resolution,step,origin_x,origin_y)
        print(pos)
        gp.robot1_goal = gp.getPoseStamped(pos[0],pos[1],0)

    if(len(ta.robots[1].taskList)>0):
        robot_dest = ta.robots[1].taskList[0]
        gridx = ta.nodes[robot_dest].x
        gridy = ta.nodes[robot_dest].y
        pos = gridToReal(gridx,gridy,resolution,step,origin_x,origin_y)
        print(pos)
        gp.robot2_goal = gp.getPoseStamped(pos[0],pos[1],0)

    if(len(ta.robots[2].taskList)>0):
        robot_dest = ta.robots[2].taskList[0]
        gridx = ta.nodes[robot_dest].x
        gridy = ta.nodes[robot_dest].y
        pos = gridToReal(gridx,gridy,resolution,step,origin_x,origin_y)
        print(pos)
        gp.robot3_goal = gp.getPoseStamped(pos[0],pos[1],0)

    if(len(ta.robots[3].taskList)>0):
        robot_dest = ta.robots[3].taskList[0]
        gridx = ta.nodes[robot_dest].x
        gridy = ta.nodes[robot_dest].y
        pos = gridToReal(gridx,gridy,resolution,step,origin_x,origin_y)
        print(pos)
        gp.robot4_goal = gp.getPoseStamped(pos[0],pos[1],0)


    rospy.sleep(1.0)
    gp.pub()
    rospy.loginfo("Goal Published!")


    visualisemap()

if __name__ == "__main__":
    getdata()
    

    

