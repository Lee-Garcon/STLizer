import math
import sys
import itertools

class NotSamePlaneError(ValueError):
	pass

class point(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z


class spvector(vector):
	def __init__(self, spoint, p):
		self.value = (p[0] - spoint[0], p[1] - spoint[1], p[2] - spoint[2])
		self.magnitude = math.sqrt(self.value[0]**2 + self.value[1]**2 + self.value[2]**2)

class vector(item):
	Whoami = 'vector'
	def __init__(self, val):
		self.value = val
		self.magnitude = math.sqrt(self.value[0]**2 + self.value[1]**2 + self.value[2]**2)

	def unit_resize(self):
		return vector((self.value[0]/self.magnitude, self.value[1]/self.magnitude, self.value[2]/self.magnitude))
	
class item:
	Whoami = ''
	def whoami(self):
		return self.Whoami

class trigon(item):
	#polygon; triangle

	Whoami = 'trigon'

	def __init__(self, p1, p2, p3):
		self.points = [p1, p2, p3]
		self.normal = self.normal()

	def normal(self):
		#Vectorize (p1, p2) and (p1, p3)
		vector1 = spvector(self.points[0], self.points[1])
		vector2 = spvector(self.points[0], self.points[2])
		normal = vector(self.cross_product(vector1.value, vector2.value))
		unit_normal = normal.unit_resize()
		return unit_normal

	def cross_product(self, v1, v2):
		v3 = (v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0])
		return v3

	def split(self, point):
		return polygon([point] + self.points)

class polygon(complex):

	def __init__(self, *points):
		self.points = points
		self.trigons = []
		self.initialize()
		if not self.valid(self.trigons):
			raise NotSamePlaneError('Not all trigons are contained in the same plane.')

	def add_points(self, *points):
		self.points.append(points)
		self.initialize()

	def initialize(self):
		self.trigons = []
		pivot = self.points[0]
		for idx, val in enumerate(self.points[1:-1]):
			self.trigons.append(trigon(pivot, val, self.points[1:][idx+1]))

		self.non_overlap_segments()

	def non_overlap_segments(self):
		non_overlap_segments = []
		self.blacklist = []
		for x in [itertools.combinations(trigon.points, 2) for trigon in self.trigons]]:
			for y in x:
				if y not in non_overlap_segments:
					non_overlap_segments.append(y)
				else:
					blacklist.append(y)

		self.non_overlap_segments = []
		for x in non_overlap_segments:
			if x not in self.blacklist:
				self.non_overlap_segments.append(x)

	def valid(trigons):
		for i in range(len(trigons)-1):
			if trigons[i].normal != trigons[i+1].normal:
				return False
		return True

	def ret(self):
		return self.trigons

class complex(item):
	trigons = []
	Whoami = 'complex'

	def ret(self):
		return self.trigons

class figure(complex):
	Whoami = 'figure'


class simple_solid(figure):
	def __init__(self, *points):
		self.points = points
		self.trigons = [trigon(*x) for x in itertools.combinations(self.points, 3)]


class complex_solid(figure):

	def __init__(self, *trigons):
		self.trigons = list(set(trigons))

	def add_simple(self, *simples):
		merge = set(self.trigons)
		for simple in simples:
			merge = set(list(merge) + simple.trigons)

		self.trigons = list(merge)


class cone(simple_solid):
	def __init__(self, polygon, vertex):
		self.trigons = polygon.ret()

		for point_tuple in polygon.non_overlap_segments:
			self.trigons.append(trigon(*point_tuple, vertex))

class solid:
	def __init__(self):
		self.trigon_list = []

	def add(self, *items):
		for idx, val in enumerate(items):
			if val.whoami() == 'figure' or val.whoami() == 'polygon':
				for trigon in val.ret():
					self.trigon_list.append(trigon)
			elif val.whoami() == 'trigon':
				self.trigon_list.append(val)
			else:
				raise ValueError('Item \'%s\' number %s provided does not have a trigon value.' % (val.__name__, idx))


	def output(self):
		export_text = 'solid %s\n' % filename

		for trigon in self.trigon_list:
			export_text += '\tfacet normal %s %s %s\n\t\touter loop\n' % (str(trigon.normal.value[0]), str(trigon.normal.value[1]), str(trigon.normal.value[2]))
			for i in range(3):
				export_text += '\t\t\tvertex %s %s %s\n' % (str(trigon.points[i][0]), str(trigon.points[i][1]), str(trigon.points[i][2]))
			export_text += '\t\tendloop\n\tendfacet\n'

		export_text += 'endsolid'
		return export_text

	def export(self, export_file):
		try:
			f = open(export_file, 'w')

		_tab = '\t'

		filename = export_file.split('/')[-1].split('.')[0]

		export_text = self.output()

		f.write(export_text)
		f.close()
