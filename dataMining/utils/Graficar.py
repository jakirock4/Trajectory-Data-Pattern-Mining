import gmplot
import matplotlib.pyplot as plt

class Graficar():
	"""docstring for Graficar"""
	def __init__(self, data, pathHTML, pathPNG, titulo):
		super(Graficar, self).__init__()
		self.data = data
		self.pathHTML = pathHTML
		self.pathPNG = pathPNG
		self.titulo = titulo

	def setPathHTML(self, pathHTML):
		self.pathHTML = pathHTML

	def getPathHTML(self):
		return self.pathHTML

	def setPathPNG(self, pathPNG):
		self.pathPNG = pathPNG

	def getPathPNG(self):
		return self.pathPNG

	def setTitutlo(self, titutlo):
		self.titutlo = titutlo

	def getTitutlo(self):
		return self.titutlo

	def setData(self, data):
		self.data = data

	def getData(self):
		return self.data

	def mapear(self):
		#print(self.data)
		gmap = gmplot.GoogleMapPlotter(self.data.latitude[0], self.data.longitude[0], 11)
		gmap.plot(self.data.latitude, self.data.longitude)
		gmap.draw(self.pathHTML + ".html")

	def plotMapear(self):
		plt.plot(self.data.longitude, self.data.latitude, linewidth=0.5)
		plt.title(self.titulo)
		# y finalmente guardarlo con alta resolución.
		plt.savefig(self.pathPNG + '.png', dpi=500)
		plt.close()