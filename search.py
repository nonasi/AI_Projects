# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
# Add a different
# Add another line

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    #nodes contain the state, the direction we had to take to get to the state 
    #and the cost of taking this particular edge. 
    startStateNode = (problem.getStartState(), "No Direction", 1)
    
    directions, possible_path = recursiveDFS (problem, startStateNode, explored = [problem.getStartState()]) #problem and current state's location

    path = []
    for curDir in directions:
        if curDir is 'South': path.append(s)
        if curDir is 'North': path.append(n)
        if curDir is 'East': path.append(e)
        if curDir is 'West': path.append(w)

    #print "final path returned: ", path
    return  path #[s,s,w,s,w,w,s,w]


# Takes the problem and the current state
# curState[0] = loc
# curState[0] = dir
# curState[0] = score
# dirs = path to the food
# frontier = non explored nodes (the stack) 
# explored = the explored nodes (an array)

# note: we use the boolean in orver to backtrack
def recursiveDFS (problem, curStateNode, dirs = [], explored = [], possible_path = False):
    curState = curStateNode[0]
    curDir = curStateNode[1]
    if problem.isGoalState(curState):
    #add current state to dirs:
        #dirs.append(curDir); #append the direction we had to take
        return dirs, True

    else: #if we are not in a goal state
        #go down the right subtree
        successors = problem.getSuccessors(curState)

        for successorNumber in range(len(successors)):
            if successors[successorNumber][0] not in explored:
                explored.append(successors[successorNumber][0]) #append state
                dirs.append(successors[successorNumber][1]) #append the direction 
                dirs, possible_path = recursiveDFS(problem, successors[successorNumber], dirs, explored, possible_path)
            if possible_path:
                return dirs, True

        dirs.pop()
    return dirs, False

def breadthFirstSearch(problem):
    "Search the shallowest nodes in the search tree first. [p 81]"
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    startState = problem.getStartState()
    #nodes contain the state, the direction we had to take to get to the state 
    #and the cost of taking this particular edge. 
    startStateNode = (problem.getStartState(), "No Direction", 1)  
    if problem.isGoalState(problem.getStartState()):
        return []
    directions, possible_path = BFSHelper (problem, curState=startState, frontier = [startStateNode]) #problem and current state's location
    path = bfsPathHelper(directions)
    return  path #[s,s,w,s,w,w,s,w]


    # Takes the problem and the current state
# curState[0] = loc
# curState[1] = dir
# curState[2] = score
# dirs = path to the food
# frontier = non explored nodes (the stack) 
# explored = the explored nodes (an array)

#curState = state
#frontier = list of stateNodes
#stateNodes = triplet (state, direction, path cost)
#explored = list of tuples: (newState, dir, pathcost), (newState, dir, pathcost)
# note: we use the boolean in orver to backtrack

# recursively find BFS solution
def BFSHelper (problem, curState, frontier, explored = [], possible_path = False):
    #Base case
    while len(frontier) is not 0:
        # frontier is a list of triplets
        parentState = curState
        curStateNode = frontier.pop(0)
        curState = curStateNode[0]

        # successorsTriplets holds a list of triplets
        successorsTriplets = problem.getSuccessors(curState)

        for successorNumber in range(len(successorsTriplets)):
            #i[0][0] is the state 
            if successorsTriplets[successorNumber][0] not in [i[0][0] for i in explored]:
                currentSuccessor = successorsTriplets[successorNumber][0]
                if problem.isGoalState(currentSuccessor):
                    explored.append([successorsTriplets[successorNumber], curState])
                    return explored, True
                else:
                    frontier.append(successorsTriplets[successorNumber])
                    explored.append([successorsTriplets[successorNumber], curState])
    return explored, False

# given a list of triplets with explored states, it extracts the path 
def bfsPathHelper(explored):
    """
    explored is a list of these: [((1,2), "direction", 1), ((1,3), "direction", 1)]
                  which is also: [ child, parent ]
    """
    saveThis = toDir(explored[0][0][1])
    path = []
    pathElement = explored.pop()
    parent = pathElement[0][0]
    while len(explored) is not 0:
        # Add direction to this location to path list
        path.append(toDir(pathElement[0][1]))
        #  save parent location so it can be looked for
        #  similar to a linked list
        parent = pathElement[1]
        while parent is not pathElement[0][0] and len(explored) is not 0:
            pathElement = explored.pop()
    if parent is pathElement[0][0]:
        path.append(toDir(pathElement[0][1]))
    #path.append(saveThis)
    return path[::-1]


#direction is a string with a direction, 
#this method returns n,s,w,e depending on which 
#direction string gets passed in
def toDir(direction):
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH
    if direction is "North":
        return n
    if direction is "South":
        return s
    if direction is "East":
        return e
    if direction is "West":
        return w


# implemented as shown in the book
def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    from game import Directions
    from util import PriorityQueue
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH
    #print "Var s is: ", s
    startState = [(problem.getStartState(), "No Direction", 0), 0]
    if problem.isGoalState(problem.getStartState()):
        return []
    # initialize frontier as PriorityQueue( (stateTriple), locationUnitCost )
    startFrontier = PriorityQueue()
    startFrontier.push(startState, startState[0][2])
    directions, possible_path = UCSHelper (problem, curState=startState, frontier = startFrontier)
    if not possible_path: print "COULDN'T FIND ANYTHING"
    path = ucsPathHelper(directions)
    return  path #[s,s,w,s,w,w,s,w]


    # Takes the problem and the current state
# curState[0] = loc
# curState[0] = dir
# curState[0] = score
# dirs = path to the food
# frontier = non explored nodes (the stack) 
# explored = the explored nodes (an array) 

# note: we use the boolean in orver to backtrack
def UCSHelper (problem, curState, frontier, explored = [], possible_path = False):
    print "Is (1,1) the goal state ", problem.isGoalState((1,1))
    print "just came in to UCSHelper"
    print "curState inside BFS: ", curState

    #Base case
    while not frontier.isEmpty():

        # frontier is a PriorityQueue
        # parentState = curState

        curState = frontier.pop()
        oldCost = curState[1]

        successors = problem.getSuccessors(curState[0][0])

        for successorNumber in range(len(successors)):
            if successors[successorNumber][0] not in [i[0][0] for i in explored]:
                if problem.isGoalState(successors[successorNumber][0]):
                    explored.append([successors[successorNumber], curState[0]])
                    return explored, True
                else:
                    thisCost = successors[successorNumber][2]
                    totalCost = thisCost + oldCost
                    newTuple = (successors[successorNumber][0], successors[successorNumber][1], totalCost)
                    frontier.push([newTuple, totalCost], totalCost)
                    explored.append([newTuple, curState[0]])

    # else no solution found
    return explored, False

def ucsPathHelper(explored):
    """
    explored is a list of these: [((1,2), "direction", 1), ((1,3), "direction", 1)]
                  which is also: [ child, parent ]
    """
    saveThis = toDir(explored[0][0][1])
    path = []
    pathElement = explored.pop()
    while len(explored) is not 0:
        # Add direction to this location to path list
        path.append(toDir(pathElement[0][1]))

        # save parent location so it can be looked for
        #  similar to a linked list
        parent = pathElement[1]
        if len(explored) is not 0: pathElement = explored.pop()
        while parent is not pathElement[0] and len(explored) is not 0:
            pathElement = explored.pop()
            if len(explored) is 0 and parent is pathElement[0]:
                path.append(toDir(pathElement[0][1]))
    return path[::-1]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"    # util.raiseNotDefined()
    
    """
   Definitions:
   state = ( (x,y), "dir", pathCost )
   stateNode = (state, g(n))
   frontierNode = (stateNode, f(n))
   explored = [ childStateNode, parentStateNode ]
   also += means append
   """
    from game import Directions
    from util import PriorityQueue
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    initialState = (problem.getStartState(), "No Direction", 0)
    initialStateNode = (initialState, 0) #state, g(n)
    #state node, f(n)
    frontier = PriorityQueue()
    frontier.push(initialStateNode, heuristic(problem.getStartState(),problem))
    # list of tuples. Each tuple is of the form [curStateNode, parentStateNode]
    explored = []
    explored.append([initialStateNode, initialStateNode])
    if problem.isGoalState(problem.getStartState()):
        return []
    
    #path = the path
    #foundSol = true if path found; false if no path found
    path, foundSol= aStarHelper(problem=problem, curStateNode=initialStateNode,frontier=frontier,heuristic=heuristic, explored = explored)

    path = aStarPathHelper(path)
    print "returning processed path: ", path
    return  path #[s,s,w,s,w,w,s,w]

#curStateNode = a friontierNode
#frontier = priority queue ordered by f(n)
#heuristic = 
def aStarHelper(problem, curStateNode, frontier, heuristic, explored):
    while not frontier.isEmpty():
        curStateNode = frontier.pop()
        curStateGn = curStateNode[1]
        curStateCoords = curStateNode[0][0] #(x,y)
        
        #list of successors states (not nodes) of current state
        successors = problem.getSuccessors(curStateCoords)
        
        for successorIndex in range(len(successors)):
            thisSuccessor = successors[successorIndex]
            #sucessorIndex's g(n) = parent's g(n) + cost of going from parent to this sucessorIndex
            successorGn = curStateGn + thisSuccessor[2] 
            successorFn = successorGn + heuristic(curStateCoords, problem)

            #if this (x, y ) has already been explored
            i = 0
            while i < len(explored) - 1 and thisSuccessor[0] != explored[i][0][0][0] :
                i += 1
            if thisSuccessor[0] == explored[i][0][0][0]:
                #oldFn = Fn of node in explored
                oldFn = explored[i][0][1] + heuristic(explored[i][0][0][0], problem)
                #oldFN = FN of node in explored
                if oldFn > successorFn:
                   
                   # in explored, change the first element of the given tuple to be thisSuccessor
                   toAppend = [(thisSuccessor, successorGn), curStateNode]
                   explored.append(toAppend)
                else: continue # Required to go to next successor in for-loop
               
            else:
                successorNode = (thisSuccessor, successorGn)
                explored.append([successorNode, curStateNode])
                frontier.push(successorNode, successorFn)

                if problem.isGoalState(successorNode[0][0]) :
                    return explored, True

        

def aStarPathHelper(explored):
    """
    explored is a list of these: [((1,2), "direction", 1), ((1,3), "direction", 1)]
                  which is also: [ child, parent ]
    """
    saveThis = toDir(explored[0][0][0][1]) #dir
    path = []
    pathElement = explored.pop() #[stateNodeChild, stateNodeParent]
    
    while len(explored) is not 0:
        # Add direction to this location to path list
        path.append(toDir(pathElement[0][0][1])) #dir
        # save parent location so it can be looked for
        #  similar to a linked list
        parent = pathElement[1][0] #state
        
        if len(explored) is not 0: pathElement = explored.pop()
        
        while parent != pathElement[0][0] and len(explored) is not 0:
            pathElement = explored.pop()
            if len(explored) is 0 and parent is pathElement[0][0]:
                path.append(toDir(pathElement[0][0][1]))

    if None in path:
        path.remove(None)
    return path[::-1]

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch