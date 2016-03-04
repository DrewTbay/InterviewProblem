"""
By: Drew Reid
Date: May 2, 2015
Purpose: 
-Completed the desired result for the Index Exchange test.
-First ever python Program.
-After 10 days of learning python I have coded the following.

Tools/Programs used:

Python 3.4.3
MySQL 5.6
MySQL connector python 2.0.4-py3.4-py

Other products/resources needed:

7-Zip 9.20

Started: 11am on Saturday
1pm Lunch
2pm back
3:30pm. first test case successful. small break.
3:45pm. back starting the report testing.
5:15pm report testing complete.
6:00pm finished code check and re-run of testing.
7:00pm change database connector to accept config file for the connection to be more re-usable.
8:00pm changed database commit of csv file to be more dynamic and re-usable
9:00pm re-test, proof read code, and submit code.

total Hours: ~10hrs
"""

#import Custom database Connection
from indexExchDataBaseConn import sqlConn
#import String
import string
#import the system date and time
import datetime
#import defaultdict
from collections import defaultdict
#import the csv file layout
import csv

#Declare variables and lists needed for script

#Get current date and format it in the standard SQL format YYYY-MM-DD
curDate = (datetime.datetime.now().date()).strftime('%Y-%m-%d')
#Get Date 30 days ago and format it in the standard SQL format YYYY-MM-DD
deltaDate = (datetime.datetime.now().date() + datetime.timedelta(-30)).strftime('%Y-%m-%d')
#we will store the domain count in the domain dictionary
domainDict = defaultdict(int)
report = list()
uploadFile = 'domains.csv'

print ("Attempting to connect to database...")
#connect the the database using the the attached ConfigFile
db_Connect = sqlConn('configFiles\iniIndexExch.ini')

db_Connect.query("SELECT addr FROM mailing") #Query the mailing table

#loop through the Query results
for (addr) in db_Connect.db_Cur:
	try: #to find the @ symbol in the string
		temp = ''.join(addr).split('@') #convert the tuple to string then split on @
		if len(temp) == 2: #if more then 1 or no @ symbol is found, display error, move to next addr record
			(email, domain) = temp
			#if either domain or email is blank address is invalid 
			if not domain or not email:
				print ("Format issue with the email address domain:"+ ''.join(addr))
			else:
				domainDict[domain] += 1
		else:
			print ("Format issue with the email address domain:"+ ''.join(addr))
	except ValueError:
		print ("The address does not have a domain: "+ ''.join(addr))

print("Create Upload file...")
#Open the upload file
domainFile = db_Connect.open_db_file(uploadFile)
#Create a csv writer
csvDomainFile = csv.writer(domainFile)

print("Loop through collected Domains...")
for domain in domainDict: #for each unique domain found in the mailing table do the following
	domainCurrCount = domainDict[domain]	
	#insert the count for each domain for the current day into domainOccurrence
	domainCount = str(domainCurrCount)
	csvDomainFile.writerow([domain,domainCount,curDate])
		
	#for each domain collect the number of times the domain was counted the last 30 days
	domainPastCount = 0
	db_Connect.query("SELECT domainCount FROM domainOccurrence WHERE domainName = '"+domain+"' AND  domainDay >= '"+deltaDate+"' AND domainDay < '"+curDate+"'")
	#add the count on each day together
	
	for row in db_Connect.db_Cur:
		domainPastCount = row[0] + domainPastCount
	
	#if the domain has not occured in the past 30 days the percentage growth would be infinite because of the fact we would divide by 0. As such, we skip over these domains
	if domainPastCount != 0:
		domainCurrCount = (domainCurrCount+domainPastCount)
		#percentage Growth calulation: (Current Count - Past Count)/Past Count
		perGrowth = round((domainCurrCount - domainPastCount)/domainPastCount *100) #rounding to show whole precentages
		#keep track of all domain precentage growth
		loc = 0
		#if the lenght of the report is empty, add the first element
		if len(report) == 0:
			report.append([domain,perGrowth,domainCurrCount])
		else:
			#loop through the report
			for rows in report:
				#if the current domain count is greater than the row domain count
				if domainCurrCount > rows[2]:
					#insert into report
					report.insert(loc, [domain,perGrowth,domainCurrCount])
					#break loop on report
					break
				else:
					#increase location by one
					loc +=1
			#if the location is equal to the report and the location is currently under 50 than
			if loc == len(report) and loc < 50:
				#add the item on the end of the report
				report.append([domain,perGrowth,domainCurrCount])
			#final check to see if the report has over 50 elements
			if len(report) > 50:
				#if so remove last element
				report.pop()

print("Commit Upload file to database...")

#close the database upload file
domainFile.close()

#Commit the upload file to the database
db_Connect.commit_csvfile_to_table(uploadFile, "domainOccurrence")

print("Report the top 50 domains by count. Sort this report by percentage growth of the last 30 days.")				

#sort the report by precentage growth in descending order
report.sort(key=lambda x: x[1], reverse=True)

#Write the results to a report file
file = open("report_"+curDate+".csv", 'w')
csvFile = csv.writer(file)
csvFile.writerow(["Domain", "Precentage Growth", "Count"])

for rows in report:
	csvFile.writerow(rows)

file.close()

print("Clear Input file of data, so we do not re-read any addresses...")
#The script is now done the process. Clear the mailing table to not re-read any addresses from today.
db_Connect.query("TRUNCATE mailing")

print("Process is completed successfully.")	
