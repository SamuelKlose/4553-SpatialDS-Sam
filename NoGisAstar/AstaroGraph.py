"""
@author - Samuel Klose
@date -  12/6/2015
@description - This program modifies the given astar program to add additional functionality
preloads a scenario
double click to start
middle mouse button a start and end location to create an obstacle line between the points
ctrl + left click to move start positoin
alt + left click to move end position
shift + left click to create horizontal line of obstacles
left click to create obstacle
right click to cycle through tile types
light blue squares are ice and have a lower move cost
dark blue squares are water and have a higher move cost
white squares a move cost in between
@resources - I used the code given on github
"""
from math import sqrt
from itertools import product
import pantograph
import sys
import time

"""
START Astar Implementation
Obtained from github and pulled out of its own file `astar.py` to
make it a little easier to incorporate pantograph
"""
class AStar():
	def __init__(self, graph):
		self.graph = graph
		self.moves = []

	def heuristic(self, node, start, end):
		raise NotImplementedError

	def search(self, start, end):
		openset = set()
		closedset = set()
		current = start
		openset.add(current)  #lets add the start coordinate
		buildingpath = []
		buildingpath.append(current)
		while openset:  #openset still has items in it
			current = min(openset, key=lambda o:o.g + o.h)  #
			buildingpath.append(current)
			if current == end:
				path = []
				while current.parent:
					path.append(current)
					current = current.parent
				path.append(current)
				return path[::-1], buildingpath  #reverse the path
			openset.remove(current)
			closedset.add(current)
			for node in self.graph[current]:
				if node in closedset:
					continue
				if node in openset:
					new_g = current.g + current.move_cost(node)
					if node.g > new_g:
						node.g = new_g
						node.parent = current
						buildingpath.append(node)
				else:
					node.g = current.g + current.move_cost(node)
					node.h = self.heuristic(node, start, end)
					node.parent = current
					openset.add(node)
					
		return None

class AStarNode(object):
	def __init__(self):
		self.g = 0
		self.h = 0
		self.parent = None
		self.type = 'regular'

	def move_cost(self, other):
		raise NotImplementedError

class AStarGrid(AStar):
	def heuristic(self, node, start, end):
		# NOTE: this is traditionally sqrt((end.x - node.x)**2 + (end.y -
		# node.y)**2)
		# However, if you are not interested in the *actual* cost, but only
		# relative cost,
		# then the math can be simplified.
		return abs(end.x - node.x) + abs(end.y - node.y)
		#return sqrt((end.x - node.x)**2 + (end.y - node.y)**2)
class AStarGridNode(AStarNode):
	def __init__(self, x, y, type='regular'):
		self.x, self.y = x, y
		self.type = type
		super(AStarGridNode, self).__init__()

	def move_cost(self, other):
		diagonal = abs(self.x - other.x) == 1 and abs(self.y - other.y) == 1
		if diagonal: 
			return sys.getsizeof(int)
		elif other.type == 'ice':
			return 1
		elif other.type == 'water':
		   return 50
		else:
		   return 25

	def __repr__(self):
		return '(%d %d %s)' % (self.x, self.y, self.type)
	
	"""
	Creates a graph used for searching in astar
	"""
def make_graph(mapinfo):
	nodes = [[AStarGridNode(x, y, 'regular') for y in range(mapinfo['height'])] for x in range(mapinfo['width'])]

	graph = {}
	for x, y in product(range(mapinfo['width']), range(mapinfo['height'])):
		if [x, y] in mapinfo['iceTiles']:
			node = (nodes[x][y], 'ice')
		elif [x, y] in mapinfo['waterTiles']:
			node = (nodes[x][y], 'water')
		else:
			node = (nodes[x][y], 'regular')
		
		graph[node[0]] = []
		
		for i, j in product([-1, 0, 1], [-1, 0, 1]):
			if not (0 <= x + i < mapinfo['width']): continue
			if not (0 <= y + j < mapinfo['height']): continue
			if [x + i,y + j] in mapinfo['obstacle']: continue
			if [x + i, y + j] in mapinfo['iceTiles']:
				nodes[x + i][y + j].type = 'ice'
			if [x + i, y + j] in mapinfo['waterTiles']:
				nodes[x + i][y + j].type = 'water'
			graph[[nodes[x][y]][0]].append(nodes[x + i][y + j])

	return graph, nodes

	"""
	Creates a graph used for making a line between 2 points
	"""
def make_graph_for_obstacles(mapinfo):
	nodes = [[AStarGridNode(x, y, 'regular') for y in range(mapinfo['height'])] for x in range(mapinfo['width'])]

	graph = {}
	for x, y in product(range(mapinfo['width']), range(mapinfo['height'])):
		node = (nodes[x][y], 'regular')
		
		graph[node[0]] = []
		
		for i, j in product([-1, 0, 1], [-1, 0, 1]):
			if not (0 <= x + i < mapinfo['width']): continue
			if not (0 <= y + j < mapinfo['height']): continue
			graph[[nodes[x][y]][0]].append(nodes[x + i][y + j])

	return graph, nodes

"""
END Astar Implementation
"""

"""
A pantograph / Astar extension to output the results of the algorithm
visually.
"""
class DrawAstar(pantograph.PantographHandler):

	"""
	Our constructor
	"""
	def setup(self):
		self.block = 10                 # grid size on the browser
		self.obstacles = []             # cells in the grid to block astar
		self.adjObstacles = []          # adjusted for astar because each grid cell is "block" times big.
		self.regularTiles = []          # normal tiles
		self.iceTiles = []              # ice tiles with a lower move cost
		self.waterTiles = []            # water tiles with a higher move cost
		self.createPath = []            # used for discovering path
		self.finalPath = []             # final path to draw one at a time
		self.obstaclePath = []          # create a path of obstacles between 2 points
		self.startCoord = None          # Start Cell
		self.finishCoord = None         # Finish Cell
		self.pathFound = False          # Set path found to false so we don't try to draw it right off
		self.path = None                # Holds the found path (if any) so we can draw it.
		self.buildingpath = None
		self.point1 = None
		self.point2 = None
		self.setUpGrid()
		self.discovercounter = 0
		self.pathcounter = 0

		self.setupScenario()

		print self.width / self.block     #Debugging values
		print self.height / self.block

	"""
	Sets up a preloaded scenario for testing
	"""
	def setupScenario(self):
		self.addStart(5 * self.block, 10 * self.block)
		self.addFinish(25 * self.block, 25 * self.block)
		self.toggleTileType(5 * self.block, 9 * self.block)
		self.toggleTileType(5 * self.block, 8 * self.block)
		self.toggleTileType(5 * self.block, 7 * self.block)
		self.toggleTileType(6 * self.block, 7 * self.block)
		self.toggleTileType(7 * self.block, 7 * self.block)
		self.toggleTileType(8 * self.block, 7 * self.block)
		self.toggleTileType(8 * self.block, 8 * self.block)
		self.toggleTileType(8 * self.block, 9 * self.block)
		self.toggleTileType(8 * self.block, 10 * self.block)
		self.toggleTileType(8 * self.block, 11 * self.block)
		self.toggleTileType(8 * self.block, 12 * self.block)
		self.toggleTileType(8 * self.block, 13 * self.block)
		self.toggleTileType(7 * self.block, 13 * self.block)
		self.toggleTileType(6 * self.block, 13 * self.block)
		self.toggleTileType(5 * self.block, 13 * self.block)
		self.toggleTileType(4 * self.block, 13 * self.block)
		self.toggleTileType(3 * self.block, 13 * self.block)
		self.toggleTileType(4 * self.block, 15 * self.block)
		self.toggleTileType(5 * self.block, 15 * self.block)
		self.toggleTileType(6 * self.block, 15 * self.block)
		self.toggleTileType(7 * self.block, 15 * self.block)
		self.toggleTileType(8 * self.block, 15 * self.block)
		self.toggleTileType(9 * self.block, 15 * self.block)
		self.toggleTileType(10 * self.block, 15 * self.block)
		self.toggleTileType(11 * self.block, 15 * self.block)
		self.toggleTileType(12 * self.block, 15 * self.block)
		self.toggleTileType(13 * self.block, 15 * self.block)
		self.toggleTileType(14 * self.block, 15 * self.block)
		self.toggleTileType(15 * self.block, 15 * self.block)
		self.toggleTileType(4 * self.block, 15 * self.block)
		self.toggleTileType(5 * self.block, 15 * self.block)
		self.toggleTileType(6 * self.block, 15 * self.block)
		self.toggleTileType(7 * self.block, 15 * self.block)
		self.toggleTileType(8 * self.block, 15 * self.block)
		self.toggleTileType(9 * self.block, 15 * self.block)
		self.toggleTileType(10 * self.block, 15 * self.block)
		self.toggleTileType(11 * self.block, 15 * self.block)
		self.toggleTileType(12 * self.block, 15 * self.block)
		self.toggleTileType(13 * self.block, 15 * self.block)
		self.toggleTileType(14 * self.block, 15 * self.block)
		self.toggleTileType(15 * self.block, 15 * self.block)
		self.toggleObstacle(3 * self.block,14 * self.block)
		self.toggleObstacle(14 * self.block,24 * self.block)
		self.toggleObstacle(15 * self.block,20 * self.block)
		self.drawLine(3 * self.block, 14 * self.block)
		self.drawLine(14 * self.block, 24 * self.block)
		self.drawLine(15 * self.block, 20 * self.block)

	"""
	Start the Astar pathfind algorithm aka RELEASE THE KRAKEN!
	"""
	def startAstar(self):

		# Initialize Astar
		adjustedIceTiles = []
		adjustedWaterTiles = []
		
		for i in self.iceTiles:
			adjustedIceTiles.append([i[0] / self.block, i[1] / self.block])

		for i in self.waterTiles:
			adjustedWaterTiles.append([i[0] / self.block, i[1] / self.block])

		graph, nodes = make_graph({"width": self.width / self.block, "height": self.height / self.block, "obstacle": self.adjObstacles, "iceTiles": adjustedIceTiles, "waterTiles": adjustedWaterTiles})

		# Build the graph
		paths = AStarGrid(graph)

		# Pull start and finish cell coordinates off the grid
		startx,starty = self.startCoord
		finishx,finishy = self.finishCoord

		# Divide block size into the coordinates to
		# bring them back to the original state
		startx /= self.block
		starty /= self.block
		finishx /= self.block
		finishy /= self.block

		# Grab the start and end nodes (copies) from the graph
		start, end = nodes[startx][starty], nodes[finishx][finishy]

		# Start searching
		path, buildingpath = paths.search(start, end)
		self.buildingpath = buildingpath
		if path is None:
			print "No path found"
		else:
			print "Path found:", path
			self.path = path
			self.pathFound = True


	#def addElement(self.element,x1,y1,x2,y2)

	"""
	Continous calls to redraw necessary items
	"""
	def update(self):
		self.clear_rect(0, 0, self.width, self.height)
		self.drawGrid()
		if self.buildingpath:
			if self.discovercounter < len(self.buildingpath):
				self.discoverPath(self.discovercounter)
				self.discovercounter += 1
		if self.createPath:
			for i in self.createPath:
				self.fill_rect(i[0], i[1], self.block, self.block, "#AAA")

		self.drawObstacles()
		self.drawStartFinish()
		if self.buildingpath and self.discovercounter == len(self.buildingpath):
			if self.pathFound:
				if self.pathcounter < len(self.path):
					self.drawPath(self.pathcounter)
					self.pathcounter += 1
				for i in self.finalPath:
					self.fill_rect(i[0], i[1], self.block, self.block, "F05")

	"""
	Draw the found path
	"""
	def drawPath(self, count):
		# Blow up the cordinates pulled from Astar to fit our grid
		x,y = self.adjustCoords(self.path[count].x * self.block,self.path[count].y * self.block)
		self.finalPath.append([x,y])

	def discoverPath(self, count):
		# Blow up the cordinates pulled from Astar to fit our grid
		x,y = self.adjustCoords(self.buildingpath[count].x * self.block,self.buildingpath[count].y * self.block)
		self.createPath.append([x, y])
		
	"""
	Draw the background grid
	"""
	def drawGrid(self):
		for i in range(0,self.width,self.block):
		   self.draw_line(i, 0, i, self.height, "#AAAAAA")
		   self.draw_line(0, i, self.width, i , "#AAAAAA")


	"""
	Toggle means that it draws an obstacle, unless you click on
	an already "obstacled" cell, then it turns off
	"""
	def toggleObstacle(self,x,y):
		gridX = x
		gridY = y
		adjX = gridX / self.block
		adjY = gridY / self.block
		if [gridX,gridY] not in self.obstacles:
			self.obstacles.append([gridX,gridY])
			self.adjObstacles.append([adjX,adjY])
		else:
			self.obstacles.remove([gridX,gridY])
			self.adjObstacles.remove([adjX,adjY])
		#print self.obstacles
		#print self.adjObstacles

	"""
	Draws the obstacles and different types of tiles.
	"""
	def drawObstacles(self):
		for r in self.obstacles:
			self.fill_rect(r[0], r[1], self.block , self.block , "#000")
		for r in self.iceTiles:
			self.fill_rect(r[0], r[1], self.block, self.block, "#0FF")
		for r in self.waterTiles:
			self.fill_rect(r[0], r[1], self.block, self.block, "#05F")

	"""
	Change the current tile between regular, ice, and water tiles. Cycles through each time called
	"""
	def toggleTileType(self,x,y):
		gridX = x
		gridY = y
		if [gridX,gridY] not in self.regularTiles and [gridX, gridY] in self.waterTiles:
			self.regularTiles.append([gridX,gridY])
			self.waterTiles.remove([gridX, gridY])
		elif [gridX,gridY] not in self.iceTiles and [gridX, gridY] in self.regularTiles:
			self.iceTiles.append([gridX,gridY])
			self.regularTiles.remove([gridX, gridY])
		elif [gridX,gridY] not in self.waterTiles and [gridX, gridY] in self.iceTiles:
			self.waterTiles.append([gridX,gridY])
			self.iceTiles.remove([gridX, gridY])
	"""
	Draws the start and finish coordinates
	"""
	def drawStartFinish(self):
		if self.startCoord:
			x,y = self.startCoord
			self.fill_rect(x, y, self.block , self.block , "#0F0")

		if self.finishCoord:
			x,y = self.finishCoord
			self.fill_rect(x, y, self.block , self.block , "#F00")

	"""
	Event handlers for the mouse down event.
	LeftClick = add obstacle
	RightClick = change tile type
	Ctrl + LeftClick = place start location
	Alt + LeftClick = place end location
	Shift + LeftClick = Draw a line obstacle
	"""
	def on_mouse_down(self,e):
		print e
		#Alt key gets you bigger blocks
		x,y = self.adjustCoords(e.x,e.y)

		if not e.alt_key and not e.ctrl_key and not e.meta_key and e.button == 0:
			self.toggleObstacle(x,y)

		if e.button == 2:
			self.toggleTileType(x, y)
		if e.button == 1:
			if self.point1 == None:
				self.point1 = [x,y]
				self.toggleObstacle(x, y)
			elif self.point2 == None:
				self.point2 = [x,y]
				self.toggleObstacle(x, y)
				self.drawLinePoints()
		if e.alt_key:
			self.addFinish(x,y)
		elif e.ctrl_key:
			self.addStart(x,y)
		elif e.shift_key:
			self.drawLine(x,y)

	"""
	Create obstacles between 2 points
	"""
	def drawLinePoints(self):
		graph, nodes = make_graph_for_obstacles({"width": self.width / self.block, "height": self.height / self.block})

		# Build the graph
		paths = AStarGrid(graph)

		# Pull start and finish cell coordinates off the grid
		startx,starty = self.point1
		finishx,finishy = self.point2

		# Divide block size into the coordinates to
		# bring them back to the original state
		startx /= self.block
		starty /= self.block
		finishx /= self.block
		finishy /= self.block

		# Grab the start and end nodes (copies) from the graph
		start, end = nodes[startx][starty], nodes[finishx][finishy]

		# Start searching
		path, buildingpath = paths.search(start, end)
		isObstaclePath = False
		if path is None:
			print "No path found"
		else:
			print "Path found:", path
			self.obstaclePath = path
			isObstaclePath = True

		if isObstaclePath:
			for i in self.obstaclePath:
				gridX = i.x
				gridY = i.y
		
				if [gridX,gridY] not in self.obstacles:
					self.obstacles.append([gridX * self.block, gridY * self.block])
					self.adjObstacles.append([gridX,gridY])
				
		self.point1 = None
		self.point2 = None
		self.obstaclePath = []

	"""
	Key press handlers
	"""
	def on_key_down(self,e):
		print e
		if e.key_code == 32: # S key
			self.refreshWorld()
		if e.key_code == 83: # S key
			pass
		elif e.key_code == 70: # F key
			pass

	"""
	This simply draws a complete line on the x axis (minus 1 cell).
	"""
	def drawLine(self,x,y):
		for i in range(0,self.width,self.block):
			print i,y
			self.toggleObstacle(i,y)
	
	"""
	This initializes the grid with all regular cells
	"""
	def setUpGrid(self):
		for i in range(0, self.width, self.block):
			for j in range(0, self.height, self.block):
				self.regularTiles.append([i,j])

	"""
	Double Click starts the path finding.
	"""
	def on_dbl_click(self,e):
		print e
		self.startAstar()

	"""
	Space bar erases the path, so you can go again
	"""
	def refreshWorld(self):
		self.pathFound = False
		self.path = []

	"""
	Adds the start cell
	"""
	def addStart(self,x,y):
		self.fill_rect(x, y, self.block , self.block , "#F00")
		self.startCoord = (x,y)

	"""
	Adds the finish cell
	"""
	def addFinish(self,x,y):
		self.fill_rect(x, y, self.block , self.block , "#0F0")
		self.finishCoord = (x,y)

	"""
	Fattens the coords to fit grid.
	"""
	def adjustCoords(self,x,y):
		"""adjust the coords to fit our grid"""
		x = (x / self.block) * self.block
		y = (y / self.block) * self.block
		return (x,y)
"""
Main Driver!!!
"""
if __name__ == '__main__':
	app = pantograph.SimplePantographApplication(DrawAstar)
	app.run()
