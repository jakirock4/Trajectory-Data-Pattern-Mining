import pandas as pd
import mysql.connector as sql
from dataMining.utils.config import Config

class Data():
	"""docstring for Data"""
	def __init__(self):
		super(Data, self).__init__()

	def setPathID(self, pathID):
		self.pathID = pathID

	def getPathID(self):
		return self.pathID

	def infoMysql(self):
	    db_connection = sql.connect(host=Config.host,user=Config.user,passwd=Config.password, db=Config.database)
	    db_cursor = db_connection.cursor()
	    #db_cursor.execute('SELECT id, deviceid, valid, latitude, longitude, fixtime, speed, attributes FROM tc_positions WHERE deviceid BETWEEN 15 AND 20')
	    """
	    SELECT COUNT(*) FROM tc_positions WHERE deviceid = 20                                          -> 124297
		SELECT COUNT(*) FROM tc_positions WHERE deviceid = 20 GROUP BY attributes                      -> 15654
		SELECT COUNT(*) FROM tc_positions WHERE deviceid = 20 GROUP BY longitude, latitude, fixtime    -> 121308
		SELECT COUNT(*) FROM tc_positions WHERE deviceid = 20 GROUP BY longitude, latitude             -> 32996
		SELECT COUNT(*) FROM tc_positions WHERE deviceid = 20 GROUP BY longitude, latitude, attributes -> 33744
		"""
	    db_cursor.execute('SELECT id, deviceid, valid, latitude, longitude, fixtime, speed, attributes FROM tc_positions WHERE deviceid BETWEEN 15 AND 20 GROUP BY longitude, latitude, attributes')
	    table_rows = db_cursor.fetchall()
	    db_cursor.execute('SELECT DISTINCT(deviceid) FROM tc_positions')
	    id = db_cursor.fetchall()
	    columna = pd.DataFrame(id)
	    columna.columns = ["deviceid"]
	    df = pd.DataFrame(table_rows)
	    df.columns = Config.columns
	    columna.to_csv(Config.pathFull + "trajectoriesID.csv", index=False,header=True)

	    for val in columna.deviceid:
	    	data = df.loc[df.deviceid == val]
	    	if (len(data) != 0):
	    		data.to_csv(Config.pathFull + str(val) + ".csv", index=False,header=True)

	def readCSV(self):
		#print(self.pathID + ".csv")
		datos = pd.read_csv(self.pathID + ".csv" ,header=1,names=Config.columns,index_col=False)
		return datos

