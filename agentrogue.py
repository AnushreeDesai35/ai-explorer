from agent import BaseAgent
from heapq import *
import random
import time
import sys

class Node:
    """
    Node object for bookeeping of the current state, parent node for backtracking,
    action performed to generate the node, actual cost and estimated cost.
    """
    def __init__(self, estimateCost, actualCost, state, parent, action):
        """
        Constructor
        """
        self.estimateCost = estimateCost
        self.actualCost = actualCost
        self.state = state
        self.parent = parent
        self.action = action

    def __eq__(self, other):
        """
        Equal operator overload for membership testing of states in heapq
        and replace the node having state with higher estimated cost if
        node already present.
        """
        if other:
            if self.state == other.state:
                return True

    def __lt__(self, other):
        """
        Less than operator overload to compare estimated costs for heapify
        comparisions in heapq, using the priority as estimated cost.
        """
        return self.estimateCost < other.estimateCost

    def __str__(self):
        return str(self.state)

class AgentRogue(BaseAgent):
    def __init__(self, height, width, initial_strength, name='agent_rogue'):
        super().__init__(height=height, width=width,
                            initial_strength=initial_strength, name=name)
    
    problemPathCost = {'p': 10, 's': 30, 'm': 100, 'w': 1000, 'u': -300}

    def neighbours(self, state, size):
        # topleft
        # if(state[0] > 0 and state[1] > 0):
        #     yield (state[0] - 1, state[1] - 1)
        # else:
        #     yield None
        # top
        if state[0] > 0:
            yield (state[0] - 1, state[1])
        else:
            yield None
        # topright
        # if state[0] > 0 and state[1] < size:
        #     yield (state[0] - 1, state[1] + 1)
        # else:
        #     yield None
        # right
        if state[1] < size:
            yield (state[0], state[1] + 1)
        else:
            yield None
        # bottomright
        # if state[0] < size and state[1] > size:
        #     yield (state[0] + 1, state[1] + 1)
        # else:
        #     yield None
        # bottom
        if state[0] < size:
            yield (state[0] + 1, state[1])
        else:
            yield None
        # bottomleft
        # if state[0] < size and state[1] > 0:
        #     yield (state[0] + 1, state[1] - 1)
        # else:
        #     yield None
        # left
        if state[1] > 0:
            yield (state[0], state[1] - 1)
        else:
            yield None

def evaluateHeuristic(self, problem, state):
    value = self.problemPathCost[problem[state[0]][state[1]]]
    for neighbour in self.neighbours(state, len(problem) - 1):
        if neighbour == None:
            value += 1000
        else:
            value += self.problemPathCost[problem[neighbour[0]][neighbour[1]]]

    return value


    def applyAction(self, state, action):
        """
        Generate next state by performing the action on the state.
        Args:
            state: tuple - (x,y). State of the agent.
            action: character - 'N'. Action to perform.
        Returns: tuple -> (x,y). Next state of the agent.
        """
        if action == 'N':
            return (state[0] - 1, state[1])

        if action == 'E':
            return (state[0], state[1] + 1)

        if action == 'W':
            return (state[0], state[1] - 1)

        if action == 'S':
            return (state[0] + 1, state[1])

    def generateChild(self, problem, node, action):
        """
        Generate the child node by performing the legal action on the current state
        and calculating the estimated cost to reach to the goal state and actual cost to
        reach to the current state from the start state.
        Args:
            problem: 2d list of characters - [['m','p'],['s','p']]. Problem with terrain as characters.
            goal: tuple - (x,y). Goal state to reach.
            node: Object - Node. Node object representing current state.
            action: character - 'S'. Action to perform on the state.
        Returns: Object - Node. The Child node.
        """
        # get the next state
        state = self.applyAction(node.state, action)
        # calculate hueristic cost
        estimateCost = self.evaluateHeuristic(problem, state)
        return Node(estimateCost, 0, state, node, action)
    
    def findActions(self, problem, state):
        """
        Find all legal actions allowed on the state.
        Args:
            size: int. Size of the problem terrain.
            state: tuple - (x,y). State of the agent on which to perform actions.
        Returns: [] -> list of actions.
        """
        size = len(problem) - 1
        legalActions = []
        if state[0] > 0 and problem[state[0] - 1][state[1]] != 'w':
            legalActions.append('N')
        if state[0] < size and problem[state[0] + 1][state[1]] != 'w':
            legalActions.append('S')
        if state[1] > 0 and problem[state[0]][state[1] - 1] != 'w':
            legalActions.append('W')
        if state[1] < size and problem[state[0]][state[1] + 1] != 'w':
            legalActions.append('E')
        return legalActions
    
    def getBestNodeDistance(self, current, best):
        return (abs(current[0] - best[0]) + abs(current[1] - best[1]))

    def goalTest(self, node, goal):
        """
        Test whether the goal state has been reached, if not find a goal state
        in frontier that is satisfiable(<= 300 calories), but not optimal.
        Args:
            node: Object - Node. The node to test for goal.
            goal: tuple(x,y). The goal state.
            frontier: []. list of frontier nodes prioritized by estimated cost
            to reach the goal.
        Returns: Object- Node. The goal node that is either satisfiable or optimal.
        """
        if node.state == goal:
            return node

    def getExploredStates(self, node):
        """
        Print the solution path by backtracking to the root node
        following throught all the parent nodes.
        Args:
            node: Object - Node. The node containing goal state at the end of the search.
        Returns: string. String of actions performed on root node
        to reach the goal node.
        """
        nodes = []
        while node.parent:
            nodes.insert(0, node)
            node = node.parent

        return nodes

    def generateBacktrackNode(self, problem, goal, node, action):
        state = self.applyAction(node.state, action)
        estimateCost = node.actualCost + self.problemPathCost[problem[state[0]][state[1]]]
        return Node(estimateCost, 0, state, node, action)

    def backtrackSearch(self, start, goal, problem):

        explored = set()
        frontier = []
        node = Node(0, 0, start.state, None, None)
        heappush(frontier, node)
        while (True):
            if len(frontier) == 0:
                return "Path does not exists."

            node = heappop(frontier)
            if self.goalTest(node, goal.state):
                return self.getExploredStates(node)

            explored.add(node.state)
            Actions = self.findActions(problem, node.state)
            for action in Actions:
                neighbour = self.generateBacktrackNode(problem, goal, node, action)
                if neighbour != None:
                    if neighbour not in frontier and neighbour.state not in explored:
                        heappush(frontier, neighbour)

    def solve(self, start, strength, problem):
        explored = set()
        frontier = []
        node = Node(0, 0, start, None, None)
        # push the start node to the beam
        heappush(frontier, node)
        explored.add(node.state)
        if len(frontier) == 0:
            return "Path does not exists."

        prevnode = node
        node = heappop(frontier)

        if self.getBestNodeDistance(prevnode.state, node.state) > 1:
            backtrackNodes = self.backtrackSearch(prevnode, node, problem)
            for backTrackNode in len(backtrackNodes):
                return backTrackNode.action
        else:
            return node.action

        # get the list of all possible actions on the state
        Actions = self.findActions(problem, node.state)
        for action in Actions:
            # generate a child node by applying actions to the current state
            neighbour = self.generateChild(problem, node, action)
            # check if child is already explored or present in beam
            if neighbour not in frontier and neighbour.state not in explored:
                #add node to frontier only if it can contain within best k nodes
                heappush(frontier, neighbour)

    def step(self, location, strength, game_map, map_objects):
        return self.solve(location, strength, game_map)