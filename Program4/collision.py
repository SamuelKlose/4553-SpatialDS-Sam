"""
@author - Samuel Klose
@date -  10/18/2015
@description - This program uses a quadtree for collision detection of an n number of balls.
When the balls collide they change color, grow in size, and change direction. None of the balls go out of bounds
of the screen. Uses python 2.7. Requires pantograph and numpy installed. After running copy go to the localhost by placing
http://127.0.0.1:8080/ in the browser in order to view the animation. The quadtree bounding boxes are shown behind the balls
as well to see it splitting in real time. Currently set to split when there are 2 balls in a node with a maximum level of division of 4.
Click on the screen to stop movement. Press the up arrow to increase ball speed, down to lower it.
@resources - I found code and methods at http://www.learnpygame.com, http://stackoverflow.com, http://gamedev.stackexchange.com/
http://gamedevelopment.tutsplus.com/tutorials/quick-tip-use-quadtrees-to-detect-likely-collisions-in-2d-space--gamedev-374, and
the quadtree code Dr. Griffin pushed onto his github

"""

import sys
import math
import random
import pantograph
import numpy as np
import time

class Point:
	"""A point identified by (x,y) coordinates.
	supports: +, -, *, /, str, repr
	length  -- calculate length of vector to point from origin
	distance_to  -- calculate distance between two points
	as_tuple  -- construct tuple (x,y)
	clone  -- construct a duplicate
	integerize  -- convert x & y to integers
	floatize  -- convert x & y to floats
	move_to  -- reset x & y
	slide  -- move (in place) +dx, +dy, as spec'd by point
	slide_xy  -- move (in place) +dx, +dy
	rotate  -- rotate around the origin
	rotate_about  -- rotate around another point
	"""

	"""
	@function __init__
	Function description: Initializes a points at given coordinates with a random direction
	Modified from code given for assignment using randomwalk as suggested.
	@param  {double} - x: x coordinate
	@param  {double} - y: y coordinate
	@returns{void}:   - return void
	"""
	def __init__(self, x=0.0, y=0.0):
		self.x = x
		self.y = y

	"""
	@function __add__
	Function description: Adds this point to another points
	From polygon code given in assignment
	@param  {double} - x: x coordinate
	@param  {double} - y: y coordinate
	@returns{Point()}:   - return new point
	"""

	def __add__(self, p):
		"""Point(x1+x2, y1+y2)"""
		return Point(self.x + p.x, self.y + p.y)

	"""
	@function __sub__
	Function description: Subtracts this point with another points
	From polygon code given in assignment
	@param  {double} - x: x coordinate
	@param  {double} - y: y coordinate
	@returns{Point()}:   - return new point
	"""
	def __sub__(self, p):
		"""Point(x1-x2, y1-y2)"""
		return Point(self.x - p.x, self.y - p.y)

	"""
	@function __mul__
	Function description: Multiplies this point with another points
	From polygon code given in assignment
	@param  {double} - x: x coordinate
	@param  {double} - y: y coordinate
	@returns{Point()}:   - return new point
	"""
	def __mul__(self, scalar):
		"""Point(x1*x2, y1*y2)"""
		return Point(self.x * scalar, self.y * scalar)

	"""
	@function __div__
	Function description: Divides this point with another points
	From polygon code given in assignment
	@param  {double} - x: x coordinate
	@param  {double} - y: y coordinate
	@returns{Point()}:   - return new point
	"""
	def __div__(self, scalar):
		"""Point(x1/x2, y1/y2)"""
		return Point(self.x / scalar, self.y / scalar)

	"""
	@function __str__
	Function description: Prints a representation of point
	From polygon code given in assignment
	@returns{void}:   - prints the point
	"""
	def __str__(self):
		return "(%s, %s)" % (self.x, self.y)

	"""
	@function __repr__
	Function description: Prints a representation of point
	From polygon code given in assignment
	@returns{void}:   - prints the point
	"""
	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

	"""
	@function length
	Function description: Returns the length of the point
	From polygon code given in assignment
	@returns{double}:   - return length of point
	"""
	def length(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)

	"""
	@function distance_to
	Function description: Gets the distance between two points
	From polygon code given in assignment
	@returns{double}:   - return distance to point
	"""
	def distance_to(self, p):
		"""Calculate the distance between two points."""
		return (self - p).length()

	"""
	@function as_tuple
	Function description: Gets the x, y coords
	From polygon code given in assignment
	@returns{tuple}:   - return a tuple of the xy coords
	"""
	def as_tuple(self):
		"""(x, y)"""
		return (self.x, self.y)

	"""
	@function clone
	Function description: Returns a full copy of this point
	From polygon code given in assignment
	@returns{Point()}:   - return this point
	"""
	def clone(self):
		"""Return a full copy of this point."""
		return Point(self.x, self.y)

	"""
	@function integerize
	Function description: Converts coordinates to integers
	From polygon code given in assignment
	@returns{void}:   - coordinates set to integers
	"""
	def integerize(self):
		"""Convert co-ordinate values to integers."""
		self.x = int(self.x)
		self.y = int(self.y)

	"""
	@function floatize
	Function description: Converts the coordinates to floats
	From polygon code given in assignment
	@returns{void}:   - coordinates set to floats
	"""
	def floatize(self):
		"""Convert co-ordinate values to floats."""
		self.x = float(self.x)
		self.y = float(self.y)
	
	"""
	@function move_to
	Function description: Moves point to new location
	From polygon code given in assignment
	@param  {double} - x: x coordinate
	@param  {double} - y: y coordinate
	@returns{void}:   - point moved to new coordinates
	"""
	def move_to(self, x, y):
		"""Reset x & y coordinates."""
		self.x = x
		self.y = y
	
	"""
	@function slide
	Function description: Moves point to new coords
	From polygon code given in assignment
	@param  {point} - x: moves point to new (x+dx, y+dy)
	@returns{void}:   - coordinates set to point coords
	"""
	def slide(self, p):
		'''Move to new (x+dx,y+dy).
		Can anyone think up a better name for this function?
		slide? shift? delta? move_by?
		'''
		self.x = self.x + p.x
		self.y = self.y + p.y
	
	"""
	@function slide_xy
	Function description: Moves the point by the xy coords
	From polygon code given in assignment
	@param  {double} - x: x coordinate
	@param  {double} - y: y coordinate
	@returns{void}:   - moves the point by xy
	"""
	def slide_xy(self, dx, dy):
		'''Move to new (x+dx,y+dy).
		Can anyone think up a better name for this function?
		slide? shift? delta? move_by?
		'''
		self.x = self.x + dx
		self.y = self.y + dy

	"""
	@function rotate
	Function description: Rotate counter-clockwise by rad radians
	From polygon code given in assignment
	@param  {double} - rad: radians to rotate by
	@returns{Point()}:   - returns rotated point
	"""
	def rotate(self, rad):
		"""Rotate counter-clockwise by rad radians.
		Positive y goes *up,* as in traditional mathematics.
		Interestingly, you can use this in y-down computer graphics, if
		you just remember that it turns clockwise, rather than
		counter-clockwise.
		The new position is returned as a new Point.
		"""
		s, c = [f(rad) for f in (math.sin, math.cos)]
		x, y = (c * self.x - s * self.y, s * self.x + c * self.y)
		return Point(x,y)

	"""
	@function rotate_about
	Function description: Rotates around point p by theta degrees
	From polygon code given in assignment
	@param  {double} - p: point to rotate about
	@param  {double} - theta: rotate theta degrees
	@returns{Point()}:   - returns point rotated around p by theta
	"""
	def rotate_about(self, p, theta):
		"""Rotate counter-clockwise around a point, by theta degrees.
		Positive y goes *up,* as in traditional mathematics.
		The new position is returned as a new Point.
		"""
		result = self.clone()
		result.slide(-p.x, -p.y)
		result.rotate(theta)
		result.slide(p.x, p.y)
		return result

class Rectangle:

	"""
	A rectangle identified by two points.
	The rectangle stores left, top, right, and bottom values.
	Coordinates are based on screen coordinates.
	origin                               top
	   +-----> x increases                |
	   |                           left  -+-  right
	   v                                  |
	y increases                         bottom
	set_points  -- reset rectangle coordinates
	contains  -- is a point inside?
	overlaps  -- does a rectangle overlap?
	top_left  -- get top-left corner
	bottom_right  -- get bottom-right corner
	expanded_by  -- grow (or shrink)
	"""

	"""
	@function __init__
	Function description: Initializes a bounding rectangle from two points
	by calling set_points()
	From code given for assignment
	@returns{void}:   - bounding rectangle is created
	"""
	def __init__(self, pt1, pt2):
		"""Initialize a rectangle from two points."""
		self.set_points(pt1, pt2)
	
	"""
	@function set_points
	Function description: Sets the dimensions of the rectangle based
	on the given points
	From code given for assignment
	@param {Point()} - pt1: Used to determine boundaries of rectangle
	@param {Point()} - pt2: Used to determine boundaries of rectangle
	@returns{void}:   - bounding rectangle dimensions are set
	"""
	def set_points(self, pt1, pt2):
		"""Reset the rectangle coordinates."""
		(x1, y1) = pt1.as_tuple()
		(x2, y2) = pt2.as_tuple()
		self.left = min(x1, x2)
		self.top = min(y1, y2)
		self.right = max(x1, x2)
		self.bottom = max(y1, y2)
		self.width = self.right - self.left
		self.height = self.bottom - self.top
	
	"""
	@function contains
	Function description: Return true if a point is inside the rectangle
	From code given for assignment
	@param {Point()} - pt: point to see if is in rectangle
	@returns{boolean}:   - True if point is inside the rectangle
	"""
	def contains(self, pt):
		"""Return true if a point is inside the rectangle."""
		return (self.top_left().x <= pt.x and pt.x <= self.bottom_right().x and self.top_left().y <= pt.y and pt.y <= self.bottom_right().y)

	"""
	@function overlaps
	Function description: Returns true if a rectangle overlaps this rectangle
	From code given for assignment
	@param {Point()} - other: Other rectangle to check overlap for
	@returns{Boolean}:   - True if rectangles overlap
	"""
	def overlaps(self, other):
		"""Return true if a rectangle overlaps this rectangle."""
		return (self.right > other.left and self.left < other.right and self.top < other.bottom and self.bottom > other.top)
	
	"""
	Return true if a rect is inside this rectangle.
	"""
	def encompasses(self, other):
		return  (self.left <= other.left and self.right >= other.right and self.top <= other.top and self.bottom >= other.bottom)

	"""
	@function top_left
	Function description: Returns top left point of rectangle
	Using code from assignment
	@returns{Point()}:   - Returns top left point of rectangle
	"""
	def top_left(self):
		"""Return the top-left corner as a Point."""
		return Point(self.left, self.top)

	"""
	@function top_right
	Function description: Returns top right point of rectangle
	Using code from assignment
	@returns{Point()}:   - Returns right left point of rectangle
	"""
	def top_right(self):
		"""Return the top-right corner as a Point."""
		return Point(self.right, self.top)

	"""
	@function bottom_left
	Function description: Returns bottom left point of rectangle
	Using code from assignment
	@returns{Point()}:   - Returns bottom left point of rectangle
	"""
	def bottom_left(self):
		"""Return the bottom-left corner as a Point."""
		return Point(self.left, self.bot)

	"""
	@function bottom_right
	Function description: Returns bottom right point of rectangle
	Using code from assignment
	@returns{Point()}:   - Returns bottom right point of rectangle
	"""
	def bottom_right(self):
		"""Return the bottom-right corner as a Point."""
		return Point(self.right, self.bottom)

	"""
	@function expanded_by
	Function description: Creates slightly larger rectangle
	Using code from assignment
	@param{int} - n : number to enlarge rectangle by
	@returns{Point()}:   - Returns larger rectangle
	"""
	def expanded_by(self, n):
		"""Return a rectangle with extended borders.
		Create a new rectangle that is wider and taller than the
		immediate one. All sides are extended by "n" points.
		"""
		p1 = Point(self.left - n, self.top - n)
		p2 = Point(self.right + n, self.bottom + n)
		return Rectangle(p1, p2)

	"""
	@function get_centroid
	Function description: Returns centroid of rectangle
	http://www.engineeringintro.com/mechanics-of-structures/centre-of-gravity/centroid-of-rectangle/
	@returns{Point()}:   - Returns center
	"""
	def get_centroid(self):
		tempX = (self.left + self.width) / 2
		tempY = (self.top + self.height) / 2
		return Point(tempX, tempY)

	"""
	@function get_collision_side
	Function description: Determines which side of bounding box was hit in collision
	http://gamedev.stackexchange.com/questions/24078/which-side-was-hit
	@param {Rectangle} - other: Other rectangle to check collision with
	@returns{string}:   - Returns side that was hit
	"""
	def get_collision_side(self, other):
		wy = (self.width + other.width) * (self.get_centroid().y - other.get_centroid().y)
		hx = (self.height + other.height) * (self.get_centroid().x - other.get_centroid().x)
		if wy > hx:
			if wy > -hx:
				return "Top"
			else:
				return "Left"
		else:
			if wy > -hx:
				return "Right"
			else:
				return "Bottom"

	"""
	@function __str__
	Function description: Prints out representation of the rectangle
	From code given for assignment
	@returns{string}:   - Prints out representation of itself
	"""
	def __str__(self):
		return "<Rect (%s,%s)-(%s,%s)>" % (self.left,self.top, self.right,self.bottom)

	"""
	@function __repr__
	Function description: Prints out representation of the rectangle
	From code given for assignment
	@returns{string}:   - Prints out representation of itself
	"""
	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, Point(self.left, self.top), Point(self.right, self.bottom))

class PointQuadTree(object):

	"""
	@function get_collision_side
	Function description: Determines which side of bounding box was hit in collision
	
	Found help at http://www.learnpygame.com/2015/03/implementing-quadtree-collision-system.html

	@param {Rectangle} - bbox: the bounding box of the current quadtree level
	@param {int} - maxPoints: The maximum number of points a node can hold before subdividing
	@param {list} - points: The list of points that are to be handled by the quadtree
	@param {int} - level: current level of subdivision
	@param {int} - maxLevel: maxLevel to subdivide nodes to
	@returns{string}:   - Returns side that was hit
	"""
	def __init__(self, bbox, maxPoints, points=[], level=0, maxLevel=4):
		self.northEast = None
		self.southEast = None
		self.southWest = None
		self.northWest = None

		self.points = points
		self.bbox = bbox
		self.maxPoints = maxPoints
		self.level = level
		self.maxLevel = maxLevel

	def __str__(self):
		return "\nnorthwest: %s,\nnorthEast: %s,\nsouthWest: %s,\nsouthEast: %s,\npoints: %s,\nbbox: %s,\nmaxPoints: %s,\nparent: %s" % (self.northWest, self.northEast,self.southWest, self.southEast,self.points,self.bbox,self.maxPoints,self.level)

	"""
	@function update

	Subdivides the nodes, puts the points into the right node, recursively updates each subtree, and checks for collisions in appropriate nodes and handles them

	Found help at http://www.learnpygame.com/2015/03/implementing-quadtree-collision-system.html
	
	@returns{void} - the quadtree is updated
	"""
	def update(self):
		if len(self.points) >= self.maxPoints and self.level <= self.maxLevel:
			# If we still have spaces in the bucket array for this QuadTree node,
			#    then the point simply goes here and we're finished
			self.subdivide()
			self.subdividePoints()
			self.northEast.update()
			self.southEast.update()
			self.southWest.update()
			self.northWest.update()
		else:
			self.checkCollisionsPoints()

	"""
	@function subdivide

	Split this QuadTree node into four quadrants for NW/NE/SE/SW

	Modified from quadtree code pushed onto github
	
	@returns{void}   - Split this QuadTree node into four quadrants for NW/NE/SE/SW
	"""
	def subdivide(self):
		left = self.bbox.left
		right = self.bbox.right
		top = self.bbox.top
		bottom = self.bbox.bottom
		midX = (self.bbox.width) / 2
		midY = (self.bbox.height) / 2
		self.northEast = PointQuadTree(Rectangle(Point(left + midX, top), Point(right, top + midY)), self.maxPoints, [], self.level + 1)
		self.northWest = PointQuadTree(Rectangle(Point(left, top), Point(left + midX,top + midY)), self.maxPoints, [], self.level + 1)
		self.southWest = PointQuadTree(Rectangle(Point(left, top + midY), Point(left + midX, bottom)), self.maxPoints, [], self.level + 1)
		self.southEast = PointQuadTree(Rectangle(Point(left + midX, top + midY), Point(right, bottom)), self.maxPoints, [], self.level + 1)
	
	"""
	@function subdividePoints

	Puts the points in the quadtree into the leaf of the appropriate node

	Found help at http://www.learnpygame.com/2015/03/implementing-quadtree-collision-system.html
	
	@returns{void}   - the points are put into their appropriate sub node in the quad tree
	"""
	def subdividePoints(self):
		for point in self.points:
			if self.northEast.bbox.overlaps(point.getBBox()) or self.northEast.bbox.encompasses(point.getBBox()):
				self.northEast.addPoint(point)
			if self.northWest.bbox.overlaps(point.getBBox()) or self.northWest.bbox.encompasses(point.getBBox()):
				self.northWest.addPoint(point)
			if self.southWest.bbox.overlaps(point.getBBox()) or self.southWest.bbox.encompasses(point.getBBox()):
				self.southWest.addPoint(point)
			if self.southEast.bbox.overlaps(point.getBBox()) or self.southEast.bbox.encompasses(point.getBBox()):
				self.southEast.addPoint(point)
		
	"""
	@function searchBox

	Return an array of all points within this QuadTree and its child nodes that fall
	within the specified bounding box

	Taken from quadtree implementation pushed onto github

	@param  {Rectangle} - bbox: the bounding box to search in
	
	@returns{list}   - a list of all the points in the bounding box
	 
	"""
	def searchBox(self, bbox):
		results = []

		if self.bbox.overlaps(bbox) or self.bbox.encompasses(bbox):
			# Test each point that falls within the current QuadTree node
			for p in self.points:
				# Test each point stored in this QuadTree node in turn, adding
				# to the results array
				#    if it falls within the bounding box
				if self.bbox.contains(p):
					results.append((bbox, self.level))


			# If we have child QuadTree nodes....
			if (not self.northWest == None):
				# ...  search each child node in turn, merging with any
				# existing results
				results = results + self.northEast.searchBox(self.bbox)
				results = results + self.northWest.searchBox(self.bbox)
				results = results + self.southWest.searchBox(self.bbox)
				results = results + self.southEast.searchBox(self.bbox)

		return results

	"""
	@function searchNeighbors

	Returns the containers points that are in the same container as another point

	Taken from quadtree implementation pushed onto github

	@param  {Point} - point: the point whose container should be searched
	
	@returns{list}   - a list of all the points in the same container as point
	"""
	def searchNeighbors(self, point):
		#If its not a point (its a bounding rectangle)
		if not hasattr(point, 'x'):
			return []

		results = []

		if self.bbox.containsPoint(point):
			# Test each point that falls within the current QuadTree node
			for p in self.points:
				# Test each point stored in this QuadTree node in turn, adding
				# to the results array
				#    if it falls within the bounding box
				if self.bbox.containsPoint(p):
					results.append(p)


			# If we have child QuadTree nodes....
			if (not self.northWest == None):
				# ...  search each child node in turn, merging with any
				# existing results
				results = results + self.northEast.searchNeighbors(point)
				results = results + self.northWest.searchNeighbors(point)
				results = results + self.southWest.searchNeighbors(point)
				results = results + self.southEast.searchNeighbors(point)

		return results

	"""
	@function getBBoxes

	Gets all of the bounding boxes of the quadtree

	Taken from quadtree implementation pushed onto github
	
	@returns{list} -bboxes: a list of all of the bounding boxes in the quadtree
	"""
	def getBBoxes(self):
		bboxes = []

		bboxes.append(self.bbox)

		if (not self.northWest == None):
			# ...  search each child node in turn, merging with any existing
			# results
			bboxes = bboxes + self.northEast.getBBoxes()
			bboxes = bboxes + self.northWest.getBBoxes()
			bboxes = bboxes + self.southWest.getBBoxes()
			bboxes = bboxes + self.southEast.getBBoxes()

		return bboxes

	"""
	@function checkCollisionsPoints

	Checks all the points in the current quadtree node for collisions then handles the collision

	Found help at http://www.learnpygame.com/2015/03/implementing-quadtree-collision-system.html
	
	@returns{void}   - collisions in the current node are found and handled
	"""
	def checkCollisionsPoints(self):
		for i, particle in enumerate(self.points):
			for particle2 in self.points[i + 1:]:
				if (particle.collides(particle2)):
					particle.handleCollision(particle2)
	
	
	"""
	@function addPoint

	Adds a point to the quadtree

	Found help at http://www.learnpygame.com/2015/03/implementing-quadtree-collision-system.html

	@param  {Point} - point: the point to add into the quadtree
	 
	@returns{void}   - a point is added to the quadtree
	"""
	def addPoint(self, point):
		self.points.append(point)
				

"""
A vector can be determined from a single point when basing
it from the origin (0,0), but I'm going to assume 2 points.
Example:
	AB = Vector(Point(3,4),Point(6,7))
or if you want to use the origin
	AB = Vector(Point(0,0),Point(8,4))
"""
class Vector(object):
	"""
	@function __init__

	Initializes the variables of a vector object

	Taken from quadtree implementation pushed onto github

	@param  {Point} - p1: the first point in the vector
	@param  {Point} - p2: the second point in the vector
	
	@returns{void}   - the vector object is initialized
	"""
	def __init__(self, p1, p2):
		assert not p1 == None
		assert not p2 == None
		self.p1 = p1
		self.p2 = p2
		self.v = [self.p1.x - self.p2.x, self.p1.y - self.p2.y]
		self.a, self.b = self.v

	"""
	@function __str__

	Represents the data in a vector as a string

	Taken from quadtree implementation pushed onto github

	@returns{string}   - returns a a string representation of a vector
	"""
	def _str__(self):
		return "[\n p1: %s,\n p2: %s,\n vector: %s,\n a: %s,\n b: %s\n]" % (self.p1, self.p2, self.v,self.a,self.b)

	"""
	@function __repr__

	Represents the data in a vector as a string

	Taken from quadtree implementation pushed onto github

	@returns{string}   - returns a a string representation of a vector
	"""
	def __repr__(self):
		return "[\n p1: %s,\n p2: %s,\n vector: %s,\n a: %s,\n b: %s\n]" % (self.p1, self.p2, self.v,self.a,self.b)


class VectorOps(object):
	"""
	@function __init__

	Initializes the variables of a vectorOps object
	Taken from quadtree implementation pushed onto github

	@param  {Point} - p1: the first point in the vectorOps 
	@param  {Point} - p2: the second point in the vectorOps
	@returns{void}   - the vectorOps object is initialized
	"""
	def __init__(self,p1=None, p2=None, velocity=1):
		self.p1 = p1
		self.p2 = p2
		self.dx = 0
		self.dy = 0
		if not self.p1 == None and not self.p2 == None:
			self.v = Vector(p1,p2)
			self.velocity = velocity
			self.magnitude = self._magnitude()
			self.bearing = self._bearing()
			self.step = self._step()
		else:
			self.v = None
			self.velocity = None
			self.bearing = None
			self.magnitude = None

	"""
	@function _bearing

	Calculate the bearing (in radians) between p1 and p2

	Taken from quadtree implementation pushed onto github

	@returns{double}   - returns the bearing of the vector
	"""
	def _bearing(self):
		dx = self.p2.x - self.p1.x
		dy = self.p2.y - self.p1.y
		rads = math.atan2(-dy,dx)
		return rads % 2 * math.pi         # In radians
		#degs = degrees(rads)
	"""
	@function _magnitude

	A vector by itself can have a magnitude when basing it on the origin (0,0),
	but in this context we want to calculate magnitude (length) based on another
	point (converted to a vector).

	Taken from quadtree implementation pushed onto github

	@returns{double}   - returns the magnitude of the vector
	
	"""
	def _magnitude(self):
		assert not self.v == None
		return math.sqrt((self.v.a ** 2) + (self.v.b ** 2))

	"""
	@function _yInBounds

	Create the step factor between p1 and p2 to allow a point to
	move toward p2 at some interval based on velocity. Greater velocity
	means bigger steps (less granular).

	Taken from quadtree implementation pushed onto github

	@param  {Bounds} - bounds: essentially a bounding box
	@param {double} - y: the y coordinate of the ball to check if in bounds
	@returns{boolean}   - returns True if in bounds, false otherwise
	"""
	def _step(self):
		cosa = math.sin(self.bearing)
		cosb = math.cos(self.bearing)
		self.dx = cosa * self.velocity
		self.dy = cosb * self.velocity
		return [cosa * self.velocity, cosb * self.velocity]

	"""
	@function __str__

	Represents the data in a vectorOps as a string

	Taken from quadtree implementation pushed onto github

	@returns{string}   - returns a a string representation of a vectorOps
	"""
	def __str__(self):
		return "[\n Vector: %s,\n velocity: %s,\n bearing: %s,\n magnitude: %s,\n step: %s]" % (self.v, self.velocity, self.bearing,self.magnitude,self.step)

	"""
	@function __repr__

	Represents the data in a vectorOps as a string

	Taken from quadtree implementation pushed onto github

	@returns{string}   - returns a a string representation of a vectorOps
	"""
	def __repr__(self):
		return "[\n Vector: %s,\n velocity: %s,\n bearing: %s,\n magnitude: %s,\n step: %s]" % (self.v, self.velocity, self.bearing,self.magnitude,self.step)

"""
Ball is an extension of a point. It doesn't truly "extend" the point class but it
probably should have! Having said that, I probably should extend the VectorOps class
as well.
@method: destination       -- private method to give the bearing going from p1 -> p2
@method: move              -- length in this context
@method: xInBounds         -- Helper class to check ... I'll let you guess
@method: yInBounds         -- Same as previous just vertically :)
This class is used as follows:
Given a point, p1, I want to move it somewhere, anywhere. So I do the following:
1) Create a random point somewhere else on the screen / world / board:
		distance = 100
		degrees = math.radians(random.randint(0,360))
		p2 = destination(distance,degrees)
2) Now I can calculate a vector between P1 and P2 at a given velocity (scalar value
	to adjust speed)
		velocity = random.randint(1,MaxSpeed) # 1-15 or 20
		vectorOps = VectorOps(p1,p2,velocity)
3) Finally I have a "step" (or incorrectly coined as a motion vector) that as applied to
	p1 will move it toward p2 at the given step.
		p1.x += vectorOps.dx
		p1.y += vectorOps.dy
"""
class Ball():
	"""
	@function __init__

	Initializes the variables of a ball i.e location, radius, screen bounds, colors, speed, mass, maxRadius

	Taken from quadtree implementation pushed onto github

	@param  {Point} - center: the center of the ball
	@param {double} - radius: the radius of the ball
	@param  {Bounds} - bounds: the bounds of the screen
	@param  {list} - colorlist: list holding all of the possible color combinations the ball can be
	@param  {double} - velocity: the speed the ball is moving
	@param  {mass} - mass: mass of the ball used in collision handling
	@param  {double} - maxRadius: the largest radius the ball can have(in order to stay in bounds)
	@returns{void}   - the ball is initialized
	"""
	def __init__(self, center, radius, bounds, colorList, velocity=1, mass=1, maxRadius=50):
		self.center = center
		self.radius = radius
		self.velocity = velocity
		self.x = center.x
		self.y = center.y
		self.center = center
		self.bearing = math.radians(random.randint(0,360))
		self.dest = self.destination(100,self.bearing)
		self.vectorOps = VectorOps(self.center,self.dest,self.velocity)
		self.colorList = colorList
		self.colorIndex = 0
		self.color = self.colorList[self.colorIndex]
		self.mass = mass
		self.bounds = bounds
		self.maxRadius = maxRadius

	"""
	@function destination

	Given a distance and a bearing find the point: P2 (where we would end up).

	Taken from quadtree implementation pushed onto github

	@param  {double} - distance: the distance the point should be
	@param {double} - bearing: the direction the point should be placed in
	@returns{Point}   - returns a point representing the new location
	"""
	def destination(self, distance, bearing):
		cosa = math.sin(bearing)
		cosb = math.cos(bearing)
		return Point(self.x + (distance * cosa), self.y + (distance * cosb))

	"""
	@function move

	Applies the "step" to current location and checks for out of bounds

	Taken from quadtree implementation pushed onto github

	@returns{void}   - The location of the ball is updated and direction changed if necessary to keep in bounds
	"""
	def move(self):
		x = self.x
		y = self.y

		#Move temporarily
		x += self.vectorOps.dx
		y += self.vectorOps.dy

		#Check if in bounds
		#If it's not, then change direction
		if not self._xInBounds(self.bounds,x):
			self.vectorOps.dx *= -1
			self._change_bearing(math.pi)
		if not self._yInBounds(self.bounds,y):
			self.vectorOps.dy *= -1
			self._change_bearing(math.pi)

		# Move any way because If we hit boundaries then we'll
		# go in the other direction.
		self.x += self.vectorOps.dx
		self.y += self.vectorOps.dy

		# Update center value of ball
		self.center.x = self.x
		self.center.y = self.y

	
	"""
	@function _xInBounds

	Checks to see if the ball is within the x coordinates of the bounds passed in

	Taken from quadtree implementation pushed onto github

	@param  {Bounds} - bounds: essentially a bounding box
	@param {double} - x: the x coordinate of the ball to check if in bounds
	@returns{boolean}   - returns True if in bounds, false otherwise
	"""
	def _xInBounds(self,bounds,x):
		if x + self.radius >= bounds.maxX or x - self.radius <= bounds.minX :
			return False

		return True

	"""
	@function _yInBounds

	Checks to see if the ball is within the y coordinates of the bounds passed in

	Taken from quadtree implementation pushed onto github

	@param  {Bounds} - bounds: essentially a bounding box
	@param {double} - y: the y coordinate of the ball to check if in bounds
	@returns{boolean}   - returns True if in bounds, false otherwise
	"""
	def _yInBounds(self,bounds,y):
		if y + self.radius >= bounds.maxY or y - self.radius <= bounds.minY:
			return False

		return True

	"""
	@function _change_bearing 

	Changes the bearing of the ball by an amount in radians

	Taken from quadtree implementation pushed onto github

	@param  {double} - change: the amount to change the bearing by in radians
	
	@returns{void}   - the bearing of the ball is updated
	"""
	def _change_bearing(self, change):
		self.bearing = (self.bearing + change) % (2 * math.pi)
	
	"""
	@function changeSpeed 

	Sets the velocity of the ball to a new velocity and changes the bearing

	Taken from quadtree implementation pushed onto github

	@param  {double} - new_velocity: descriptiong
	@returns{void}   - The speed of the ball is updated
	"""
	def changeSpeed(self, new_velocity):
		self.dest = self.destination(100, self.bearing)
		self.velocity = new_velocity
		self.vectorOps = VectorOps(self.center, self.dest,self.velocity)
	
	"""
	@function getBBox

	Returns a bounding box representation of the ball used in the quad tree

	@returns{Rectangle}   - Returns a rectangle representing the bounding box
	"""
	def getBBox(self):
		return Rectangle(Point(self.center.x - self.radius, self.center.y - self.radius), Point(self.center.x + self.radius, self.center.y + self.radius))


	"""
	@function collides

	Checks for collision of two balls using their center point and radius. If the distance between
	the centers is less than the sum of their radii then they are colliding

	Found help at http://stackoverflow.com/questions/345838/ball-to-ball-collision-detection-and-handling

	@param  {Ball} - ball: Takes a ball and checks to see if this ball is colliding with that ball
	@returns{boolean}   - If the balls are colliding returns true, returns false otherwise
	"""
	def collides(self, ball):
		xd = self.x - ball.x #get the difference in x positions
		yd = self.y - ball.y #get the difference in y positions

		sumRadius = self.radius + ball.radius #find the minimum distance the difference can be before collision based on
										#radii
		sqrRadius = sumRadius * sumRadius

		distSqr = (xd * xd) + (yd * yd) #find the distance between the balls

		if (distSqr <= sqrRadius):
			return True
		else:
			return False
	
	"""
	@function handleCollision
	
	The ball handles a collision with another ball

	Found help at http://gamedev.stackexchange.com/questions/20516/ball-collisions-sticking-together and used the built in vectorOps class

	@param  {Ball} - ball: Takes a ball that this one is currently colliding with as a parameter
	@returns{void}   - The balls directions are changed, their radius increased, and their color changed
	"""	
	def handleCollision(self, ball):
		xDist = self.center.x - ball.center.x #calculate x distance between the ball centers
		yDist = self.center.y - ball.center.y #calculate y distance between the ball centers
		distSquared = xDist * xDist + yDist * yDist #find the squared distance between the ball centers
		xVel = ball.vectorOps.dx - self.vectorOps.dx #find the combined x velocity of the balls
		yVel = ball.vectorOps.dy - self.vectorOps.dy #find the combined y velocity of the balls
		dotProduct = xDist * xVel + yDist * yVel #determine the dot product to determine the direction the balls are moving
		if(dotProduct > 0): #if the balls are moving toward each other
			collisionScale = dotProduct / distSquared #The Collision vector is the speed difference projected on the Dist vector,
			xCollision = xDist * collisionScale #thus it is the component of the speed difference needed for the collision.
			yCollision = yDist * collisionScale
			combinedMass = self.mass + ball.mass
			collisionWeightA = 2 * ball.mass / combinedMass #figure out the weight of each ball in the collision
			collisionWeightB = 2 * self.mass / combinedMass
			self.vectorOps.dx += collisionWeightA * xCollision #change the x and y velocity of the balls according to the collision
			self.vectorOps.dy += collisionWeightA * yCollision
			ball.vectorOps.dx -= collisionWeightB * xCollision
			ball.vectorOps.dy -= collisionWeightB * yCollision
			if(self.radius < self.maxRadius): #If you haven't reached the maximum size of the circle increase its radius
									 #after a collision
				self.radius += .5
			if(ball.radius < ball.maxRadius):
				ball.radius += .5
			self.colorIndex = (self.colorIndex + 1) % len(self.colorList) #increment the color index to get the next color
			ball.colorIndex = (ball.colorIndex + 1) % len(ball.colorList)
			self.color = self.colorList[self.colorIndex] #update the color
			ball.color = ball.colorList[ball.colorIndex]
		self.move() #move the ball to get out of the collision, moves even if the circles aren't
			  #moving toward each other so they don't get stuck
		ball.move()
			
	"""
	@function as_tuple

	Gets the coordinates of the ball as a tuple

	Taken from quadtree implementation pushed onto github

	@returns{tuple}   - returns a tuple representing the ball location
	"""
	def as_tuple(self):
		return (self.x, self.y)

	"""
	@function __str__

	Represents the data in a ball as a string

	Taken from quadtree implementation pushed onto github

	@returns{string}   - returns a a string representation of a ball
	"""
	def _str__(self):
		return "[\n center: %s,\n radius: %s,\n Vector: %s,\n speed: %s\n ]" % (self.center,self.radius, self.vectorOps, self.velocity)

	"""
	@function __repr__

	Represents the data in a ball as a string

	Taken from quadtree implementation pushed onto github

	@returns{string}   - returns a a string representation of a ball
	"""
	def __repr__(self):
		return "[\n center: %s,\n radius: %s,\n Vector: %s,\n speed: %s\n ]" % (self.center, self.radius, self.vectorOps, self.velocity)

"""
A class more or so to put all the boundary values together. Friendlier than
using a map type.
"""
class Bounds(object):
	"""
	@function __init__
	
	initializes the extent of the bounds

	@param  {double} - minx: The min x coordinate of the bounds
	@param  {double} - miny: The min y coordinate of the bounds
	@param  {double} - maxx: The max x coordinate of the bounds
	@param  {double} - maxy: The max y coordinate of the bounds
	@returns{void}   - The bounds are initialized
	"""	
	def __init__(self,minx,miny,maxx,maxy):
		self.minX = minx
		self.minY = miny
		self.maxX = maxx
		self.maxY = maxy

	"""
	@function __str__

	Represents the data in a Bounds object as a string

	Taken from quadtree implementation pushed onto github

	@returns{string}   - returns a a string representation of a Bounds object
	"""
	def __repr__(self):
		return "[%s %s %s %s]" % (self.minX, self.minY, self.maxX,self.maxY)

"""
The driver class that extends the Pantograph class that creates the html 5
canvas animations.
If you run this file from the command line "python visualizeQuadtree.py"
Pantograph will start a local server running at address: http://127.0.0.1:8080
Simply place "http://127.0.0.1:8080" in the address bar of a browser and hit enter.
Dependencies:
	Pantograph:
		pip install pantograph
	Numpy
	Point
	Rectangle
"""
class Driver(pantograph.PantographHandler):
	"""
	@function setup
	
	Creates the balls and sets up all the variables necessary for running the animation
	Also creates a list of all possible colors. All balls are then put into the a quad tree

	Modified from code pushed onto github

	@returns{void}   - The variables are initialized and balls created and put into quadtree
	"""	
	def setup(self):
		self.bounds = Bounds(0,0,self.width,self.height)
		self.bbox = Rectangle(Point(0, 0), Point(10, 10))
		self.ballSpeeds = np.arange(1,4,1)
		self.ballMasses = np.arange(1,10,1)
		self.numBalls = 50
		self.ballSize = 10
		self.radius = self.ballSize / 2
		self.balls = []
		self.boxes = []
		self.freeze = False
		self.colorList = []
		self.maxBallRadius = (self.width + self.height) / self.numBalls
		mass = random.choice(self.ballMasses)
		for i in xrange(0, 16):
			for j in xrange(0, 16):
				for k in xrange(0, 16):
					self.colorList.append("#" + "{0:x}{1:x}{2:x}".format(i,j,k))
		for i in range(self.numBalls):
			speed = random.choice(self.ballSpeeds)
			newBall = Ball(self.getRandomPosition(),self.ballSize, self.bounds, self.colorList, speed, mass, self.maxBallRadius)
			self.balls.append(newBall)
		
	  
		self.qt = PointQuadTree(Rectangle(Point(0,0),Point(self.width,self.height)),2, self.balls)

	"""
	@function update
	
	Runs the animation including moving the balls and drawing them. Update happens every ? milliseconds. Its not to bad.

	Taken from code pushed onto github
	
	@returns{void}   - animation is updated
	"""	
	def update(self):
		if not self.freeze:
			self.moveBalls()
		self.clear_rect(0, 0, self.width, self.height)
		self.drawBalls()
		self.drawBoxes()
	
	"""
	@function getRandomPosition
	Generate some random point somewhere within the bounds of the canvas.

	Taken from quadtree code pushed onto github
	
	@returns{Point}   - returns point with random Position in screen
	"""	
	def getRandomPosition(self):
		x = random.randint(0 + self.ballSize, int(self.width) - self.ballSize)
		y = random.randint(0 + self.ballSize, int(self.height) - self.ballSize)
		return Point(x,y)

	"""
	@function drawBoxes
	
	Draw the bounding boxes fetched from the quadtree
	
	Taken from quadtree code pushed onto github
	
	@returns{void}   - the bounding boxes of the quad tree are drawn
	"""	
	def drawBoxes(self):
		boxes = self.qt.getBBoxes()
		for box in boxes:
			self.draw_rect(box.top_left().x, box.top_left().y, box.width, box.height)
		#for r in self.balls:
			#self.draw_rect(r.getBBox().top_left().x, r.getBBox().top_left().y,
			#r.getBBox().width, r.getBBox().height)


	"""
	@function drawBalls
	
	Draw the balls onto the screen

	Taken from quadtree code pushed onto github
	
	@returns{void}  - the balls are drawn
	"""	
	def drawBalls(self):
		for r in self.balls:
			self.fill_circle(r.x, r.y, r.radius, r.color)

	"""
	@function moveBalls
	
	Moves the balls by applying my super advanced euclidian based geometric
	vector functions to my balls. By super advanced I mean ... not. The balls
	are inserted into the quadtree and it is updated

	Modified from quadtree code pushed onto github
	
	@returns{void}   - the balls are moved and the quadtree is updated
	"""
	def moveBalls(self):
		for ball in self.balls:
			ball.move()
		self.qt = PointQuadTree(Rectangle(Point(0, 0),Point(self.width, self.height)), 2, self.balls)
		self.qt.update()
		
	"""
	@function on_click
	
	Freezes and unfreezes the movement of the balls

	Taken from quadtree code pushed onto github

	@param{InputEvent} - InputEvent: the mouse is clicked
	@returns{void}   - the balls movement is stopped and started
	"""
	def on_click(self,InputEvent):
		if self.freeze == False:
			self.freeze = True
		else:
			self.freeze = False

	"""
	@function on_key_down
	
	On up arrow press the speed of the balls increased
	On down arrow press the speed of the balls lowered

	Modified from quadtree code pushed onto github

	@param{InputEvent} - InputEvent: up or down arrow is pressed
	@returns{void}   - the balls movement is sped up or slowed down
	"""
	def on_key_down(self,InputEvent):
		# User hits the UP arrow
		if InputEvent.key_code == 38:
			for r in self.balls:
				r.changeSpeed(r.velocity * 1.25)
		# User hits the DOWN arrow
		if InputEvent.key_code == 40:
			for r in self.balls:
				r.changeSpeed(r.velocity * .75)
			pass


if __name__ == '__main__':
	app = pantograph.SimplePantographApplication(Driver)
	app.run()
