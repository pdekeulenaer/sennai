# utilities

import math

def arrmult(a,b):
	assert (len(a) == len(b))
	return [a[i]*b[i] for i in range(0,len(a))]

def lincomb(a,b):
	assert (len(a) == len(b))
	s = 0
	for i in range(0, len(a)):
		s += a[i]*b[i]
	return s


def slope(A,B):
	(xa, ya) = A
	(xb, yb) = B
	if (xb == xa): return None

	return (yb-ya) * 1.0 / (xb-xa)

def yintersect((A,B)):
	m = slope(A,B)
	if (m is None): return None
	(xa, ya) = A
	return (ya - (m * xa))


# line given as a tuple of 2 points
def intersect((A,B), (C,D)):
	m1 = slope(A,B)
	m2 = slope(C,D)

	if m1 == m2:
		return None

	if (m1 is not None and m2 is not None):
		# non vertical
		py1 = yintersect((A,B))
		py2 = yintersect((C,D))

		x = (py2 - py1) / (m1 - m2)
		y = (m1 * x) + py1

	else:
		if (m1 is None):
			py2 = yintersect((C,D))
			x = A[0]
			y = (m2 * x) + py2
		elif (m2 is None):
			py1 = yintersect((A,B))
			x = C[0]
			y = (m1 * x) + py1
		else:
			assert False

	return (x,y)

def segment_intersect((A,B),(C,D)):
	p = intersect((A,B),(C,D))
	if p is not None:
		if (is_on(A,B,p) and is_on(C,D,p)):
			return p
	return None

def is_on(A,B,p):
	dotproduct = (p[0] - A[0]) * (B[0] - A[0]) + (p[1] - A[1])*(B[1]-A[1])
	if dotproduct < 0:
		return False

	l = length(A,B)
	if dotproduct > l*l:
		return False

	return True

def length(A,B):
	squaredlength = (B[0]-A[0])*(B[0]-A[0]) + (B[1]-A[1])*(B[1]-A[1])
	return math.sqrt(squaredlength)


	# if (A[0] < B[0]):
	# 	if (point[0] < A[0] or point[0] > B[0]):
	# 		return None
	# else:
	# 	if (point)


# A = (0,0)
# B = (10,10)

# C = (1,1)
# D = (11,11)

# print intersect((A,B),(C,D))


class Vector:
	def __init__(self, x, y, (xa,ya)=(0,0)):
		self.A = (xa*1.0,ya*1.0)
		self.B = (x*1.0,		y*1.0)

	def _to_origin(self):
		v = self.copy()
		(xa, ya) = self.A
		v = v.translate((-xa,-ya))
		# print v
		return v

	def translate(self, (x,y)):
		(xb, yb) = self.B
		(xa, ya) = self.A
		A = (xa + x, ya + y)
		return Vector(xb + x,yb + y,A)

	def copy(self):
		(x,y) = self.B
		return Vector(x,y,self.A)

	def rotate(self, angle=0):
		v = self._to_origin()
		(x, y) = v.B
		alpha = math.radians(angle)
		v.B = (x * math.cos(alpha) - y*math.sin(alpha), x*math.sin(alpha) + y * math.cos(alpha))
		v = v.translate(self.A)
		return v

	def distance(self):
		(xb,yb) = self.B
		(xa, ya) = self.A
		x = xb-xa
		y = yb-ya
		return math.sqrt(x*x + y*y)

	def normalize(self, r=1.0):
		v = self.copy()
		v = v._to_origin()
		d = v.distance()

		(xb, yb) = v.B
		newB = (r*(xb/d), r*(yb/d))
		v.B = newB
		
		v = v.translate(self.A)
		return v

	def __str__(self):
		return str([self.A, self.B])

# v = Vector(10,10, (5,5))
# v = v.normalize(10)
# print v
# print v.distance()
# v = v.normalize(100)
# print v.distance()
# print v
