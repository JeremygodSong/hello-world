# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import cgi, html
cgi.escape = html.escape

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    mystack = util.Stack()
    startNode = (problem.getStartState(), '', 0, [])
    mystack.push(startNode)
    visited = set()
    while mystack :
        node = mystack.pop()
        state, action, cost, path = node
        if state not in visited :
            visited.add(state)
            if problem.isGoalState(state) :
                path = path + [(state, action)]
                break;
            succNodes = problem.expand(state)
            for succNode in succNodes :
                succState, succAction, succCost = succNode
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                mystack.push(newNode)
    actions = [action[1] for action in path]
    del actions[0]
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    #COMP90054 Task 1, Implement your A Star search algorithm here
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    PriorityQ = util.PriorityQueue()
    PriorityQ.push((problem.getStartState(), '', 0, []), 0+heuristic(problem.getStartState(), problem))  
                      #current State,   action, cost, path->action list
    visited = []
    best_g = {}      
    while PriorityQ:
        node = PriorityQ.pop()
        Current_State, action, cost, path = node
        gcost = problem.getActionCost
        if Current_State not in visited or cost < best_g[Current_State]:
            visited.append(Current_State)
            best_g[Current_State] = cost
            if problem.isGoalState(Current_State):
                path = path + [action]
                break;
            succNodes = problem.expand(Current_State)
            for succState, action1, cost1 in succNodes:
                newActions = path + [action]
                newCost = cost + cost1
                if succState not in visited:
                    search_node = (succState, action1, newCost, newActions)
                    PriorityQ.push(search_node, newCost+heuristic(succState, problem))
    actions = path
    del actions[0]
    return actions

        
def recursivebfs(problem, heuristic=nullHeuristic) :
    #COMP90054 Task 2, Implement your Recursive Best First Search algorithm here
    "*** YOUR CODE HERE ***"
    def RBFS(problem, node, f_limit):
        state, action, cost, path, f = node 
        if problem.isGoalState(state):
            return path, 0
        expanded_tuples = problem.expand(state)
        successors = []
        for nextState, action1, cost1 in expanded_tuples:
            newActions = path + [action1]
            newCost = cost + cost1
            CHILD_NODE = [nextState, action1, newCost, newActions, f] 
            successors.append(CHILD_NODE)            
        if len(successors) == 0:
            return None, float('inf')
        for s in successors:
            state_s, action_s, cost_s, path_s, f = s
            s[4] = max(cost_s + heuristic(state_s, problem), s[4])
           
            #loop
        while True:
            successors.sort(key=lambda x: x[4])
            best = successors[0]
            if best[4] > f_limit:
                return None, best[4]
            if len(successors) > 1:
                alternative = successors[1][4]
            else:
                alternative = float('inf')
            result, best[4] = RBFS(problem, best, min(f_limit, alternative))
            if result is not None:
                return result, best[4]
            
    node = [problem.getStartState(), '', 0, [], 0+heuristic(problem.getStartState(), problem)]
    result, bestf = RBFS(problem, node, float('inf'))
    return result

    
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
rebfs = recursivebfs

