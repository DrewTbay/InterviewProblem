"""
By: Drew Reid
Date: May 2, 2015
Purpose: 
	class to parse the Config File
"""
#import the configparser
from configparser import ConfigParser

class db_Config:
	
	parser = None
	
	def __init__(self, configFile):
		self.parser = ConfigParser()
		self.parser.read(configFile)
	
	#read the databse connection details
	def read_db_Conn(self, section='mySQL'):
		db = {}
		if self.parser.has_section(section):
			items = self.parser.items(section)
			for item in items:
				db[item[0]] = item[1]
		else:
			raise Exception("{0} not found in the {1} file".format(section, self.file))
		return db
	
	#read the path to the databse upload file
	def read_db_Path(self, section='dbPath'):
		if self.parser.has_section(section):
			return self.parser.get(section, 'path')
		else:
			raise Exception("{0} not found in the {1} file".format(section, self.file))
	
	#get the database upload file name
	def read_db_File(self, section='dbPath'):
		if self.parser.has_section(section):
			return self.parser.get(section, 'file')
		else:
			raise Exception("{0} not found in the {1} file".format(section, self.file))