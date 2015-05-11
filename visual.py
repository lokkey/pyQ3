"""
Main.py
~~~~~~~~~~

#Class summary
"""

#### Libraries
# Standard library
import player
import rocket
import simplebot
import learningbot
import pygame
from rocket import Rocket

class Visual:
	FRAG_LIMIT = 20
	GRID_SIZE = 20
	ROCKET_PACK_SIZE = 10
	DAMAGE_MULTIPLIER = 0.6
	SQUARE_SIZE = 30
	
	def __init__(self):
		print("init")
		self.players = []
		self.initPlayers()
		self.time = -1
		self.firedRockets = []
		self.rockets = [[0 for i in range(self.GRID_SIZE+1)] for j in range(self.GRID_SIZE+1)]
		self.quad = True
		self.healthPack1, self.healthPack2, self.healthPack3, self.healthPack4 = True, True, True, True
		self.startMatch()
	
	def initPlayers(self):
		self.player1 = player.Player((0,255,0))
		self.player2 = player.Player((0,0,0))
		self.player1.setOpp(self.player2)
		self.player2.setOpp(self.player1)
		self.players.append(self.player1)
		self.players.append(self.player2)
		self.player1.setAgent(simplebot.SimpleBot("SimpleBot"))
		self.player2.setAgent(learningbot.LearningBot("LearningBot"))
		
	def startMatch(self):
		pygame.init()
		size = [700,500]
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(size)
		pygame.display.set_caption("PyQ3")
		self.sqcolor = [[(200,200,200) for i in range(self.GRID_SIZE+1)] for j in range(self.GRID_SIZE+1)]

		done = False;
		while done == False:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
			
			done = self.runOnce()
			self.clock.tick(30)
			
		
	def runOnce(self):
		
		#update time
		self.time += 1
		
		#update resource map with spontaneous resources
		self.updateResources()
				
		#effect players movement
		for player in self.players:
			player.act(self.time, self.rockets, self.healthPack1, self.healthPack2, self.healthPack3, self.healthPack4, self.quad)
			if self.isValidPoint([player.myX + player.currentAction[0], player.myY + player.currentAction[1]]):
				player.myX = player.myX + player.currentAction[0]
				player.myY = player.myY + player.currentAction[1]

			
			if self.isQuad(player):
				print '{bot} acquired quad'.format(bot = player.agent.name)
				self.pickQuad(player)
			if self.isHealth(player):
				print '{bot} acquired health'.format(bot = player.agent.name)
				self.pickHealth(player)
			if self.isRocket(player):
				print '{bot} acquired rockets'.format(bot = player.agent.name)
				self.pickRockets(player)
		
		for player in self.players:
			player.lastx = player.myX
			player.lasty = player.myY 
			
		
		rocketsToRemove = []
		#move rocket
		for rocket in self.firedRockets:
			rocketPos = rocket.getPos(True) #move and give pos
			#print 'rocket at {a},{b}'.format(a=rocketPos[0], b=rocketPos[1])
		
		#rocket explode
		#TODO - if any player and rocket are on same spot, rocket should explode
		#TODO - explosion not accurate on edges
			if (rocket.isAlive()==False or rocketPos[0] == self.GRID_SIZE+1 or rocketPos[1] == self.GRID_SIZE+1):
				print 'rocket exploded at {x},{y}'.format(x=rocketPos[0], y=rocketPos[1])
				mult = 4 if rocket.owner.quad else 1
				for i in range(-2,2):
					for j in range(-2, 2):
						rdx = rocketPos[0]+i #rdx = rocket damage x
						rdy = rocketPos[1]+j #rocket damage y
						for player in self.players:
							if(player.myX == rdx and player.myY == rdy):
								print 'player({x},{y}) health before explosion {h}'.format(x = rdx, y = rdy, h = player.health)
								player.health -= (rocket.DAMAGE[i+2][j+2] * mult) * self.DAMAGE_MULTIPLIER
								print 'player({x},{y}) health after explosion {h}'.format(x = rdx, y = rdy, h = player.health)
								if player.health <= 0:
									self.rockets[rdx][rdy] += self.ROCKET_PACK_SIZE #update for dropped rocket pack
									player.alive = False
				rocketsToRemove.append(rocket)	#TODO - check whether it is working fine - removing while iterating
		
		
		#remove rockets from live rockets
		for rocket in rocketsToRemove:
			self.firedRockets.remove(rocket)

		

		#effect players firing
		for player in self.players:
			if not (player.currentAction[2] == -1 or player.currentAction[3] == -1 or player.rockets < 1):
				rocket1 = Rocket(player.myX, player.myY, player.currentAction[2], player.currentAction[3], player, player.quad)
				self.firedRockets.append(rocket1)
				player.rockets -= 1
				print 'rocket aimed at {x}, {y}'.format(x = player.currentAction[2], y = player.currentAction[3])

		self.updateDisplay()

		#update frags
		for player in self.players:
			if not player.alive:
				player.opp.frags += 1
				player.init()
				
		#print score
		self.printScore()
		return not (self.player1.frags < self.FRAG_LIMIT and self.player2.frags < self.FRAG_LIMIT)
		
			
	def updateResources(self):
		if (self.time%80 == 0):
			for i in range(0,self.GRID_SIZE+1):
				for j in range(0,self.GRID_SIZE+1):
					if self.rockets[i][j] > 0:
						self.rockets[i][j] = 0
		
		if (self.time%25 == 0):
			#Refresh rockets 0510, 1015, 1510, 1005
			print ("self.time%100 = 0")
			self.rockets[5][10] += 10
			self.rockets[10][15] += 10
			self.rockets[15][10] += 10
			self.rockets[10][5] += 10
		
		
		if (self.time%20 == 0):
			print ("self.time%50 = 0")
			self.healthPack1 = True #0000
			self.healthPack2 = True	#0020
			self.healthPack3 = True #2000
			self.healthPack4 = True #2020
		
		if(self.time%100 == 0):
			print ("self.time%125 = 0")
			self.quad = True	#1010
			
	def isQuad(self, player):
		x, y = player.myX, player.myY
		return x == 10 and y == 10
		
	def isHealth(self, player):
		x, y = player.myX, player.myY
		return ((x==0 and y==0) or (x==0 and y == 20) or (x==20 and y==0) or (x==20 and y==20))
	
	def isRocket(self, player):
		x, y = player.myX, player.myY
		return self.rockets[x][y] > 0
	
	def pickQuad(self, player):
		player.quad = True
		self.quad = False
	
	def pickHealth(self, player):
		x, y = player.myX, player.myY
		if(x==0 and y==0):
			self.healthPack1 = False
		elif(x==20 and y==0):
			self.healthPack2 = False	
		elif(x==0 and y==20):
			self.healthPack3 = False
		elif(x==20 and y==20):
			self.healthPack4 = False
		player.health += 25
		player.health = min(100, player.health) #max 100 health
	
	def pickRockets (self, player):
		player.rockets += self.rockets[player.myX][player.myY]
		player.rockets = min(50, player.rockets) #max 25 rockets
		self.rockets[player.myX][player.myY] = 0
			
	def isValidPoint(self, point):
		#print 'isValid {x} {y}'.format(x = point[0], y = point[1])
		return point[0] < self.GRID_SIZE+1 and point[1] < self.GRID_SIZE+1 and point [0] > -1 and point[1] > -1
			
	def printScore(self):
		print '( {time} ) \t {p1frags} \t {p2frags}'.format(time = self.time, p1frags=self.player1.frags, p2frags = self.player2.frags)
	
	def updateDisplay(self):
		self.screen.fill((255,255,255)) #white
			
		"""draw grid"""
		for i in range(0,self.GRID_SIZE+1):
			for j in range(0,self.GRID_SIZE+1):
				self.sqcolor[i][j] = (200,200,200) #grey
		
		linewidth = 1
		for i in range(0,self.GRID_SIZE+1):
			for j in range(0,self.GRID_SIZE+1):
				pygame.draw.rect(self.screen, self.sqcolor[i][j], [i*20, j*20, 20, 20], linewidth)
		
		"""draw health packs"""
		linewidth = 0
		i,j = 0,0
		if(self.healthPack1):
			i,j = 0,0
			self.sqcolor[i][j] = (255,255,0) #yellow
			pygame.draw.rect(self.screen, self.sqcolor[i][j], [i*20, j*20, 20, 20], linewidth) 
		if(self.healthPack2):
			i,j = 20,0
			self.sqcolor[i][j] = (255,255,0) #yellow
			pygame.draw.rect(self.screen, self.sqcolor[i][j], [i*20, j*20, 20, 20], linewidth) #yellow	
		if(self.healthPack3):
			i,j = 0,20
			self.sqcolor[i][j] = (255,255,0) #yellow
			pygame.draw.rect(self.screen, self.sqcolor[i][j], [i*20, j*20, 20, 20], linewidth) #yellow
		if(self.healthPack4):
			i,j = 20,20
			self.sqcolor[i][j] = (255,255,0) #yellow
			pygame.draw.rect(self.screen, self.sqcolor[i][j], [i*20, j*20, 20, 20], linewidth) #yellow	
		
		#print self.rockets
		"""draw rocket packs"""			
		for i in range(0,self.GRID_SIZE+1):
			for j in range(0,self.GRID_SIZE+1):
				if self.rockets[i][j] > 0:
					self.sqcolor[i][j] = (255,0,0) #red
					linewidth = 0
					pygame.draw.rect(self.screen, self.sqcolor[i][j], [i*20, j*20, 20, 20], linewidth)
		

		"""draw fired rockets"""
		for rocket in self.firedRockets:
			rocketPos = rocket.getPos(False)
			linewidth = 0
			pygame.draw.rect(self.screen, rocket.owner.color, [rocketPos[0]*20, rocketPos[1]*20, 20, 20], linewidth)
		
		"""quad"""
		if(self.quad):
			i,j = 10,10
			self.sqcolor[i][j] = (0,0,255) #blue
			linewidth = 0
			pygame.draw.rect(self.screen, self.sqcolor[i][j], [i*20, j*20, 20, 20], linewidth)
		
		"""draw players"""
		for player in self.players:
			linewidth = 4
			pygame.draw.rect(self.screen, player.color, [player.myX*20, player.myY*20, 20, 20], linewidth)
			pygame.draw.rect(self.screen, player.color, [max(0,player.myX*20 - 6), max(0,player.myY*20 -6), 32, 32], linewidth)
		
		pygame.display.flip()
		#pygame.time.delay(10)
		#clock.tick(30)
		#self.clock.tick(100)

