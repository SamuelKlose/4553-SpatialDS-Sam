"""
@author - Samuel Klose
@date - 10/1/2015
@description - This program does creates 3 polygons and three points and moves them around
the screen. They bounce off the edges

@resources - I found code and methods at http://pythonhelper.com,
http://gamedev.stackexchange.com/, http://stackoverflow.com/ and used code from assignment and github.
"""
"""Point and Rectangle classes.

This code is in the public domain.

Point  -- point with (x,y) coordinates
Rect  -- two points, forming a rectangle
"""
import pantograph
import math
import sys
import random
import numpy as np

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
	def __init__(self, x = 0.0, y = 0.0):
		self.x = x
		self.y = y
		self.directionList = ['N','NE','E','SE','S','SW','W','NW']
		self.direction = random.choice(self.directionList)
		self.velocityX = 0
		self.velocityY = 0
		self.set_direction(self.direction)

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
		return "(%s, %s)" %(self.x, self.y)

	"""
	@function __repr__

	Function description: Prints a representation of point

	From polygon code given in assignment

	@returns{void}:   - prints the point
	"""
	def __repr__(self):
		return "%s(%r, %r)" %(self.__class__.__name__, self.x, self.y)

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

	"""
	@function set_velocity

	Function description: Divides this point with another points

	Modified from polygon code given in assignment for movement

	@param  {double} - velX: x velocity of the point
	@param  {double} - velY: y velocity of the point
	@returns{void}:   - velocity is changed
	"""
	def set_velocity(self, velX, velY):
		self.velocityX = velX
		self.velocityY = velY
	
		"""
	@function set_direction

	Function description: Changes the velocity of the point based on direction desired

	Modified from polygon code given in assignment using randomwalk idea given

	@param  {string} - direction: direction the point travels in
	@returns{Point()}:   - point is traveling in new direction
	"""
	def set_direction(self,direction):
		assert direction in ['N','NE','E','SE','S','SW','W','NW']
		self.direction = direction
		if direction == "N":
			self.set_velocity(0, -1)
		elif direction == "NE":
			self.set_velocity(1, -1)
		elif direction == "E":
			self.set_velocity(1, 0)
		elif direction == "SE":
			self.set_velocity(1, 1)
		elif direction == "S":
			self.set_velocity(0, 1)
		elif direction == "SW":
			self.set_velocity(-1, 1)
		elif direction == "W":
			self.set_velocity(-1, 0)
		elif direction == "NW":
			self.set_velocity(-1, -1)
		self.update_position()
	
	"""
	@function get_direction_from_velocity

	Function description: Figures out direction based on current velocity

	Modified from polygon code given in assignment and randomwalk idea

	@returns{string}:   - returns the direction
	"""
	def get_direction_from_velocity(self):
		if self.velocityX == 0 and self.velocityY == -1:
			return "N"
		elif self.velocityX == 1 and self.velocityY == -1:
			return "NE"
		elif self.velocityX == 1 and self.velocityY == 0:
			return "E"
		elif self.velocityX == 1 and self.velocityY == 1:
			return "SE"
		elif self.velocityX == 0 and self.velocityY == 1:
			return "S"
		elif self.velocityX == -1 and self.velocityY == 1:
			return "SW"
		elif self.velocityX == -1 and self.velocityY == 0:
			return "W"
		elif self.velocityX == -1 and self.velocityY == -1:
			return "NW"

	"""
	@function get_direction

	Function description: gets the current direction of the point

	From polygon code given in assignment and randomwalk idea

	@returns{string}:   - return current direction of point
	"""
	def get_direction(self):
		return self.direction

	"""
	@function update_position()

	Function description: Updates position based on velocity for movement

	http://www.somethinghitme.com/2013/11/13/snippets-i-always-forget-movement/

	@returns{void}:   - point is moved
	"""
	def update_position(self):
		self.x += self.velocityX
		self.y += self.velocityY



class Rectangle:

	"""A rectangle identified by two points.

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
		x,y = pt.as_tuple()
		return (self.left <= x <= self.right and self.top <= y <= self.bottom)

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
	@function bounding_box_collisions

	Function description: Checks to see if bounding box collided with another bounding box

	http://gamedev.stackexchange.com/questions/586/what-is-the-fastest-way-to-work-out-2d-bounding-box-intersection
	@param {Point()} - other: Bounding box to check collision with
	@returns{void}:   - returns true if boxes interset
	"""
	def bounding_box_collision(self, other):
		"""Return true if a rectangle collides with this rectangle."""
		return ((abs(self.left - other.left) * 2 < (self.width + other.width)) and (abs(self.top - other.top) * 2 < (self.height + other.height)))

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
		return "<Rect (%s,%s)-(%s,%s)>" %(self.left,self.top, self.right,self.bottom)

	"""
	@function __repr__

	Function description: Prints out representation of the rectangle

	From code given for assignment

	@returns{string}:   - Prints out representation of itself
	"""
	def __repr__(self):
		return "%s(%r, %r)" %(self.__class__.__name__, Point(self.left, self.top), Point(self.right, self.bottom))

class Polygon(object):
	"""
	@function __init__

	Function description: Creates a polygon and initializes the points

	Modified from code given for assignment

	@returns{string}:   - Initializes points and direction of polygon
	"""
	def __init__(self, pts = []):
		"""Initialize a polygon from list of points."""
		self.set_points(pts)
		self.directionList = ['N','NE','E','SE','S','SW','W','NW']
		self.set_direction("N")

	"""
	@function set_points

	Function description: Resets the poly coordinates

	From code given for assignment
	@param{List[]} - pts: points representing the polygon
	@param{Point()} - centroid: center of the polygon
	@returns{void}:   - Initializes minimum bounding rectangle, centroid and points
	"""
	def set_points(self, pts,centroid=None):

		if not centroid == None:
			self.centroid = Point(centroid[0],centroid[1])
		else:
			self.centroid = None

		self.minX = sys.maxsize
		self.minY = sys.maxsize
		self.maxX = sys.maxsize * -1
		self.maxY = sys.maxsize * -1

		self.points = []

		for p in pts:
			x,y = p

			if x < self.minX:
				self.minX = x
			if x > self.maxX:
				self.maxX = x
			if y < self.minY:
				self.minY = y
			if y > self.maxY:
				self.maxY = y

			self.points.append(Point(x,y))

		self.mbr = Rectangle(Point(self.minX,self.minY),Point(self.maxX,self.maxY))
		
	"""
	@function get_points

	Function description: gets the points of the polygon

	@returns{List[]}:   - Returns list of points in polygon
	"""
	def get_points(self):
		generic = []
		for p in self.points:
			generic.append(p.as_tuple())
		return generic

	"""
	@function point_inside_polygon

	Function description: Determines if a point is overlapping the polygon

	From code given for assignment

	@param{Point()} - p: Point to check if is inside of polygon
	@returns{boolean}:   - Returns true if point is inside of polygon
	"""
	# determine if a point is inside a given polygon or not
	# Polygon is a list of (x,y) pairs.
	def point_inside_polygon(self, p):
		n = len(self.points)
		inside = False

		p1x,p1y = self.points[0].as_tuple()
		for i in range(n + 1):
			p2x,p2y = self.points[i % n].as_tuple()
			if p.y > min(p1y,p2y):
				if p.y <= max(p1y,p2y):
					if p.x <= max(p1x,p2x):
						if p1y != p2y:
							xinters = (p.y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
						if p1x == p2x or p.x <= xinters:
							inside = not inside
			p1x,p1y = p2x,p2y

		return inside

	"""
	@function order_points

	Function description: Orders the points of the polygon; used in RandPolygon

	From code given for assignment

	@returns{void}:   - Points in polygon list are ordered
	"""
	def orderPoints(self):
		assert not self.centroid == None

		ptsDict = {}
		for p in self.points:
			ptsDict[self.angleWithRespect2Centroid(p.x,p.y)] = p
			#print self.angleWithRespect2Centroid(p.x,p.y)
		self.points = []
		for key in sorted(ptsDict):
			#print "%s: %s" % (key, ptsDict[key])
			self.points.append(ptsDict[key])
	
	"""
	@function set_direction

	Function description: Changes the direction of the polygon and all its points

	Using random walk idea from assignment description

	@param{string} - direction: direction to move the polygon in
	@returns{void}:   - The polygons direction is changed for movement
	"""
	def set_direction(self, direction):
		assert direction in ['N','NE','E','SE','S','SW','W','NW']
		self.direction = direction
		for point in range(len(self.points)):
			self.points[point].set_direction(direction)
		self.updateMBR()
	"""
	@function set_points

	Function description: Calculates the signed area of an arbitrary polygon given its verticies
		http://stackoverflow.com/a/4682656/190597 (Joe Kington)
		http://softsurfer.com/Archive/algorithm_0101/algorithm_0101.htm#2D%20Polygons
	

	From code given for assignment
	@param{double} - x: x coordinate
	@param{double} - y: y coordinate
	@returns{string}:   - calculates area of polygon
	"""
	def calcArea(self,x, y):
		
		area = 0.0
		for i in xrange(-1, len(x) - 1):
			area += x[i] * (y[i + 1] - y[i - 1])
		return area / 2.0

	"""
	@function calcCentroid

	Function description: Gets the center of the polygon


	http://stackoverflow.com/a/14115494/190597 (mgamba)


	@returns{Point()}:   - The result is returned
	"""
	def calcCentroid(self):
		
		area = self.calcArea(*zip(*points))
		points = self.points
		result_x = 0
		result_y = 0
		N = len(points)
		points = IT.cycle(points)
		x1, y1 = next(points)
		for i in range(N):
			x0, y0 = x1, y1
			x1, y1 = next(points)
			cross = (x0 * y1) - (x1 * y0)
			result_x += (x0 + x1) * cross
			result_y += (y0 + y1) * cross
		result_x /= (area * 6.0)
		result_y /= (area * 6.0)
		return (result_x, result_y)


	def angleWithRespect2Centroid(self,x,y):
		assert not self.centroid == None

		return math.atan2(y - self.centroid.y, x - self.centroid.x)

	def get_direction(self):
		return self.direction

	def update_position(self):
		for point in range(len(self.points)):
			self.points[point].update_position()
		self.updateMBR()
	
	"""
	@function move

	Function description: moves the polygon

	@param{double} - x: x coord
	@param{double} - x: y coord
	@returns{void}:   - polygons change direction 
	"""
	def move(self, x, y):
		for p in range(len(self.points)):
			self.points[p].slide_xy(x, y)
		self.updateMBR()
	"""
	@function updateMBR

	Function description: Updates the minimum bounding rectangle

	Based on code given in assignment

	@returns{void}:   - minimum bounding rectangle changed
	"""
	def updateMBR(self):
		self.oldMbr = self.mbr
		self.minX = sys.maxsize
		self.minY = sys.maxsize
		self.maxX = sys.maxsize * -1
		self.maxY = sys.maxsize * -1
		for p in self.points:
			if p.x < self.minX:
				self.minX = p.x
			if p.x > self.maxX:
				self.maxX = p.x
			if p.y < self.minY:
				self.minY = p.y
			if p.y > self.maxY:
				self.maxY = p.y
		self.mbr = Rectangle(Point(self.minX,self.minY),Point(self.maxX,self.maxY))
	"""
	@function negate_direction_y

	Function description: Negates the direction of the polygon on the y axis

	http://gamedev.stackexchange.com/questions/13774/how-do-i-detect-the-direction-of-2d-rectangular-object-collisions

	@returns{void}:   - polygons change direction 
	"""
	def negate_direction_x(self):
		for p in range(len(self.points)):
			velocityX = self.points[p].velocityX
			velocityY = self.points[p].velocityY
			self.points[p].set_velocity(-velocityX, velocityY)
			newDirection = self.points[p].get_direction_from_velocity()
			self.points[p].set_direction(newDirection)
			self.points[p].slide_xy(-velocityX, velocityY)
		self.update_position()
		self.updateMBR()
		self.direction = self.points[0].get_direction()

	"""
	@function negate_direction_y

	Function description: Negates the direction of the polygon on the y axis

	http://gamedev.stackexchange.com/questions/13774/how-do-i-detect-the-direction-of-2d-rectangular-object-collisions

	@returns{void}:   - polygons change direction 
	"""
	def negate_direction_y(self):
		for p in range(len(self.points)):
			velocityX = self.points[p].velocityX
			velocityY = self.points[p].velocityY
			self.points[p].set_velocity(velocityX, -velocityY)
			newDirection = self.points[p].get_direction_from_velocity()
			self.points[p].set_direction(newDirection)
			self.points[p].slide_xy(velocityX, -velocityY)
		self.update_position()
		self.updateMBR()
		self.direction = self.points[0].get_direction()


	def __str__(self):
		return "<Polygon \n Points: %s \n Mbr: %s>" % ("".join(str(self.points)),str(self.mbr))

	def __repr__(self):
		return "%s %s" % (self.__class__.__name__,''.join(str(self.points)))

class RandPolygon(object):
	"""
	@function __init__

	Function description: Changes the direction of polygons when they collide with the wall
	to keep them inside the scene

	Uses rectangle class from assignment for minimum bounding rectangle and random walk idea

	@returns{void}:   - polygons change direction when they collide with wall
	"""
	def __init__(self,minDist = 1000,maxDist = 5000,minPoints = 10,maxPoints = 100,startY = 30.430073,startX = 59.143826):
		self.minDist = minDist
		self.maxDist = maxDist
		self.minPoints = minPoints
		self.maxPoints = maxPoints
		self.randPoints = random.randrange(self.minPoints,self.maxPoints)
		self.startX = startX
		self.startY = startY

		self.currIteration = 0.0
		self.maxIteration = self.maxPoints

		self.polygon = Polygon()
		self.points = []

		self.generatePolygon()
	
	"""
	@function destination

	Function description: Displaces a LatLng angle degrees counterclockwise and some
	distance in that direction

	Taken from RandPolygon on github by Dr. Griffin

	@returns{void}:   - latitude and longitude displaced
	"""
	def destination(self,x,y,angle, distance):
		"""
		Displace a LatLng angle degrees counterclockwise and some
		meters in that direction.
		Notes:
			http://www.movable-type.co.uk/scripts/latlong.html
			0 DEGREES IS THE VERTICAL Y AXIS! IMPORTANT!
		Args:
			angle:    A number in degrees.
			distance: A number in meters.
		Returns:
			A new LatLng.
		"""
		angle = np.float32(angle)

		delta = np.divide(np.float32(distance), np.float32(3959))

		angle = self.deg2rad(angle)
		y1 = self.deg2rad(y)
		x1 = self.deg2rad(x)

		y2 = np.arcsin(np.sin(y1) * np.cos(delta) + np.cos(y1) * np.sin(delta) * np.cos(angle))

		x2 = x1 + np.arctan2(np.sin(angle) * np.sin(delta) * np.cos(y1),
								  np.cos(delta) - np.sin(y1) * np.sin(y2))

		x2 = (x2 + 3 * np.pi) % (2 * np.pi) - np.pi

		return [self.rad2deg(x2),self.rad2deg(y2)]

	def deg2rad(self,angle):
			return np.divide(np.dot(angle, np.pi), np.float32(180.0))

	def rad2deg(self,angle):
			return np.divide(np.dot(angle, np.float32(180.0)), np.pi)
	
	"""
	@function generatePolygon

	Function description: Uses the methods of this class to generate the randomized
	list of points for a polygon

	Taken from RandPolygon class on github by Dr. Griffin

	@returns{void}:   - a randomized polygon is created
	"""
	def generatePolygon(self):
		pts = []
		n = self.randPoints
		for i in range(n):
			angle = self.randAngle(i,n,"Degrees")
			distance = random.randrange(self.minDist,self.maxDist)
			xy = self.destination(self.startX,self.startY,self.rad2deg(angle),distance)
			pts.append((xy[0],xy[1]))
		self.polygon.set_points(pts,(self.startX,self.startY))
		self.polygon.orderPoints()
		pts = self.polygon.get_points()
		#for p in pts:
			#print(p[1],",",p[0],":")
	
	"""
	@function randDistance

	Function description: Generates a distance using the python random library

	Taken from RandPolygon class on github by Dr. Griffin

	@returns{void}:   - polygons change direction when they collide with wall
	"""
	def randDistance(self):
		random.randrange(self.minDist,self.maxDist)
	"""
	@private
	@method - randAngle: Generates a random angle between the ith and ith + 1 iteration.
						 Meaning that if this function was called 4 times, it would successively
						 return angles: 0-90,90-180,180-270,270-360
	@param {int} i      : Current iteration count (or starting angle)
	@param {int} n      : Max iterations (or ending angle)
	@param {string}     : Radians or Degrees
	@returns list[]: list of items in node
	"""
	def randAngle(self,i,n,Units = "Radians"):
		i = float(i)
		n = float(n)
		value = (2.0 * math.pi) * random.uniform((i) / n , (i + 1) / n)
		if Units == "Radians":
			return value
		else:
			return math.degrees(value)

class Driver(pantograph.PantographHandler):
	"""
	@function setup

	Function description: Creates the polygons and points and puts them in the scene
	with a random direction

	Uses code from assignment and RandPolygon class grabbed from github for creating
	randomized polygons for scene.

	@returns{void}:   - polygons and points are initialized in scene
	"""
	def setup(self):
		self.polyList = []
		self.pointList = []
		self.directionList = ['N','NE','E','SE','S','SW','W','NW']
		self.pointSize = 7
		self.numPolys = 3
		self.numPoints = 3

		for i in range(1, self.numPolys + 1):
			tempPoly = RandPolygon()
			direction = random.choice(self.directionList)
			tempPoly.polygon.set_direction(direction)
			tempPoly.polygon.move(200 * i, 200 * i)
			self.polyList.append(tempPoly.polygon)
			i += 1

		for i in range(0, self.numPoints):
			self.pointList.append(Point(random.randint(1, self.width), random.randint(1, self.height)))
			i += 1
	
	"""
	@function drawShapes

	Function description: Draws the polygons and the points during each update loop to simulate
	movement.

	Uses pantograph code from assignment to draw the scene

	@returns{void}:   - polygons and points are drawn to the screen
	"""
	def drawShapes(self):
		for poly in range(len(self.polyList)):
			self.draw_polygon(self.polyList[poly].get_points(), color = "#000")
			#self.draw_rect(self.polyList[poly].mbr.left, self.polyList[poly].mbr.top, self.polyList[poly].mbr.width, self.polyList[poly].mbr.height, "#F00")
		self.draw_rect(0, 0, self.width, self.height, color = "#000")

		for point in range(len(self.pointList)):
			for poly in range(len(self.polyList)):
				if  self.polyList[poly].point_inside_polygon(self.pointList[point]):
					color = "#0F0"
					break
				else:
					color = "#F00"
			self.fill_oval(self.pointList[point].x, self.pointList[point].y, self.pointSize, self.pointSize, color)

	"""
	@function hitWallPoint

	Function description: Changes the direction of points when they collide with the wall
	to keep them inside the scene

	Uses point class from assignment

	@returns{void}:   - points change direction when they collide with wall
	"""
	def hitWallPoint(self):
		for point in range(len(self.pointList)):
			if self.pointList[point].get_direction() == "N" and self.pointList[point].y < 0:

				self.pointList[point].set_direction("S")
				self.pointList[point].slide_xy(0, -self.pointSize)

			elif self.pointList[point].get_direction() == "NE" and self.pointList[point].y < 0:

				self.pointList[point].set_direction("SE")
				self.pointList[point].slide_xy(0, -self.pointSize)

			elif self.pointList[point].get_direction() == "NE" and self.pointList[point].x > self.width:

				self.pointList[point].set_direction("NW")
				self.pointList[point].slide_xy(-self.pointSize, 0)

			elif self.pointList[point].get_direction() == "E" and self.pointList[point].x > self.width:

				self.pointList[point].set_direction("W")
				self.pointList[point].slide_xy(-self.pointSize, 0)

			elif self.pointList[point].get_direction() == "SE" and self.pointList[point].y > self.height:

				self.pointList[point].set_direction("NE")
				self.pointList[point].slide_xy(0, self.pointSize)

			elif self.pointList[point].get_direction() == "SE" and self.pointList[point].x > self.width:

				self.pointList[point].set_direction("SW")
				self.pointList[point].slide_xy(-self.pointSize, 0)

			elif self.pointList[point].get_direction() == "S" and self.pointList[point].y > self.height:

				self.pointList[point].set_direction("N")
				self.pointList[point].slide_xy(0, self.pointSize)

			elif self.pointList[point].get_direction() == "SW" and self.pointList[point].y > self.height:

				self.pointList[point].set_direction("NW")
				self.pointList[point].slide_xy(0, self.pointSize)

			elif self.pointList[point].get_direction() == "SW" and self.pointList[point].x < 0:

				self.pointList[point].set_direction("SE")
				self.pointList[point].slide_xy(self.pointSize, 0)

			elif self.pointList[point].get_direction() == "W" and self.pointList[point].x < 0:

				self.pointList[point].set_direction("E")
				self.pointList[point].slide_xy(self.pointSize, 0)

			elif self.pointList[point].get_direction() == "NW" and self.pointList[point].y < 0:

				self.pointList[point].set_direction("SW")
				self.pointList[point].slide_xy(0, self.pointSize)

			elif self.pointList[point].get_direction() == "NW" and self.pointList[point].x < 0:
				
				self.pointList[point].set_direction("NE")
				self.pointList[point].slide_xy(self.pointSize, 0)

	"""
	@function hitWallPolygon

	Function description: Changes the direction of polygons when they collide with the wall
	to keep them inside the scene

	Uses rectangle class from assignment for minimum bounding rectangle and random walk idea

	@returns{void}:   - polygons change direction when they collide with wall
	"""
	def hitWallPolygon(self):
		for poly in range(len(self.polyList)):
			if self.polyList[poly].get_direction() == "N" and self.polyList[poly].mbr.top < 0:
				self.polyList[poly].set_direction("S")
				while(self.polyList[poly].mbr.top < 0):
					self.polyList[poly].move(0, 1)

			elif self.polyList[poly].get_direction() == "NE" and self.polyList[poly].mbr.top < 0:
				self.polyList[poly].set_direction("SE")
				while(self.polyList[poly].mbr.top < 0):
					self.polyList[poly].move(0, 1)

			elif self.polyList[poly].get_direction() == "NE" and self.polyList[poly].mbr.right > self.width:
				self.polyList[poly].set_direction("NW")
				while(self.polyList[poly].mbr.right > self.width):
					self.polyList[poly].move(-1, 0)

			elif self.polyList[poly].get_direction() == "E" and self.polyList[poly].mbr.right > self.width:
				self.polyList[poly].set_direction("W")
				while(self.polyList[poly].mbr.right > self.width):
					self.polyList[poly].move(-1, 0)

			elif self.polyList[poly].get_direction() == "SE" and self.polyList[poly].mbr.bottom > self.height:
				self.polyList[poly].set_direction("NE")
				while(self.polyList[poly].mbr.bottom > self.height):
					self.polyList[poly].move(0, -1)

			elif self.polyList[poly].get_direction() == "SE" and self.polyList[poly].mbr.right > self.width:
				self.polyList[poly].set_direction("SW")
				while(self.polyList[poly].mbr.right > self.width):
					self.polyList[poly].move(-1, 0)

			elif self.polyList[poly].get_direction() == "S" and self.polyList[poly].mbr.bottom > self.height:
				self.polyList[poly].set_direction("N")
				while(self.polyList[poly].mbr.bottom > self.height):
					self.polyList[poly].move(0, -1)

			elif self.polyList[poly].get_direction() == "SW" and self.polyList[poly].mbr.bottom > self.height:
				self.polyList[poly].set_direction("NW")
				while(self.polyList[poly].mbr.bottom > self.height):
					self.polyList[poly].move(0, -1)

			elif self.polyList[poly].get_direction() == "SW" and self.polyList[poly].mbr.left < 0:
				self.polyList[poly].set_direction("SE")
				while(self.polyList[poly].mbr.left < 0):
					self.polyList[poly].move(1, 0)

			elif self.polyList[poly].get_direction() == "W" and self.polyList[poly].mbr.left < 0:
				self.polyList[poly].set_direction("E")
				while(self.polyList[poly].mbr.left < 0):
					self.polyList[poly].move(1, 0)

			elif self.polyList[poly].get_direction() == "NW" and self.polyList[poly].mbr.top < 0:
				self.polyList[poly].set_direction("SW")
				while(self.polyList[poly].mbr.top < 0):
					self.polyList[poly].move(0, 1)
	
			elif self.polyList[poly].get_direction() == "NW" and self.polyList[poly].mbr.left < 0:
				self.polyList[poly].set_direction("NE")
				while(self.polyList[poly].mbr.left < 0):
					self.polyList[poly].move(1, 0)


	"""
	@function handleCollisions

	Function description: Changes the direction of polygons when they collide.
	Note: Seems to occassionally spaz out on corner hits but eventually rights itself.

	http://gamedev.stackexchange.com/questions/586/what-is-the-fastest-way-to-work-out-2d-bounding-box-intersection
	http://gamedev.stackexchange.com/questions/24078/which-side-was-hit

	@returns{void}:   - polygons change direction when they collide
	"""
	def handleCollisions(self):
		for poly in range(len(self.polyList)):
			for otherPoly in range(len(self.polyList)):
				if self.polyList[poly] is not self.polyList[otherPoly] and self.polyList[poly].mbr.bounding_box_collision(self.polyList[otherPoly].mbr):
					print "there is a collision"
					if self.polyList[poly].mbr.get_collision_side(self.polyList[otherPoly].mbr) == "Right" or self.polyList[poly].mbr.get_collision_side(self.polyList[otherPoly].mbr) == "Left":
						self.polyList[poly].negate_direction_x()
						self.polyList[otherPoly].negate_direction_x()
						print "negating x direction"
					if self.polyList[poly].mbr.get_collision_side(self.polyList[otherPoly].mbr) == "Top" or self.polyList[poly].mbr.get_collision_side(self.polyList[otherPoly].mbr) == "Bottom":
						self.polyList[poly].negate_direction_y()
						self.polyList[otherPoly].negate_direction_y()
						print "negating y direction"
					#else:
					#   self.polyList[poly].negate_direction_x()
					#   self.polyList[poly].negate_direction_y()
					#   self.polyList[otherPoly].negate_direction_x()
					#   self.polyList[otherPoly].negate_direction_y()
				
					
	"""
	@function update

	Function description: main update loop for movement of polys and points.
	Clears the screen, updates the positions of the polys and the points,
	then checks for wall hits and collisions and then draws the shapes.

	From pantograph code given in assignment.

	@returns{void}:   - Objects in scene are handled.
	"""
	def update(self):
		self.clear_rect(0, 0, self.width, self.height)
		
		for poly in range(len(self.polyList)):
			self.polyList[poly].update_position()
			#print self.polyList[poly].mbr

		for point in range(len(self.pointList)):
			self.pointList[point].update_position()

		self.hitWallPoint()
		self.hitWallPolygon()
		self.handleCollisions()
		self.drawShapes()


if __name__ == '__main__':
	app = pantograph.SimplePantographApplication(Driver)
	app.run()
