from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPoint
from geopy.distance import great_circle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import gmplot

class Ddscan():
	"""docstring for Ddscan"""

	def __init__(self, data, mapas, plots, estadisticas):
		super(Ddscan, self).__init__()
		self.data = data
		self.mapas = mapas
		self.plots = plots
		self.estadisticas = estadisticas
		# radio de la tierra en km
		self.kms_per_radian = 6371.0088
		# define épsilon como 0.5 kilómetros, convertidos a radianes para ser usados por haversine
		self.epsilon = 0.5 / self.kms_per_radian

	def getMapas(self):
		return self.mapas

	def setMapas(self, mapas):
		self.mapas = mapas

	def getPlots(self):
		return self.plots

	def setPlots(self, plots):
		self.plots = plots

	def getEstadisticas(self):
		return self.estadisticas

	def setEstadisticas(self, estadisticas):
		self.estadisticas = estadisticas

	def main(self):
		self.data["time"] =  pd.DatetimeIndex(self.data['devicetime']).time
		#print(self.data.head(5))
		print(self.mapas)
		print("Puntos totales GPS: " + str(self.data.shape[0]))
		coords = self.data.as_matrix(columns=['latitude', 'longitude'])
		#print(coords)

		# eps es la distancia máxima que pueden tener los puntos entre sí para ser considerados en un grupo
		# min_samples es el tamaño mínimo del grupo (todo lo demás se clasifica como ruido)
		db = DBSCAN(eps=self.epsilon, min_samples=100, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
		cluster_labels = db.labels_
		# obtener el número de grupos (ignorar las muestras ruidosas a las que se les asigna la etiqueta -1)
		num_clusters = len(set(cluster_labels) - set([-1]))

		print("Agrupado " + str(len(self.data)) + " puntos a " + str(num_clusters) + " grupos")

		# convertir los grupos en una serie de pandas
		clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
		#print(clusters)

		# obtener el punto centroide para cada grupo
		puntosMasCentrico = map(self.obtenerPuntoMasCental, clusters)
		lats, lons = zip(*puntosMasCentrico)
		rep_points = pd.DataFrame({'lon':lons, 'lat':lats})
		#print(rep_points)

		fig, ax = plt.subplots(figsize=[10, 6])


		for i in range(num_clusters):
			if(i== 0):
				rs_scatter = ax.scatter(rep_points['lon'][i], rep_points['lat'][i], c='#99cc99', edgecolor='None', alpha=0.7, s=450)
			else:
				ax.scatter(rep_points['lon'][i], rep_points['lat'][i], c='#99cc99', edgecolor='None', alpha=0.7, s=250)

		"""
		rs_scatter = ax.scatter(rep_points['lon'][0], rep_points['lat'][0], c='#99cc99', edgecolor='None', alpha=0.7, s=450)
		ax.scatter(rep_points['lon'][1], rep_points['lat'][1], c='#99cc99', edgecolor='None', alpha=0.7, s=250)
		ax.scatter(rep_points['lon'][2], rep_points['lat'][2], c='#99cc99', edgecolor='None', alpha=0.7, s=250)
		ax.scatter(rep_points['lon'][3], rep_points['lat'][3], c='#99cc99', edgecolor='None', alpha=0.7, s=150)
		ax.scatter(rep_points['lon'][4], rep_points['lat'][4], c='#99cc99', edgecolor='None', alpha=0.7, s=150)

		"""

		df_scatter = ax.scatter(self.data['longitude'], self.data['latitude'], c='k', alpha=0.9, s=num_clusters - 1)
		ax.set_title('Rastreo completo de GPS vs. clusters DBSCAN')
		ax.set_xlabel('Longitud')
		ax.set_ylabel('Latitud')
		ax.legend([df_scatter, rs_scatter], ['Puntos GPS', 'Centros de grupo'], loc='upper right')

		labels = ['grupo{0}'.format(i) for i in range(1, num_clusters+1)]
		for label, x, y in zip(labels, rep_points['lon'], rep_points['lat']):
		    plt.annotate(
		        label, 
		        xy = (x, y), xytext = (-25, -30),
		        textcoords = 'offset points', ha = 'right', va = 'bottom',
		        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'white', alpha = 0.5),
		        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

		if(num_clusters > 0):
			plt.savefig(self.plots + '.png', dpi=500)
			#plt.show()
			plt.close()
		
		# Obtiene las horas para cada cluster por medio de una heuristica simple
		M = []
		for i in range(num_clusters):
		    hours = np.apply_along_axis(self.myfunc, 1, clusters[i]).tolist()
		    M.append(list(map(int, hours)))


		if(num_clusters > 0):

			fig2, axarr = plt.subplots(num_clusters, sharex=True, figsize=(10,10))

			if type(axarr) is np.ndarray:
				for i in range(num_clusters):
					axarr[i].hist(M[i])
					axarr[i].text(20, 30, "Grupo " + str(i + 1))
				
				axarr[num_clusters - 1].set_xlabel("Horas del dia")
			else:
				axarr.hist(M[i])
				axarr.text(20, 30, "Grupo " + str(i + 1))
				axarr.set_xlabel("Horas del dia")
			
			plt.xticks(np.arange(0, 25, 2.0))
			fig2.text(0.04, 0.5, '# Puntos de GPS', va='center', rotation='vertical')
			plt.savefig(self.estadisticas + '.png', dpi=500)
			#plt.show()
			plt.close()


		"""
		fig, ax = plt.subplots(figsize=[10, 6])

		for i in range(num_clusters):
			if(i== 0):
				rs_scatter = ax.scatter(rep_points['lon'][i], rep_points['lat'][i], c='#99cc99', edgecolor='None', alpha=0.7, s=450)
			else:
				ax.scatter(rep_points['lon'][i], rep_points['lat'][i], c='#99cc99', edgecolor='None', alpha=0.7, s=250)

		
		#rs_scatter = ax.scatter(rep_points['lon'][0], rep_points['lat'][0], c='#99cc99', edgecolor='None', alpha=0.7, s=450)
		#ax.scatter(rep_points['lon'][1], rep_points['lat'][1], c='#99cc99', edgecolor='None', alpha=0.7, s=250)
		#ax.scatter(rep_points['lon'][2], rep_points['lat'][2], c='#99cc99', edgecolor='None', alpha=0.7, s=250)
		#ax.scatter(rep_points['lon'][3], rep_points['lat'][3], c='#99cc99', edgecolor='None', alpha=0.7, s=150)
		#ax.scatter(rep_points['lon'][4], rep_points['lat'][4], c='#99cc99', edgecolor='None', alpha=0.7, s=150)

		df_scatter = ax.scatter(self.data['longitude'], self.data['latitude'], c='k', alpha=0.9, s=num_clusters - 1)
		ax.set_title('Rastreo completo de GPS vs. clusters DBSCAN')
		ax.set_xlabel('Longitud')
		ax.set_ylabel('Latitud')
		ax.legend([df_scatter, rs_scatter], ['Puntos GPS', 'Centros de grupos'], loc='upper right')

		labels = ['Trabajo', 'Hogar', 'Hogar 2']
		for label, x, y in zip(labels, rep_points['lon'][:num_clusters-1], rep_points['lat'][:num_clusters-1]):
		    plt.annotate(
		        label, 
		        xy = (x, y), xytext = (-25, -30),
		        textcoords = 'offset points', ha = 'right', va = 'bottom',
		        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'white', alpha = 0.5),
		        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))



		
		"""
		if(num_clusters > 0):
			gmap = gmplot.GoogleMapPlotter(rep_points['lat'][0], rep_points['lon'][0], 11)
			gmap.plot(self.data.latitude, self.data.longitude)
			gmap.heatmap(rep_points['lat'][:num_clusters], rep_points['lon'][:num_clusters], radius=20)
			gmap.draw(self.mapas + ".html")

	def obtenerPuntoMasCental(self, cluster):
	    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
	    puntoMasCentrico = min(cluster, key=lambda point: great_circle(point, centroid).m)
	    return tuple(puntoMasCentrico)

	def myfunc(self, row):
		t = self.data[(self.data['latitude']==row[0]) & (self.data['longitude']==row[1])]['time'].iloc[0]
		#Convertir de Datetime.time a String
		t = t.strftime("%H:%M:%S")
		return t[:t.index(':')]