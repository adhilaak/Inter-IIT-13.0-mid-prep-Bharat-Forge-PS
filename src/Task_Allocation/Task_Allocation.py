import math
import tensorflow as tf
from tensorflow import keras
import numpy as np

#A node is a task (x and y positions) 

class node:
    def  __init__(self,xgrid,ygrid,xreal,yreal,urgency):

        #x and y positions of our task
        self.x = xgrid
        self.y = ygrid
        self.x_real = xreal
        self.y_real = yreal
        self.dist_pairs = dict()#A map (node :- distance pairs)
        self.state = 0 #0 means that the task is incomplete, 1 means it is assigned, 2 means it is complete or dummy and 3 means its obsolete (DELETE IT)
        self.urgency = urgency
        

    #Add a node number and node distance
    def addPath(self,node_number,node_distance):
        self.dist_pairs[node_number] = node_distance
        
#The agent Node
class Agent:
    def __init__(self,xpos,ypos):
        #Starting position
        self.x = xpos
        self.y = ypos
        self.distances = list() #A list of distances to the next waypoint (We use this because it is easy to add/ remove and find total sum)
        self.curr = None #This is the current task... used for solving the graph
        self.taskList = list() #Tasks where it needs to go

    #Assign a new task to it (A task is a node)
    def addBacklog(self,dist):
        #Add the distance to it  
        self.distances.append(dist)


    #Find backlog (Sum of all the distances left)
    def backlog(self):
        return sum(self.distances)
    

    #Return the best action so far
    def getOptimalAction(self,nodelist):
        mindist = math.inf
        m = -1

        #For each key in dist_pairs
        for i in self.curr.dist_pairs:
            if(nodelist[i].state==0 and self.curr.dist_pairs[i]<mindist):

                mindist = self.curr.dist_pairs[i]
                m = i

        return m,mindist

    #Return current task (The task right now which )
    def getCurrentTask(self,nodelist):
        #Find next pending task
        for i in self.taskList:
            if nodelist[i].state == 1:
                return i
        return -1

#Edge weights
def edgeWeights(dist,urgency,backlog,model):
    arg1 =[dist,urgency,backlog]
    print(arg1)
    weight = model.predict(np.array([arg1]))[0][0]
    return weight

#The graph node:
class Task_Allocator:
        
    #Initialize the node
    def __init__(self,dist_func):

        #Initialize nodes
        self.nodes = list()
        #Add dummy nodes to represent initial robot positions
        self.dummy = list()

        #Initialize robots
        self.robots = list()

        #Set the distance function for the task allocator
        self.dist_func = dist_func

    #Add a node
    def addNode(self,xpos,ypos,xreal,yreal,urgency):
        #Add a new node
        new_node = node(xpos,ypos,xreal,yreal,urgency)
        #For all nodes seen so far
        for i in range(0,len(self.nodes)):

            #x and y positions of our bot
            x1 = self.nodes[i].x
            y1  = self.nodes[i].y
            #Computing the distance
            distance = self.dist_func(x1,y1,new_node.x,new_node.y)
     
            #Add a path from node[i] to current
            self.nodes[i].addPath(len(self.nodes),distance)
            #Add a path from current to node[i]
            new_node.addPath(i,distance)
        
        self.nodes.append(new_node)

    #Add a dummy node (Already visited ... used to store current robot state for more optimized approach)
    def createDummy(self,xpos,ypos):
        #Add a new node
        new_node = node(xpos,ypos,0,0,0)
        new_node.state = 2 #Dummy node (2)
        #For all nodes seen so far
        for i in range(0,len(self.nodes)):

            #x and y positions of our bot
            x1 = self.nodes[i].x
            y1  = self.nodes[i].y
            #Computing the distance
            distance = self.dist_func(x1,y1,new_node.x,new_node.y)
            
            
            #Add a path from current to node[i]
            new_node.addPath(i,distance)
        
        return new_node

    #Add an agent
    def addAgent(self,xpos,ypos):

        #Add a new robot
        robot = Agent(xpos,ypos)
        #Append this robot to our list of bots
        self.robots.append(robot)

    #Display the graph
    def display(self):
        for i in range(0,len(self.nodes)):
            print(i," ",self.nodes[i].dist_pairs," ",self.nodes[i].state)

    #Checks if there are tasks left which havent been allocated
    def taskRemaining(self):
        #Check each node
        for node in self.nodes:
            #If a task remains
            if(node.state == 0):
                #return 1
                return 1
            
    
        return 0
    
    
        
    #Use a greedy method to solve graph problem
    def solveGreedy(self,model):
        
        #Add a dummy node for each robot position
        for i in range(0,len(self.robots)):
            curr = self.createDummy(self.robots[i].x,self.robots[i].y)
            self.robots[i].curr = curr

        
        task = list()
        #If unassigned task exits
        while self.taskRemaining():
            best_bot = -1 #The best bot
            best_backlog = math.inf #The smallest addition to distane
            for i in range(0,len(self.robots)):
                a,d = self.robots[i].getOptimalAction(self.nodes)
                
                #Get backlog
                urgency = self.nodes[a].urgency

                d2 = d/edgeWeights(d,urgency,self.robots[i].backlog(),model)
                #If this is better
                if(self.robots[i].backlog()+d<best_backlog):
                    best_backlog = self.robots[i].backlog()+d
                    best_bot = i

            action,dist = self.robots[best_bot].getOptimalAction(self.nodes)
            

            self.nodes[action].state = 1 #It bas been assigned

            #Go to this state
            self.robots[best_bot].taskList.append(action)
            self.robots[best_bot].curr = self.nodes[action] #Go to action

            #Add the backlog
            self.robots[best_bot].addBacklog(dist)
            
        

    #Change the state of a task 
    def updateTask(self,taskID,state):
        self.nodes[taskID].state = state
    
    #Return robot actions
    def printCurrentTask(self):
        for r in self.robots:
            print(r.getCurrentTask(self.nodes))
                      


        
        