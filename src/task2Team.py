# myTeam.py
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


from captureAgents import CaptureAgent
import random
import time
from captureGraphicsDisplay import FOOD_COLOR
import util
from game import Directions
import game

#################
# Team creation #
#################


def createTeam(firstIndex, secondIndex, isRed,
               first='FoodAgent', second='CapsuleAgent'):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.  isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments ("first" and "second" are
    such arguments in the case of this function), which will come from
    the --redOpts and --blueOpts command-line arguments to capture.py.
    For the nightly contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """

    # The following line is an example only; feel free to change it.
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########


class Task2Agent(CaptureAgent):
    def registerInitialState(self, gameState):
        self.start = gameState.getAgentPosition(self.index)
        CaptureAgent.registerInitialState(self, gameState)

    def getActionToGoToStart(self, gameState):
        actions = gameState.getLegalActions(self.index)
        minDist = 9999
        for action in actions:
            successor = gameState.generateSuccessor(self.index, action)
            nextPos = successor.getAgentState(self.index).getPosition()
            nextDist = self.getMazeDistance(nextPos, self.start)
            if nextDist < minDist:
                minDist = nextDist
                choice = action

        return choice


class FoodAgent(Task2Agent):
    """
    Agent 1:
    Move to the enemy camp, eat 5 pellets, and return to our camp
    """

    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)
        myState = gameState.getAgentState(self.index)

        targetFood = self.getClosestFood(gameState)
        if myState.numCarrying >= 5 or targetFood is None:
            return self.getActionToGoToStart(gameState)

        minDist = 9999
        for action in actions:
            successor = gameState.generateSuccessor(self.index, action)
            nextPos = successor.getAgentState(self.index).getPosition()
            nextDist = self.getMazeDistance(nextPos, targetFood)
            if nextDist < minDist:
                minDist = nextDist
                choice = action

        return choice

    def getClosestFood(self, gameState):
        myPos = gameState.getAgentState(self.index).getPosition()
        foodList = self.getFood(gameState).asList()

        if not any(foodList):
            return None

        minDist = 9999
        for food in foodList:
            dist = self.getMazeDistance(myPos, food)
            if dist < minDist:
                minDist = dist
                closestFood = food

        return closestFood


class CapsuleAgent(Task2Agent):
    """
    Agent 2:
    Move to the enemy camp, eat power pellet
    """

    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)
        targetCapsule = self.getClosestCapsule(gameState)

        if targetCapsule is None:
            return self.getActionToGoToStart(gameState)

        minDist = 9999
        for action in actions:
            successor = gameState.generateSuccessor(self.index, action)
            nextPos = successor.getAgentState(self.index).getPosition()
            nextDist = self.getMazeDistance(nextPos, targetCapsule)
            if nextDist < minDist:
                minDist = nextDist
                choice = action

        return choice

    def getClosestCapsule(self, gameState):
        capsuleList = self.getCapsules(gameState)
        if not any(capsuleList):
            return None
        myPos = gameState.getAgentState(self.index).getPosition()

        minDist = 9999
        for capsule in capsuleList:
            dist = self.getMazeDistance(myPos, capsule)
            if dist < minDist:
                minDist = dist
                closestCapsule = capsule

        return closestCapsule
