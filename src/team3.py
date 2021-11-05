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
import numpy as np

#################
# Team creation #
#################


def createTeam(firstIndex, secondIndex, isRed,
               first='BlockAgent', second='BlockAgent'):
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


class BlockAgent(CaptureAgent):
    def registerInitialState(self, gameState):
        self.start = gameState.getAgentPosition(self.index)
        map = gameState.data.layout
        CaptureAgent.registerInitialState(self, gameState)

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

    def chooseActionToward(self, gameState, pos):
        actions = gameState.getLegalActions(self.index)

        minDist = 9999
        for action in actions:
            successor = gameState.generateSuccessor(self.index, action)
            nextPos = successor.getAgentState(self.index).getPosition()
            nextDist = self.getMazeDistance(nextPos, pos)
            if nextDist < minDist:
                minDist = nextDist
                choice = action

        return choice

    def chooseActionFarAway(self, gameState, pos):
        actions = gameState.getLegalActions(self.index)

        maxDist = -1
        for action in actions:
            successor = gameState.generateSuccessor(self.index, action)
            nextPos = successor.getAgentState(self.index).getPosition()
            nextDist = self.getMazeDistance(nextPos, pos)
            if nextDist > maxDist:
                maxDist = nextDist
                choice = action

        return choice

    def getActionTowardClosestFood(self, gameState):
        targetFood = self.getClosestFood(gameState)
        if targetFood is None:
            choice = self.chooseActionToward(gameState, self.start)
        else:
            choice = self.chooseActionToward(gameState, targetFood)

        return choice

    def chooseAction(self, gameState):
        myState = gameState.getAgentState(self.index)
        curPos = myState.getPosition()

        opponents = [gameState.getAgentState(i)
                     for i in self.getOpponents(gameState)]
        enemies = [a.getPosition()
                   for a in opponents if not a.isPacman and a.getPosition() is not None]
        invaders = [a.getPosition() for a in opponents if a.isPacman and a.getPosition()
                    is not None]

        # 2 개 먹고 내 진영으로 돌아가기
        if myState.numCarrying >= 2:
            return self.chooseActionToward(gameState, self.start)

        if myState.isPacman:
            if any(enemies):
                dists = np.array([self.getMazeDistance(curPos, pos)
                                 for pos in enemies])
                minDistIdx, minDist = dists.argmin(), dists.min()
                if minDist < 4:
                    choice = self.chooseActionFarAway(
                        gameState, enemies[minDistIdx])
                else:
                    choice = self.getActionTowardClosestFood(gameState)
            else:
                choice = self.getActionTowardClosestFood(gameState)
        else:
            if any(invaders):
                choice = self.chooseActionToward(gameState, invaders[0])
            elif any(enemies):
                dists = np.array([self.getMazeDistance(curPos, pos)
                                 for pos in enemies])
                minDistIdx, minDist = dists.argmin(), dists.min()
                if minDist < 2:
                    choice = self.chooseActionFarAway(
                        gameState, enemies[minDistIdx])
                else:
                    choice = Directions.STOP
            else:
                if gameState.getScore() > 0:
                    choice = Directions.STOP
                else:
                    choice = self.getActionTowardClosestFood(gameState)

        return choice
