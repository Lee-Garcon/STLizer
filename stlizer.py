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


class spvector(object):
	def __init__(self, spoint, p):
		self.value = (p[0] - spoint[0], p[1] - spoint[1], p[2] - spoint[2])
		self.magnitude = math.sqrt(self.value[0]**2 + self.value[1]**2 + self.value[2]**2)

class vector(object):
	def __init__(self, val):
		self.value = val
		self.magnitude = math.sqrt(self.value[0]**2 + self.value[1]**2 + self.value[2]**2)

	def unit_resize(self):
		return vector((self.value[0]/self.magnitude, self.value[1]/self.magnitude, self.value[2]/self.magnitude))

class item:
	whoami = 'item'
	def whoami(self):
		return self.whoami



class trigon(item):
	#polygon; triangle

	whoami = 'trigon'

	def __init__(self, p1, p2, p3):
		self.points = [p1, p2, p3]
		self.normal = self.normal()

	def normal(self):
		#Vectorize (p1, p2) and (p1, p3)
		vector1 = spvector(self.points[0], self.points[1])
		vector2 = spvector(self.points[0], self.points[2])=
		normal = vector(self.cross_product(vector1.value, vector2.value))
		unit_normal = normal.unit_resize()
		return unit_normal

	def cross_product(self, v1, v2):
		v3 = (v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0])
		return v3

	def split(self, point):
		return polygon([point] + self.points)







class polygon(item):
	whoami = 'polygon'

	def __init__(self, *points):
		self.points = points
		self.trigons = []
		self.initialize()
		if not self.valid(self.trigons):
			raise NotSamePlaneError('Not all trigons are contained in the same plane.')

	def valid(trigons):
		for i in range(len(trigons)-1):
			if trigons[i].normal != trigons[i+1].normal:
				return False
		return True

	def add_points(self, *points):
		self.points.append(points)
		self.initialize()

	def initialize(self):
		self.trigons = []
		pivot = self.points[0]
		for idx, val in enumerate(self.points[1:-1]):
			self.trigons.append(trigon(pivot, val, self.points[1:][idx+1]))

	def ret(self):
		return self.trigons







class figure(item):
	trigon = []
	whoami = 'figure'

	def ret(self):
		return self.trigons


class simple_solid(figure):
	def __init__(self, *points):
		self.points = points
		self.trigons = [trigon(*x) for x in itertools.combinations(self.points)]


class complex_solid(figure):

	def __init__(self, *trigons):
		self.trigons = list(set(trigons))

	def add_simple(self, *simples):
		merge = set(self.trigons)
		for simple in simples:
			merge = set(list(merge) + simple.trigons)

		self.trigons = list(merge)



class solid:
	def __init__(self):
		self.polygon_list = []

	def add(self, *items):
		for item in items:
			if item.whoami() == 'figure' or item.whoami() == 'polygon':
				for trigon in item.ret():
					self.polygon_list.append(x)
			elif item.whoami() == 'trigon':
				self.polygon_list.append(item)
			else:
				raise ValueError('Item \'%s\' provided does not have a trigon value.' % item.__name__)


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

		
		
		
def join_simple_solids(sub1, sub2):
	merge = set(sub1.trigons + sub2.trigons)
	return complex_solid(sub1.trigons)


