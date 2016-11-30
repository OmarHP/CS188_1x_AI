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
from game import Actions

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
        newRemainingCapsules=successorGameState.getCapsules()



        "*** YOUR CODE HERE ***"
        #score=successorGameState.getScore()

        score=0.0
        from util import manhattanDistance

        # =======================================================================
        # ========================================== Eat food ===================
        # =======================================================================

        score=successorGameState.getScore()+1.0/dfs_distanceClosestDot(successorGameState)

        # =======================================================================
        # ========================================== Eat capsulates =============
        # =======================================================================
        capsulesDistances=[]

        remainingCapsules=currentGameState.getCapsules()
        ghostStates = currentGameState.getGhostStates()
        scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
        scaredGhosts=filter(lambda x:x>0,scaredTimes)

        #print(action,scaredGhosts)
        if len(scaredGhosts)<1 and len(remainingCapsules)>0:
            for cap in newRemainingCapsules:
                capsulesDistances.append(manhattanDistance(newPos,cap))
            if(len(capsulesDistances)>0):
                closestCapsule=min(capsulesDistances)
                score=successorGameState.getScore()+1.0/(closestCapsule)
                #print("yendo hacia capsula")
            else:
                if(len(remainingCapsules)-len(newRemainingCapsules)==1):
                    score=successorGameState.getScore()+500


        # =======================================================================
        # ========================================== Eat ghosts =================
        # =======================================================================

        # =======================================================================
        # ========================================== Avoid ghosts ===============
        # =======================================================================
        ghostDistances=[]
        for ghostState in newGhostStates:
            if(ghostState.scaredTimer<2):
                ghostDistances.append(manhattanDistance(newPos,ghostState.getPosition()))

        if len(ghostDistances)>0:
            minDistance=min(ghostDistances)
            if(minDistance<2):
                score=-1000-minDistance



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
      Your minimax agent (question 2)
    """

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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #print("================ nuevo arbol ===========================")
        maxValue=self.max_value(gameState,0,0);
        return maxValue[1];


    def minimax_value(self, state, realDepth):
        depth=realDepth//state.getNumAgents()
        if(depth+1>self.depth or state.isLose() or state.isWin()):
            return (self.evaluationFunction(state),"Stop")
        if(realDepth%state.getNumAgents()==0):
            return self.max_value(state,0,realDepth)
        elif(realDepth%state.getNumAgents()!=0):
            return self.min_value(state,realDepth%state.getNumAgents(),realDepth)


    def max_value(self, state, agent, realDepth):
        from sys import maxint
        legalActions=state.getLegalActions(agent)
        maxV=((-maxint-1),"Stop");
        for action in legalActions:
            successorState=state.generateSuccessor(agent, action)
            maxV=max(maxV,(self.minimax_value(successorState,realDepth+1)[0],action),key=lambda x:x[0])
        return maxV

    def min_value(self, state, agent, realDepth):
        from sys import maxint
        legalActions=state.getLegalActions(agent)
        minV=((maxint),"Stop");
        for action in legalActions:
            successorState=state.generateSuccessor(agent, action)
            minV=min(minV,(self.minimax_value(successorState,realDepth+1)[0],action),key=lambda x:x[0])
        return minV

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #print("================ nuevo arbol ===========================")
        from sys import maxint
        maxValue=self.max_value(gameState,0,0,(-maxint-1),maxint);
        return maxValue[1];


    def minimax_value(self, state, realDepth, alpha, beta):
        depth=realDepth//state.getNumAgents()
        if(depth+1>self.depth or state.isLose() or state.isWin()):
            return (self.evaluationFunction(state),"Stop")
        if(realDepth%state.getNumAgents()==0):
            return self.max_value(state,0,realDepth,alpha,beta)
        elif(realDepth%state.getNumAgents()!=0):
            return self.min_value(state,realDepth%state.getNumAgents(),realDepth,alpha,beta)


    def max_value(self, state, agent, realDepth,alpha,beta):
        from sys import maxint
        legalActions=state.getLegalActions(agent)
        maxV=((-maxint-1),"Stop");
        for action in legalActions:
            successorState=state.generateSuccessor(agent, action)
            maxV=max(maxV,(self.minimax_value(successorState,realDepth+1,alpha,beta)[0],action),key=lambda x:x[0])
            if maxV[0]>beta :
                return maxV
            alpha=max(maxV[0],alpha)
        return maxV

    def min_value(self, state, agent, realDepth,alpha,beta):
        from sys import maxint
        legalActions=state.getLegalActions(agent)
        minV=((maxint),"Stop");
        for action in legalActions:
            successorState=state.generateSuccessor(agent, action)
            minV=min(minV,(self.minimax_value(successorState,realDepth+1,alpha,beta)[0],action),key=lambda x:x[0])
            if minV[0]<alpha :
                return minV
            beta=min(minV[0],beta)
        return minV

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
        #print("================ nuevo arbol ===========================")
        maxValue=self.max_value(gameState,0,0);
        return maxValue[1];


    def expectimax_value(self, state, realDepth):
        depth=realDepth//state.getNumAgents()
        if(depth+1>self.depth or state.isLose() or state.isWin()):
            return (self.evaluationFunction(state),"Stop")
        if(realDepth%state.getNumAgents()==0):
            return self.max_value(state,0,realDepth)
        elif(realDepth%state.getNumAgents()!=0):
            return self.exp_value(state,realDepth%state.getNumAgents(),realDepth)


    def max_value(self, state, agent, realDepth):
        from sys import maxint
        legalActions=state.getLegalActions(agent)
        maxV=((-maxint-1),"Stop");
        for action in legalActions:
            successorState=state.generateSuccessor(agent, action)
            maxV=max(maxV,(self.expectimax_value(successorState,realDepth+1)[0],action),key=lambda x:x[0])
        return maxV

    def exp_value(self, state, agent, realDepth):
        from sys import maxint
        legalActions=state.getLegalActions(agent)
        expV=0.0;
        for action in legalActions:
            successorState=state.generateSuccessor(agent, action)
            expV+=self.expectimax_value(successorState,realDepth+1)[0]
        expectedValue=(expV/len(legalActions),"Stop")
        return expectedValue

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    remainingCapsules=currentGameState.getCapsules()
    scaredGhosts=map(lambda y: y.getPosition(),filter(lambda x:x.scaredTimer>0,currentGameState.getGhostStates()))
    score=0

    if len(scaredGhosts)<1 and len(remainingCapsules)>0:
        closestCapsule=dfs_distanceClosestCapsule(currentGameState);
        score=currentGameState.getScore()+1.0/(closestCapsule)-len(remainingCapsules)*10
        return score;

    if len(scaredGhosts)>0:
        closestScared=dfs_distanceClosestScared(currentGameState);
        score=currentGameState.getScore()+1.0/closestScared
        return score;


    distanceToClosestDot=dfs_distanceClosestDot(currentGameState);
    score=currentGameState.getScore()+1.0/distanceToClosestDot
    return score

# Abbreviation
better = betterEvaluationFunction

def dfs_distanceClosestDot(currentState):
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    fringe=PriorityQueue()
    explored = set()
    root=currentState.getPacmanPosition()
    #tuple contains current pacman position, cost
    fringe.push((root,0),0);

    while not fringe.isEmpty():
        current=fringe.pop()
        if(current[0] not in explored):
            explored.add(current[0])
            currentPosition=current[0]
            if(currentState.hasFood(currentPosition[0],currentPosition[1])):
                return current[1]
            else:
                for direction in Actions._directions.values():
                    successor=(currentPosition[0]+direction[0],currentPosition[1]+direction[1])
                    if(currentState.hasWall(successor[0],successor[1])==False):
                        fringe.push((successor,current[1]+1),current[1]+1)
    return 1000.00

def dfs_distanceClosestCapsule(currentState):
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    fringe=PriorityQueue()
    explored = set()
    root=currentState.getPacmanPosition()
    #tuple contains current pacman position, cost
    fringe.push((root,0),0);

    while not fringe.isEmpty():
        current=fringe.pop()
        if(current[0] not in explored):
            explored.add(current[0])
            currentPosition=current[0]
            if((currentPosition[0],currentPosition[1]) in currentState.getCapsules()):
                return current[1]
            else:
                for direction in Actions._directions.values():
                    successor=(currentPosition[0]+direction[0],currentPosition[1]+direction[1])
                    if(currentState.hasWall(successor[0],successor[1])==False):
                        fringe.push((successor,current[1]+1),current[1]+1)
    return 1000.00

def dfs_distanceClosestScared(currentState):
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    fringe=PriorityQueue()
    explored = set()
    root=currentState.getPacmanPosition()
    #tuple contains current pacman position, cost
    fringe.push((root,0),0);

    while not fringe.isEmpty():
        current=fringe.pop()
        if(current[0] not in explored):
            explored.add(current[0])
            currentPosition=current[0]
            scaredGhosts=map(lambda y: y.getPosition(),filter(lambda x:x.scaredTimer>0,currentState.getGhostStates()))
            if((currentPosition[0],currentPosition[1]) in scaredGhosts):
                return current[1]
            else:
                for direction in Actions._directions.values():
                    successor=(currentPosition[0]+direction[0],currentPosition[1]+direction[1])
                    if(currentState.hasWall(successor[0],successor[1])==False):
                        fringe.push((successor,current[1]+1),current[1]+1)
    return 1000.00