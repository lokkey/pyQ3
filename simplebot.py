#### Libraries
# Standard library
import random

class SimpleBot:
	"""
	Valid movement values. 0 indicates no movement.
	8 1 2
	7 0 3
	6 5 4

	"""
	def __init__(self, name):
		self.name = name
		pass
	
	def act(self, myX, myY, oppX, oppY, frags, oppFrags, health, oppHealth, myRockets, time, rocketMap, healthPack1, healthPack2, healthPack3, healthPack4, quad):
		return [random.randint(-1,1), random.randint(-1,1), oppX, oppY] #movex, movey, firex, firey
