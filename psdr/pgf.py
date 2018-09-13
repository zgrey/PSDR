#provides a class for dumping tab separated files for PGF
from matplotlib.path import Path

class PGF:
	def __init__(self):
		self.column_names = []
		self.columns = []
	def add(self, name, column):
		if len(self.columns) > 1:
			assert len(self.columns[0]) == len(column)

		self.columns.append(column)
		self.column_names.append(name)


	def write(self, filename):
		f = open(filename,'w')

		for name in self.column_names:
			f.write(name + '\t')
		f.write("\n")		

		for j in range(len(self.columns[0])):
			for col in self.columns:
				f.write("{}\t".format(float(col[j])))
			f.write("\n")

		f.close()



def save_contour(fname, cs, fmt = 'matlab', **kwargs):
	""" Save a contour plot to a file for pgfplots

	Additional arguments are passed to iter_segements
	Important, simplify = True will remove invisible points
	"""

	def write_path_matlab(fout, x_vec, y_vec, z):
		# Now dump this data back out
		# Header is level followed by number of rows
		fout.write('%15.15e\t%15d\n' % (z, len(x_vec)))
		for x, y in zip(x_vec, y_vec):
			fout.write("%15.15e\t%15.15e\n" % (x,y))

	def write_path_prepared(fout, x_vec, y_vec, z):
		fout.write("%15.15e\t%15.15e\t%15.15e\n" % (x0,y0,z))
		fout.write("\t\t\t\n")

	if fmt == 'matlab':
		write_path = write_path_matlab
	elif fmt == 'prepared':
		write_path = write_path_prepared
	else:
		raise NotImplementedError

	with open(fname, 'w') as fout:
		for col, z in zip(cs.collections, cs.levels):
			for path in col.get_paths():
				x_vec = []
				y_vec = []
				for i, ((x,y), code) in enumerate(path.iter_segments(**kwargs)):
					if code == Path.MOVETO:
						if len(x_vec) !=0:
							write_path(fout, x_vec, y_vec, z)
							x_vec = []
							y_vec = []
						x_vec.append(x)
						y_vec.append(y)
					
					elif code == Path.LINETO:
						x_vec.append(x)
						y_vec.append(y)

					elif code == Path.CLOSEPOLY:
						x_vec.append(x_vec[0])
						y_vec.append(y_vec[0])
					else:
						print "received code", code

				write_path(fout, x_vec, y_vec, z)