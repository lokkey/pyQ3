#### Libraries
# Standard library
import random
import pybrain


class LearningBot:
	"""
	Valid movement values. 0 indicates no movement.
	8 1 2
	7 0 3
	6 5 4

	"""
	def __init__(self, name):
		self.name = name
	
	#TODO - To add firedRockets in the state, quad
	def act(self, myX, myY, oppX, oppY, frags, oppFrags, health, oppHealth, myRockets, time, rocketMap, healthPack1, healthPack2, healthPack3, healthPack4, quad):
		#some kick-ass stuff
		#maintain quad values and rockets of opponent in the logic
		return [random.randint(-1,1), random.randint(-1,1), oppX, oppY] #movex, movey, firex, firey
