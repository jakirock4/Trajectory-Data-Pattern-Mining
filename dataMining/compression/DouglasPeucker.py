import math
import pandas as pd, matplotlib.pyplot as plt
from shapely.geometry import LineString
from dataMining.utils.config import Config

class DouglasPeucker():
	"""docstring for DouglasPeucker"""
	def __init__(self, data, pathID):
		super(DouglasPeucker, self).__init__()
		self.data = data
		self.pathID = pathID

	def setPathID(self, pathID):
		self.pathID = pathID

	def getPathID(self):
		return self.pathID

	def setData(self, data):
		self.data = data

	def getData(self):
		return self.data

	def comprimir(self):
		print("Datos de trayectoria: " + self.pathID)
		print("Puntos totales GPS: " + str(self.data.shape[0]))
		coordinates = self.data.as_matrix(columns=Config.coordenadas)
		line = LineString(coordinates)
		tolerance = 0.015
		simplified_line = line.simplify(tolerance, preserve_topology=False)
		print('pares de coordenadas en el conjunto completo de datos: ',len(line.coords))
		print('pares de coordenadas en el conjunto de datos simplificado: ',len(simplified_line.coords))
		print('porcentaje comprimido: ',round(((1 - float(len(simplified_line.coords)) / float(len(line.coords))) * 100), 1))

		datosSimplify = pd.DataFrame(list(simplified_line.coords), columns=Config.coordenadas)
		df=pd.DataFrame(columns=Config.columns)
		#print(datosSimplify)
		#datosSimplify.to_csv(Config.pathCompressed + self.pathID + '.csv', index=False)

		for si_i, si_row in datosSimplify.iterrows():
			#print(si_row["latitude"],",",si_row["longitude"])
			#df = self.data.loc[(self.data.latitude == si_row['latitude']) & (self.data.longitude == si_row['longitude'])]
			#obtener el primer punto coincidente
			#temp = self.data.loc[(self.data.latitude == si_row['latitude']) & (self.data.longitude == si_row['longitude'])].head(1)
			temp = self.data.loc[(self.data.latitude == si_row['latitude']) & (self.data.longitude == si_row['longitude'])]
			df = df.append(temp, ignore_index=True)
			#print(i,temp)
		
		df.to_csv(Config.pathCompressed + self.pathID + '.csv', index=False)

		plt.figure(figsize=(10, 6), dpi=100)
		rs_scatter = plt.scatter(df['longitude'], df['latitude'], c='m', alpha=.4, s=150)
		df_scatter = plt.scatter(self.data['longitude'], self.data['latitude'], c='k', alpha=.3, s=10)
		plt.xlabel('longitud')
		plt.ylabel('latitud')
		plt.title('Conjunto simplificado de puntos de coordenadas vs conjunto completo original')
		plt.legend((rs_scatter, df_scatter), ('Simplicado', 'original'), loc='upper left')
		plt.savefig(Config.pathPlotCompressed + self.pathID + '.png', dpi=500)
		#plt.show()
		plt.close()