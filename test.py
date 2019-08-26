import os
import pandas as pd
from dataMining.utils.data import Data
from dataMining.utils.config import Config
from dataMining.utils.Graficar import Graficar
from dataMining.compression.DouglasPeucker import DouglasPeucker
from dataMining.clustering.Ddscan import Ddscan

class Test(object):
	"""docstring for Test"""
	def __init__(self):
		super(Test, self).__init__()


	def datos(self):
		# Guardar los datos de Mysql a un csv
	    # Data.infoMysql(self)
	    # LEER TODOS LOS DATOS

	    listaArchivo = os.listdir(Config.pathFull)
	    for path in listaArchivo:
	    	if (path != "trajectoriesID.csv" and path != ".DS_Store"):
	    		path = path.replace(".csv", "")
	    		info = Data()
	    		info.setPathID(Config.pathFull + path)
	    		data = info.readCSV()
	    		graficar = Graficar(data, Config.pathMapsFull + path, Config.pathPlotMapsFull + path, "Rutas sin procesar")
	    		graficar.mapear()
	    		graficar.plotMapear()
	    		compresion = DouglasPeucker(data, path)
	    		compresion.comprimir()
	    		print("")
	    		print("")
	    		print("")
	    		print("")
	    		console.log("error")

	    		
	    """

	    # LEER LOS DATOS COMPRIMIDOS
	    listaArchivoComprimidos = os.listdir(Config.pathCompressed)
	    for path in listaArchivoComprimidos:
	    	if (path != "trajectoriesID.csv" and path != ".DS_Store"):
	    		path = path.replace(".csv", "")
	    		info = Data()
    			info.setPathID(Config.pathCompressed + path)
    			data = info.readCSV()
    			graficar = Graficar(data, Config.pathMapsCompressed + path, Config.pathPlotMapsCompressed + path, "Rutas comprimidas")
    			graficar.mapear()
    			graficar.plotMapear()
    			#"""
    	# LEER LOS DATOS COMPRIMIDOS
"""
	    listaArchivoComprimidos = os.listdir(Config.pathCompressed)
	    for path in listaArchivoComprimidos:
	    	if (path != "trajectoriesID.csv" and path != ".DS_Store"):
	    		path = path.replace(".csv", "")
	    		info = Data()
    			info.setPathID(Config.pathCompressed + path.replace(".csv", ""))
    			data = info.readCSV()
    			cluster = Ddscan(data, Config.pathClusterDBSCANMapas + path, Config.pathClusterDBSCANPlots + path, Config.pathDBSCANEstadis + path)
    			cluster.main()
    			"""
if __name__ == '__main__':
    testeo = Test()
    testeo.datos()