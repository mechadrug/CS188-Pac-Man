# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import math
from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def helper(depth,game_state,agent_index):
            agent_index=agent_index%game_state.getNumAgents()

            if game_state.isWin() or game_state.isLose() or depth==self.depth*gameState.getNumAgents()-1:
                return self.evaluationFunction(game_state)
            
            elif agent_index==0:
                max_value=-float('inf')
                for i in game_state.getLegalActions(agent_index):  
                    value=helper(depth+1,game_state.generateSuccessor(agent_index,i),agent_index+1)
                    max_value=max(max_value,value)
                return max_value
            else:
                min_value=float('inf')
                for i in game_state.getLegalActions(agent_index):
                    value=helper(depth+1,game_state.generateSuccessor(agent_index,i),agent_index+1)
                    min_value=min(value,min_value)
                return min_value
        
        max_score = -float('inf')
        best_action = None
        actions = gameState.getLegalActions(0)

        for action in actions:
            score = helper(0, gameState.generateSuccessor(0, action), 1)
            if score > max_score:
                max_score = score
                best_action = action

        return best_action
        util.raiseNotDefined()#该函数的主要作用是在调用未实现的方法时提示开发者，并通过提供调用栈的详细信息（文件名、行号、方法名）帮助调试。

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def helper(depth,game_state,agent_index,beta,alpha):
            agent_index=agent_index%game_state.getNumAgents()

            if game_state.isWin() or game_state.isLose() or depth==self.depth*gameState.getNumAgents()-1:
                return self.evaluationFunction(game_state)
            
            elif agent_index==0:
                max_value=-float('inf')
                for i in game_state.getLegalActions(agent_index):  
                    value=helper(depth+1,game_state.generateSuccessor(agent_index,i),agent_index+1,beta,alpha)
                    max_value=max(max_value,value)
                    if max_value>beta:return max_value
                    alpha=max(alpha,max_value)
                return max_value
            else:
                min_value=float('inf')
                for i in game_state.getLegalActions(agent_index):
                    value=helper(depth+1,game_state.generateSuccessor(agent_index,i),agent_index+1,beta,alpha)
                    min_value=min(value,min_value)
                    if min_value<alpha:return min_value
                    beta= min(min_value,beta)
                return min_value
        
        max_score = -float('inf')
        best_action = None
        actions = gameState.getLegalActions(0)
        beta=float('inf')
        alpha=-float('inf')
        for action in actions:
            score = helper(0, gameState.generateSuccessor(0, action), 1,beta,alpha)
            if score > max_score:
                max_score = score
                best_action = action
            alpha=max(max_score,alpha)

        return best_action
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def helper(depth,game_state,agent_index):
            agent_index=agent_index%game_state.getNumAgents()

            if game_state.isWin() or game_state.isLose() or depth==self.depth*gameState.getNumAgents()-1:
                return self.evaluationFunction(game_state)
            
            elif agent_index==0:
                max_value=-float('inf')
                for i in game_state.getLegalActions(agent_index):  
                    value=helper(depth+1,game_state.generateSuccessor(agent_index,i),agent_index+1)
                    max_value=max(max_value,value)
                return max_value
            else:
                sum_score=0
                num=0
                for i in game_state.getLegalActions(agent_index):
                    sum_score+=helper(depth+1,game_state.generateSuccessor(agent_index,i),agent_index+1)
                    num+=1
                return sum_score/num
        
        max_score = -float('inf')
        best_action = None
        actions = gameState.getLegalActions(0)

        for action in actions:
            score = helper(0, gameState.generateSuccessor(0, action), 1)
            if score > max_score:
                max_score = score
                best_action = action

        return best_action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    Position = currentGameState.getPacmanPosition()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    
    score = currentGameState.getScore()
    walls = currentGameState.getWalls()
    Food = currentGameState.getFood()
    foodList = Food.asList()
    capsules = currentGameState.getCapsules()

    for food in foodList:
        distance = util.manhattanDistance(Position, food)
        score += 6 * math.exp(-distance / 2) + 0.7

    for capsule in capsules:
        distance = util.manhattanDistance(Position, capsule)
        score += 6 * math.exp(-distance / 2) + 0.7
    for i, ghostState in enumerate(GhostStates):
        ghostPos = ghostState.getPosition()
        distance = util.manhattanDistance(Position, ghostPos)
        if ScaredTimes[i] > 5:
            score += 150 + math.exp(3 / distance) 
        elif 0 < ScaredTimes[i] <= 5:
            score += 5 + math.exp(3 / distance)
        else:
            if distance <= 2.7:
                score -= 500 
            else:
                score -= 7 * math.exp(-distance / 2) 

    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
