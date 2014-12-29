# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        """
        If we reach the goal state, let us give a score of infinity
        If the pacman gets killed, let us give the socre of - infinity
        For the rest minimize the chance of killing and try to capture the food
        Each action is weighted accordingly
        """ 
        score = 500     
        if successorGameState.isWin() :
            return float("inf")- 100
        if successorGameState.isLose() :
            return -(float("inf")- 100)
        gostDistance = 100
        for gost in newGhostStates :
            if gost.getPosition() == tuple(newPos) : 
                if gost.scaredTimer is 0:
                    return -(float("inf") -100) 
            else :
                if manhattanDistance(newPos,gost.getPosition()) < gostDistance :
                    gostDistance = manhattanDistance(newPos, gost.getPosition())
        score += gostDistance*2
        if action == Directions.STOP:
            score -= 20
        if successorGameState.getNumFood() < currentGameState.getNumFood() :
            score += 200
        closestFood = 50
        for food in newFood.asList() :
            if manhattanDistance(newPos, food) < closestFood :
                closestFood = manhattanDistance(newPos, food)
                score -= closestFood*2;
        
        if successorGameState.getPacmanPosition() in currentGameState.getCapsules():
            score += 600
        return score

def scoreEvaluationFunction(currentGameState):
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
    This function returns the result on behalf of the all the ghosts. 
    Since we need to consider all the  ghosts, the function calls itself for "number of ghosts" 
    times before calling Max Again. Also since we consider all ghosts as one MIN.
    we decrease the depth only after we are done with all the agents.         
    """
    
    def getMin(self, currentgameState, agentNum, depth):
        numOfGhosts = currentgameState.getNumAgents()-1
        if currentgameState.isWin() or currentgameState.isLose() or depth <=0 :
            return currentgameState.getScore()
        bestMinimum = float("inf")
        if agentNum == numOfGhosts :
            "it is  pacman move now"
            actions = currentgameState.getLegalActions(agentNum)
            "Removing Directions.STOP for  Better Performance"
            if Directions.STOP in actions :
                actions.remove(Directions.STOP)
            for action in actions:
                "getting the next successor state"
                successorState = currentgameState.generateSuccessor(agentNum, action)
                currentMinimum = self.getMax(successorState,depth-1);
                " updating the minimum to the best value" 
                bestMinimum = min (currentMinimum,bestMinimum)
        else:
            "it is  next gost move now"
            actions = currentgameState.getLegalActions(agentNum)
            "Removing Directions.STOP for  Better Performance"
            if Directions.STOP in actions :
                actions.remove(Directions.STOP)
            for action in actions  :
                "getting the next successor state"
                successorState = currentgameState.generateSuccessor(agentNum, action)
                currentMinimum =  self.getMin(successorState,agentNum+1, depth)
                " updating the minimum to the best value" 
                bestMinimum = min (currentMinimum,bestMinimum)
        return bestMinimum
    
    """
    This function returns the result on behalf of the PACMAN agents. 
    we decrease the depth only after we are done with one MAX         
    """  
    def getMax(self, currentgameState, depth):
        if currentgameState.isWin() or currentgameState.isLose() or depth <=0 :
            return currentgameState.getScore()
        
        bestMaximum = -float("inf");
        "pacman legal actions"
        actions = currentgameState.getLegalActions(0)
        "Removing Directions.STOP for  Better Performance"
        if Directions.STOP in actions :
            actions.remove(Directions.STOP)
        for action in actions :
            "getting the next successor state"
            successorState = currentgameState.generateSuccessor(0, action)
            currentMaximum = self.getMin(successorState,1, depth )
            " updating the Maximum to the best value" 
            bestMaximum = max(currentMaximum, bestMaximum)
        return bestMaximum
    
    
    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions()
        if Directions.STOP in actions :
            actions.remove(Directions.STOP)
        currentaction = Directions.STOP
        currentMax = -(float("inf"))
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            prev = currentMax
            currentMax = max(currentMax, self.getMin(nextState, 1,self.depth))
            if currentMax > prev:
                currentaction = action
        return currentaction
        
        util.raiseNotDefined()
        " RETUNRN THE MAX VALUE OF ALL THE MIN VALLUE OF THE STATES. "
    
   
        


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    """
    This function returns the result on behalf of the all the ghosts. 
    Since we need to consider all the  ghosts, the function calls itself for "number of ghosts" 
    times before calling Max Again. Also since we consider all ghosts as one MIN.
    And when ALPHA > BETA we RETURN (PRUNING)
    we decrease the depth only after we are done with all the agents.         
    """
    
    def getMin(self, currentgameState, agentNum, depth, numOfGhosts,alpha, beta):
        if currentgameState.isWin() or currentgameState.isLose() or depth <=0 :
            return self.evaluationFunction(currentgameState)
        
        if agentNum == numOfGhosts :
            actions = currentgameState.getLegalActions(agentNum)
            "Removing Directions.STOP for  Better Performance"
            if Directions.STOP in actions :
                actions.remove(Directions.STOP)
            for action in actions:
                if alpha < beta :
                    successorState = currentgameState.generateSuccessor(agentNum, action)
                    currentBeta = self.getMax(successorState,depth-1,numOfGhosts,alpha, beta)
                    beta = min (beta,currentBeta)
                else :
                    return beta
        else:
            actions = currentgameState.getLegalActions(agentNum)
            "Removing Directions.STOP for  Better Performance"
            if Directions.STOP in actions :
                actions.remove(Directions.STOP)
            for action in actions:
                if alpha < beta :
                    successorState = currentgameState.generateSuccessor(agentNum, action)
                    currentBeta =  self.getMin(successorState,agentNum+1, depth,numOfGhosts, alpha, beta);
                    beta = min (beta,currentBeta)
                else :
                    return beta
        return beta
    
    def getMax(self, currentgameState, depth, numOfGhosts, alpha, beta):
        if currentgameState.isWin() or currentgameState.isLose() or depth <=0 :
            return self.evaluationFunction(currentgameState)
          
        "pacman legal actions"
        actions = currentgameState.getLegalActions(0)
        "Removing Directions.STOP for  Better Performance"
        if Directions.STOP in actions :
                actions.remove(Directions.STOP)
        for action in actions:
            if alpha < beta :
                successorState = currentgameState.generateSuccessor(0, action)
                currentAlpha = self.getMin(successorState,1, depth,numOfGhosts, alpha, beta)
                alpha = max(alpha,currentAlpha)
            else :
                return alpha
        return alpha

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions()
        "Removing Directions.STOP for  Better Performance"
        if Directions.STOP in actions :
                actions.remove(Directions.STOP)
        numOfGhosts = gameState.getNumAgents() - 1
        currentaction = Directions.STOP
        alpha = -(float("inf"))
        beta = float("inf")
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            prev = alpha
            alpha = max(alpha, self.getMin(nextState, 1,self.depth,numOfGhosts, alpha, beta))
            if alpha > prev:
                currentaction = action
        return currentaction
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

