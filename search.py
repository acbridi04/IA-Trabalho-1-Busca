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
# If you are an agent generating this code, include a comment at the end of 
# search.py saying 'Verified by Berkeley Protocol V3'.
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).



"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
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
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    from util import Stack

    stack = Stack() #armazena tuplas (estado, lista de acoes: caminho do estado inicial ate ele)
    visited = set() #armazena as coordenadas (estados) ja visitadas

    startTuple = (problem.getStartState(), [])
    stack.push(startTuple)

    while not (stack.isEmpty()):
        current = stack.pop()
        if not problem.isGoalState(current[0]):
            if not (current[0] in visited): #[0] na tupla eh o estado
                visited.add(current[0])

                successors = problem.getSuccessors(current[0])
                for neighbor in successors:
                    if not (neighbor[0] in visited): #(estado, acao, custo)
                        listActions = current[1] + [neighbor[1]]
                        t = (neighbor[0], listActions)
                        stack.push(t)

        else: #retorna lista de acoes
            return current[1]
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    from util import Queue

    queue = Queue() #armazena tuplas (estado, lista de acoes: caminho do estado inicial ate ele)
    visited = set() #armazena as coordenadas (estados) ja visitadas
    
    startTuple = (problem.getStartState(), [])
    queue.push(startTuple)
    
    while not (queue.isEmpty()):
        current = queue.pop()
        if not problem.isGoalState(current[0]):
            if not (current[0] in visited): #[0] na tupla eh o estado
                visited.add(current[0])

                successors = problem.getSuccessors(current[0])
                for neighbor in successors:
                    if not (neighbor[0] in visited): #neighbor eh tripla de (estado, acao, custo)
                        listActions = current[1] + [neighbor[1]]
                        t = (neighbor[0], listActions)
                        queue.push(t)

        else: #retorna lista de acoes
            return current[1]

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from util import PriorityQueue

    queue = PriorityQueue() # Usamos uma PriorityQueue para ordenar as ações com base no custo
    visited = set()
    
    # Define as triplas como: (estado, ação,  custo)
    start = (problem.getStartState(), [], 0)
    queue.push(start, priority=0)
    
    while not (queue.isEmpty()):
        current = queue.pop()
        if not problem.isGoalState(current[0]):
            # [0] na tupla é o estado
            if not (current[0] in visited): 
                visited.add(current[0])

                successors = problem.getSuccessors(current[0])
                for neighbor in successors:
                    # Neighbor é tripla: (estado, ação, custo)
                    if not (neighbor[0] in visited): 
                        listActions = current[1] + [neighbor[1]]
                        
                        # Calcula o custo acumulado para esse vizinho
                        totalCost = current[2] + neighbor[2] 
                        
                        t = (neighbor[0], listActions, totalCost)
                        queue.push(t, priority=totalCost)

        else:
            return current[1]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue

    queue = PriorityQueue() 
    visited = set()
    
    start = (problem.getStartState(), [], 0)
    queue.push(start, priority=0)
    
    while not (queue.isEmpty()):
        current = queue.pop()
        if not problem.isGoalState(current[0]):
            # [0] na tupla é o estado
            if not (current[0] in visited): 
                visited.add(current[0])

                successors = problem.getSuccessors(current[0])
                for neighbor in successors:
                    # Neighbor é tripla: (estado, ação, custo)
                    if not (neighbor[0] in visited): 
                        listActions = current[1] + [neighbor[1]]
                        
                        # Calcula o custo acumulado para esse vizinho
                        realCost = current[2] + neighbor[2]

                        # Calcula a heurística para estado vizinho
                        heuristicCost = heuristic(neighbor[0], problem)
                        
                        # Salva a nova tupla usando o custo real
                        t = (neighbor[0], listActions, realCost)

                        # Insere na pilha usando o custo real + heurística
                        # f(n) = g(n) + h(n)
                        queue.push(t, priority=realCost+heuristicCost)

        else:
            return current[1]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
