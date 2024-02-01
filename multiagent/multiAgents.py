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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        
        # Check for losing condition
        if newPos in [ghostState.getPosition() for ghostState in newGhostStates]:
            return float("-inf")
        for ghostState in newGhostStates:
            if manhattanDistance(newPos, ghostState.getPosition()) < 2:
                return float("-inf")
        
        # Check for winning condition
        if successorGameState.isWin():
            return float("inf")

        score = 0 
        # Penalize STOP action
        if action == Directions.STOP:
            score -= 100


        # Food related score
        foodRadius = 15  # Radius to consider for food score
        foodScore = 0
        for food in newFood.asList():
            distance = manhattanDistance(newPos, food)
            if distance <= foodRadius:
                foodScore += 1 / (distance + 0.000001)

        # Ghost related score
        ghostScore = 0
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        if any(scaredTime > 0 for scaredTime in newScaredTimes):
            foodScore += 5 / (distance + 0.000001)
        for ghostState, scaredTime in zip(newGhostStates, newScaredTimes):
            distance = manhattanDistance(newPos, ghostState.getPosition())
            if scaredTime > 0:
                # Encourage chasing scared ghosts
                ghostScore += 3 / (distance + 0.000001)
            else:
                # Avoid non-scared ghosts
                if distance < 5:
                    ghostScore -= (5 - distance)

        # Combine all scores
        return successorGameState.getScore() + foodScore + ghostScore


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
        def minimax(gameState: GameState, agentIndex: int, depth: int):
           if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

           isPacman = (agentIndex == 0)
           legalActionsNoStop = gameState.getLegalActions(agentIndex)
           legalActionsNoStop = [action for action in legalActionsNoStop if action != Directions.STOP]
           if isPacman:
            return max(minimax(gameState.generateSuccessor(agentIndex, action), 1, depth) for action in legalActionsNoStop)
           else: 
            nextAgentIndex = agentIndex + 1
            if nextAgentIndex == gameState.getNumAgents():
                nextAgentIndex = 0
            if nextAgentIndex == 0:
                depth += 1
            return min(minimax(gameState.generateSuccessor(agentIndex, action), nextAgentIndex, depth) for action in legalActionsNoStop)
        

        legalActions = gameState.getLegalActions(0)
        legalActions = [action for action in legalActions if action != Directions.STOP]
        bestScore = float("-inf")
        for action in legalActions:
            score = minimax(gameState.generateSuccessor(0, action), 1, 0)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction
        

        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def alphabeta(self, gameState: GameState, agentIndex: int, depth: int, alpha: int, beta: int):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)

        isPacman = (agentIndex == 0)
        legalActionsNoStop = gameState.getLegalActions(agentIndex)
        legalActionsNoStop = [action for action in legalActionsNoStop if action != Directions.STOP]
        if isPacman:
            bestSoFar = float("-inf")
            for action in legalActionsNoStop:
                bestSoFar = max(bestSoFar, self.alphabeta(gameState.generateSuccessor(agentIndex, action), 1, depth, alpha, beta))
                alpha = max(alpha, bestSoFar)
                if beta <= alpha:
                    break
            return bestSoFar
        else: 
            nextAgentIndex = agentIndex + 1
            if nextAgentIndex == gameState.getNumAgents():
                nextAgentIndex = 0
            if nextAgentIndex == 0:
                depth += 1
            bestSoFar = float("inf")
            for action in legalActionsNoStop:
                bestSoFar = min(bestSoFar, self.alphabeta(gameState.generateSuccessor(agentIndex, action), nextAgentIndex, depth, alpha, beta))
                beta = min(beta, bestSoFar)
                if beta <= alpha:
                    break
            return bestSoFar

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        legalActions = gameState.getLegalActions(0)
        legalActionsNoStop = [action for action in legalActions if action != Directions.STOP]
        bestScore = float("-inf")
        for action in legalActionsNoStop:
            score = self.alphabeta(gameState=gameState.generateSuccessor(0, action), agentIndex=0, depth=1, alpha=float("-inf"), beta=float("inf"))
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
