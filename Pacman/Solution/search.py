# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
  """
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  
  """
  Depth first search (DFS) makes use of stack for implementing itself.
  In this search method, we are pushing the elements on the stack in the order they are received.
  So the vertex that is pushed last onto the stack will be retrieved on subsequent pop operation and will be expanded first.
  This is a bit different from normal implementation in which we expand the node which is visited first.
  We have used visitedList to maintain the track of nodes that have been already visited.
  Another tweak that we did was that we stored the path to current node in the stack along with the node.
  This was to simplify for returning the path value (directions) for pacman
  Without this strategy, we faced problem in removing out the elements that were on stack but not on the path to be returned .
  """
  st = util.Stack()
  pathList = []
  visitedList = []
  st.push((problem.getStartState(), pathList, visitedList))
  
  while st.isEmpty() == False :
      u, path, visited = st.pop()
      visited = visited + [u]
      for v, direction, cost in problem.getSuccessors(u) :
          if problem.isGoalState(v) :
              return path + [direction]
          if v not in visited :
              st.push ((v, path + [direction], visited))
  
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  """
  Breadth first search is implemented using the queue.
  In this search method, we push the nodes onto the queue while expanding.
  The expansion is level wise ie. we first exoand level 1 nodes then 2nd level and so on
  So as per queue FIFO policy, the first element pushed onto queue will be retrieved first.
  We maintain a visited list to check which nodes has been already visited to prevent them putting into queue again.
  """
  
  qu= util.Queue()
  pathList = []
  visited = [problem.getStartState()]
  qu.push((problem.getStartState(), pathList))

  while qu.isEmpty() == False :
      u, path = qu.pop()
      for v, direction, cost in problem.getSuccessors(u) :
          if v not in visited :
              if problem.isGoalState(v) :
                  return path + [direction]
              visited = visited + [v]
              qu.push((v, path + [direction]))
              
  
  util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  """
  Uniform cost search uses a Priority Queue for the implementation.
  We push the nodes onto the priority queue along with the distance from the source. 
  This distance serves as the comparison value for returning from the queue.
  The node with the minimum distance (f(x)) is returned.
   So at iteration, we are expanding the node with the minimum distance among the explored nodes. 
  """
  
  pq = util.PriorityQueue()
  pathList = []
  visited = [problem.getStartState()] 
  pq.push( (problem.getStartState(), pathList ), 0)
  
  while pq.isEmpty() == False :
      u, path = pq.pop()
      visited = visited + [u];
      
      if (problem.isGoalState(u)) :
          return path
      
      for v, direction, cost in problem.getSuccessors(u) :
          if v not in visited :
              visited = visited + [v]
              pq.push( (v, path + [direction]), problem.getCostOfActions(path + [direction]) )
        
  
  
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  
  """ 
  A star search is similar to Uniform Cost search (UCS).
  The only difference between A star and UCS is the heuristic function.
  While pushing the current node in priority queue, we add the cost incurred to reach that point from source and the heuristic value. 
  """
  pq = util.PriorityQueue()
  pathListAstar = []
  visited = []
  pq.push((problem.getStartState(), pathListAstar), heuristic(problem.getStartState(), problem))
  
  while pq.isEmpty() == False :
      u, path = pq.pop()
      visited = visited + [u]
  
      if (problem.isGoalState(u)) :
          return path
      
      for v, direction, cost in problem.getSuccessors(u) :
          if v not in visited :
              visited = visited + [v]
              pq.push( (v, path + [direction]), problem.getCostOfActions(path + [direction]) + heuristic(v, problem) )
  
  
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch