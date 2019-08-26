import os
import pandas as pd
import numpy as np
import gmplot
import geopy.distance
from dipy.segment.metric import Metric
from dipy.segment.metric import ResampleFeature
from dipy.segment.clustering import QuickBundles
from scipy.spatial.distance import directed_hausdorff
import datetime

class QuickBundlesAlgorit():
	"""docstring for QuickBundlesAlgorit"""
	def __init__(self, arg):
		super(QuickBundlesAlgorit, self).__init__()
		self.arg = arg
		self.color_list = ['brown','orange', 'red', 'black', 'blue', 'green', 'yellow', 'gold', 'cornflowerblue','darkgreen','tomato','oldlace',
	                  'chocolate','crimson','darkorange','gray','lightblue','midnightblue','aliceblue','beige','darkmagenta','teal',
	              'deepskyblue','orchid', 'darkred','palegoldenrod','palegreen','paleturquoise','palevioletred','papayawhip','peachpuff','peru','pink','plum',]  # Aumenta el color según el tipo de clúster
		
	def read_car_file(self, filepath):
	    """Lea el archivo del automóvil y obtenga los datos de latitud, longitud y matrícula"""
	    df_trips = pd.read_hdf(filepath, key='trips')
	    df_trips.set_index(['plate'], inplace=True)
	    df_trips = df_trips[['y','x']]

	    return df_trips

	def get_car_plate(self, df_trips):
	    """Obtenga una lista de placas de servicio"""
	    car_plate = []
	    for plate in df_trips.index:
	        car_plate.append(plate)
	    car_plate = set(car_plate)

	    return car_plate

	def get_car_streams(self, df_trips, car_plate):
	    """Obtén la pista del auto"""
	    streams = []
	    for car in car_plate:
	        streams.append(df_trips.loc[car].as_matrix())

	    return streams

	"""Algoritmo de agrupamiento basado en QuickBundles"""
	def pick_trip(self, streams,index):
	    """Seleccione algunas pistas para guardar en csv"""
	    save_trip = pd.DataFrame(streams[index])
	    save_trip.to_csv('./cluster_trips/trip_'+str(index)+'.csv')

	def qb_cluster(self, streams,threshold,metric):
	    """Agrupación Qb: cuanto mayor es el umbral, se obtienen menos agrupaciones."""
	    qb = QuickBundles(threshold=threshold, metric=metric)
	    clusters = qb.cluster(streams)
	    print("clusters number:", len(clusters))
	    return clusters


	"""Elija la pista central del grupo"""
	def hausdorff(self,  u, v):
	    """Calcular agrupamiento entre pistas"""
	    d = max(directed_hausdorff(u, v)[0], directed_hausdorff(v, u)[0])
	    return d

	def generate_dis_mat(self, streams):
	    """Generar una matriz de distancia entre las trayectorias."""
	    traj_count = len(streams)
	    D = np.zeros((traj_count, traj_count))

	    # This may take a while
	    for i in range(traj_count):
	        for j in range(i + 1, traj_count):
	            distance = self.hausdorff(streams[i], streams[j])
	            D[i, j] = distance
	            D[j, i] = distance
	    return D

	def get_cluster_center_trip(self, clusters, D,cls_index):
	    """Obtenga el índice de la pista central de cada grupo de clúster"""
	    dis_dir = {}
	    tri_index_list = []
	    #Genere una lista de índices de seguimiento para cada tipo de clúster
	    for tri_index in clusters[cls_index].indices:
	        tri_index_list.append(tri_index)

	    # Extraiga las filas y columnas de la matriz asociada.
	    simp_D = pd.DataFrame(D)[tri_index_list][tri_index_list]#Convierta la matriz en una matriz df y extraiga las filas y columnas relevantes
	    #获取行和列和
	    D_row = simp_D.apply(sum)
	    D_col = simp_D.T.apply(sum)
	    #Calcular la suma de una pista a otras pistas en la clase
	    for tri_index in clusters[cls_index].indices:
	        print(tri_index)
	        sum_dis = D_row[tri_index] + D_col[tri_index]
	        print(sum_dis)
	        dis_dir[tri_index] = sum_dis
	    #Devuelve el índice del mínimo
	    min_trip_index = min(dis_dir, key=dis_dir.get)

	    return min_trip_index

	def save_trip(self, streams,index):
	    """Guardar pistas seleccionadas en csv"""
	    save_trip = pd.DataFrame(streams[index])
	    save_trip.to_csv('./clusters_center_trips1/trip_' + str(index) + '.csv')

	def map_plot(self, streams,clusters,cluster_name):
	    """Visualice resultados de agrupamiento en el mapa"""
	    clusterIndex = len(clusters)
	    gmap = gmplot.GoogleMapPlotter(streams[0][0, 0], streams[0][0, 1], 12)
	    for index in range(clusterIndex):
	        for j in clusters[index].indices:
	            gmap.plot(streams[j][:, 0], streams[j][:, 1],self.color_list[index], edge_width=2)
	    gmap.draw("./mapResult1/map_cluster_"+cluster_name+".html")

	def single_trip_plot(self, streams,index):
	    gmap = gmplot.GoogleMapPlotter(streams[0][0, 0], streams[0][0, 1], 12)
	    gmap.plot(streams[index][:, 0], streams[index][:, 1], 'orange', edge_width=4)
	    gmap.draw("./tripResult1/center_trip_"+str(index)+".html")

class GPSDistance(Metric):

    def __init__(self):
        super(GPSDistance, self).__init__(feature=ResampleFeature(nb_points=288))

    def are_compatible(self, shape1, shape2):
        return len(shape1) == len(shape2)

    def dist(self, v1, v2):
        x = [geopy.distance.vincenty([p[0][0],p[0][1]], [p[1][0],p[1][1]]).km for p in list(zip(v1,v2))]
        currD = np.mean(x)
        return currD


if __name__ == "__main__":
	obj = QuickBundlesAlgorit("algo")
	#Leer datos
	start_time = datetime.datetime.now()
	filepath1 = 'cargo_0701_valid.h5'
	os.mkdir("mapResult1")
	os.mkdir('clusters_center_trips1')
	os.mkdir("tripResult1")
	df_trips = obj.read_car_file(filepath1)
	car_plate = obj.get_car_plate(df_trips)
	streams = obj.get_car_streams(df_trips, car_plate)
	streams_num = []
	for i in range(len(streams)):
		streams_num.append(len(streams[i]))

	print("Trayectoria total:{}".format(len(streams)))
	print("Puntos de seguimiento promedio:{}".format(sum(streams_num) / len(streams)))
	# Algoritmo de agrupación Qb
	metric = GPSDistance()
	threshold = 7.5 #Parámetro de ajuste
	cluster_name = 'QuickBundles_th_' + str(threshold)
	clusters = obj.qb_cluster(streams, threshold, metric)
	obj.map_plot(streams, clusters, cluster_name)
	#Seleccionar pista central del clúster
	D = obj.generate_dis_mat(streams)

	min_trip_index_list = []
	for index in range(len(clusters)):
		min_trip_index = obj.get_cluster_center_trip(clusters, D,index)
        min_trip_index_list.append(min_trip_index)
	
	#Guarde la pista central en la carpeta clusters_center_trips
	for index in min_trip_index_list:
		obj.save_trip(streams,index)
		obj.single_trip_plot(streams,index)

	end_time = datetime.datetime.now()
	print("El programa se ejecuta con éxito, en tiempo total.：{}".format(end_time -start_time))
