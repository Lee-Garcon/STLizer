import math
import sys


class point(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z





class spvector(object):
	def __init__(self, spoint, p):
		self.value = (p.x - spoint.x, p.y - spoint.y, p.z - spoint.z)
		self.magnitude = math.sqrt(self.value[0]**2 + self.value[1]**2 + self.value[2]**2)

class vector(object):
	def __init__(self, val):
		self.value = val
		self.magnitude = math.sqrt(self.value[0]**2 + self.value[1]**2 + self.value[2]**2)
		print('math.sqrt(%s^2 + %s^2 + %s^2)' % (self.value[0], self.value[1], self.value[2]))

	def unit_resize(self):
		return vector((self.value[0]/self.magnitude, self.value[1]/self.magnitude, self.value[2]/self.magnitude))





class trigon(object):
	#polygon; triangle
	def __init__(self, p1, p2, p3):
		self.points = [p1, p2, p3]
		self.normal = self.normal()
		self.type = 'trig'

	def normal(self):
		#Vectorize (p1, p2) and (p1, p3)
		vector1 = spvector(self.points[0], self.points[1])
		vector2 = spvector(self.points[0], self.points[2])
		print(vector1.value, vector2.value)
		normal = vector(self.cross_product(vector1.value, vector2.value))
		unit_normal = normal.unit_resize()
		return unit_normal

	def cross_product(self, v1, v2):
		v3 = (v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0])
		return v3

class quad(object):
	#Convert into two polygons
	#Format must be in rect format
	def __init__(self, p1, p2, p3, p4):
		self.type = 'quad'
		self.points = [p1, p2, p3, p4]
		self.poly1 = trigon(p1, p2, p3)
		self.poly2 = trigon(p3, p4, p1)

	def return_poly(self):
		return (self.poly1, self.poly2)

class polygon(object):
	def __init__(self, points):
		self.points = points
		self.polygons = []

	def add_points(self, *points):
		self.points.append(points)

	def initialize(self):
		pivot = self.points[0]
		for idx, val in enumerate(self.points[1:]):
			if idx != len(self.points[1:]):
				self.polygons.append(trigon(pivot, val, self.points[1:][idx+1]))

	def return_poly(self):
		return self.polygons




class solid(object):
	def __init__(self, w, l, h):
		self.w = w
		self.l = l
		self.h = h

		self.vol = w*l*h

		self.polygon_list = []



		#Make a frame

	def add_polygon(self, polygon):
		for x in polygon.points:
			if x.x > self.w or x.y > self.h or x.z > self.l or x.x < 0 or x.y < 0 or x.z < 0:
				return False
		self.polygon_list.append(polygon)

	def export(self, export_file):
		try:
			f = open(export_file, 'w')
		except:
			sys.exit(1)

		_tab = '\t'

		filename = export_file.split('/')[-1].split('.')[0]
		export_text = 'solid %s\n' % filename

		for x in self.polygon_list:
			export_text += '\tfacet normal %s %s %s\n\t\touter loop\n' % (str(x.normal.value[0]), str(x.normal.value[1]), str(x.normal.value[2]))
			for i in range(3):
				export_text += '\t\t\tvertex %s %s %s\n' % (str(x.points[i].x), str(x.points[i].y), str(x.points[i].z))
			export_text += '\t\tendloop\n\tendfacet\n'

		export_text += 'endsolid'

		f.write(export_text)
		f.close()


s = solid(10, 10, 10)

x_z_points = [(10, 5), (5, 10), (0, 5), (2, 3), (5, 0)]

base_poly = polygon([])
for x in x_z_points:
	base_poly.add_points(point(x[0], 0, x[1]))

for x in base_poly.return_poly():
	s.add_polygon(x)

for idx, x in x_z_points:
	s.add_polygon(trigon(point(x[0], 0, x[1]), point(x_z_points[idx+1][0], 0, x_z_points[idx+1][1]), point(5, 5, 5)))


s.export('/Code/test_stl.stl')




