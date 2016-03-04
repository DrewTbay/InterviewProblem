""""
By: Drew Reid
Date: May 2, 2015
Purpose: 
	class to make connection to sql
"""
#import custom Config class
from indexExchConfig import db_Config
#import installed connector provided by SQL
import mysql.connector
#import error codesf ro the connector provided by SQL
from mysql.connector import errorcode
#import the csv file layout
import csv

class sqlConn: 	
	db_Conn = None
	db_Cur = None
	db_ConfigInfo = None
	
	#When class is initialized create a database connection
	def __init__(self, configFile):
		#create a Config connection to get the database connection details
		self.db_ConfigInfo = db_Config(configFile)
		db_Login = self.db_ConfigInfo.read_db_Conn()
		try: #to setup connection to local database
			self.db_Conn = mysql.connector.connect(**db_Login)
			self.db_Cur = self.db_Conn.cursor()
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)
			self.db_Conn.close()
		else:			  
			print("Connection to the database successful...")
	
	#function to query the connected database and return the results
	def query(self, query):
		try:
			return self.db_Cur.execute(query)
		except mysql.connector.Error as err:
			print(err)
	
	#create a file for uploading purposes
	def open_db_file(self, file):
		#Get the upload file details from the config file
		db_Path = self.db_ConfigInfo.read_db_Path()+file
		try:
			#try to create or delete records already in the upload file
			return open(db_Path, "w")
		except:
			print("Error opening up file, "+ValueError)
	
	#commit the rows in the upload file to the database table
	def commit_csvfile_to_table(self, file, table):
		try:
			self.db_Cur.execute("LOAD DATA INFILE '"+file+"' INTO TABLE "+table+" FIELDS ENCLOSED BY '"+'"'+"' ESCAPED BY '"+'"'+"'"+" TERMINATED BY ',' LINES TERMINATED BY '\r\n'")
			#commit the above command to the database
			self.db_Conn.commit()
		except mysql.connector.Error as err:
			print(err)
	
	def __del__(self):
		self.db_Conn.close()