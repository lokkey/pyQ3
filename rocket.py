class Rocket:
	
	DAMAGE = [[20,20,20,20,20], 
				[20,60,60,60,20], 
				[20,60,100,60,20], 
				[20,60,60,60,20], 
				[20,20,20,20,20]]
	
	def __init__ (self, x1, y1, x2, y2, owner, quad):
		self.points = self.get_line(x1, y1, x2, y2)
		#print self.points
		self.counter = 0
		self.owner = owner
		self.quad = quad
		self.points = self.get_line(x1, y1, x2, y2)
		self.currentX, self.currentY = self.points[0][0], self.points[0][1]
	
	def setQuad(self, quad):
		self.quad = quad
		
	def isAlive(self):
		return self.counter < len(self.points)
	
	def getPos(self, move):
		if move:
			self.counter += 1
		if self.isAlive():
			return self.points[self.counter]
		else:
			return self.points[len(self.points)-1]
	
	def get_line(self, x1, y1, x2, y2):
		points = []
		issteep = abs(y2-y1) > abs(x2-x1)
		if issteep:
			x1, y1 = y1, x1
			x2, y2 = y2, x2
		rev = False
		if x1 > x2:
			x1, x2 = x2, x1
			y1, y2 = y2, y1
			rev = True
		deltax = x2 - x1
		deltay = abs(y2-y1)
		error = int(deltax / 2)
		y = y1
		ystep = None
		if y1 < y2:
			ystep = 1
		else:
			ystep = -1
		for x in range(x1, x2 + 1):
			if issteep:
				points.append((y, x))
			else:
				points.append((x, y))
			error -= deltay
			if error < 0:
				y += ystep
				error += deltax
		# Reverse the list if the coordinates were reversed
		if rev:
			points.reverse()
		return points