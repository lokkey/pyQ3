#### Libraries
# Standard library
import random

# Third-party libraries

class Player:
	"""
	Valid movement values. 0 indicates no movement.
	8 1 2
	7 0 3
	6 5 4

	"""
	
	def __init__(self, color):
		self.frags = 0
		self.color = color;
		self.init()
		
	def init(self):
		self.health = 100;
		self.myX, self.myY = (5 + random.randint(0,1)*10), (5 + random.randint(0,1)*10) #random initialization
		self.quad = False
		self.rockets = 25
		self.currentAction = None
		self.alive = True
		self.lastx, self.lasty = self.myX, self.myY
		
	def setOpp(self, opp):
		self.opp = opp
	
	def setAgent(self, agent):
		self.agent = agent
	
	#TODO - pass player.quad to agent
	def act(self, time, rockets, healthPack1, healthPack2, healthPack3, healthPack4, quad):
		print '({time}) X: {x} Y: {y}'.format(time = time, x = self.myX, y = self.myY)
		self.currentAction = self.agent.act(self.myX, self.myY, self.opp.lastx, self.opp.lasty, self.frags, self.opp.frags, self.health, self.opp.health, self.rockets, time, rockets, healthPack1, healthPack2, healthPack3, healthPack4, quad)
		