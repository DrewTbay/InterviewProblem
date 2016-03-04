""""
By: Drew Reid
Date: May 2, 2015
Purpose: 
	test the report functionality
"""

#import the system date and time
import datetime
#import Custom database Connection
from indexExchDataBaseConn import sqlConn
#import the csv file layout
import csv

#Get yesterday's date and format it in the standard SQL format YYYY-MM-DD
deltaDate = (datetime.datetime.now().date() + datetime.timedelta(-1)).strftime('%Y-%m-%d')


#connect the the database using the the attached ConfigFile
db_Connect = sqlConn('configFiles\iniIndexExch.ini')

#Delete all information current in the mailing table
db_Connect.query("TRUNCATE mailing")
#Delete all information current in the domainOccurrence table
db_Connect.query("TRUNCATE domainOccurrence")


#Open the upload file
domainFile = db_Connect.open_db_file('domainOccurrence.csv')
#Create a csv writer
csvDomainFile = csv.writer(domainFile)

i = 0
while i <= 60:
	csvDomainFile.writerow(["domain"+str(i)+".com",100,deltaDate])
	i+=1

domainFile.close()
db_Connect.commit_csvfile_to_table('domainOccurrence.csv', "domainOccurrence")

#Open the upload file
domainFile = db_Connect.open_db_file('mailing.csv')

i = 1
while i <= 60:
	j = 1
	while j <= i:
		domainFile.write('"emailTest@domain'+str(i)+'.com"\n')
		j+=1
	i+=1
	
domainFile.close()
db_Connect.commit_csvfile_to_table('mailing.csv', "mailing")