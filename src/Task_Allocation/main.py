#We are trying it out here
from Task_Allocation import *
#Make better using a better distance estimation function
def estimate_distace(x1,y1,x2,y2):
    return (math.sqrt((x1-x2)**2 + (y1-y2)**2))

if __name__ == "__main__":
   
    g = Task_Allocator(estimate_distace)
    g.addNode(0,0)
    g.addNode(10,10)
    g.addNode(20,30)
    g.addNode(50,30)
    g.addNode(51,30)

    g.addAgent(0,0)
    g.addAgent(40,40)

    g.display()
    print()

    g.solveGreedy()

    print()
    g.addNode(70,80)
    g.solveGreedy()
    print()
    g.printCurrentTask()
 
    g.updateTask(0,2)
    g.updateTask(3,2)
    g.printCurrentTask()

