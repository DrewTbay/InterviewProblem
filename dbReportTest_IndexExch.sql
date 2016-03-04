#make sure we are using our test database
USE IndexExch;

#turn off safe updates
SET SQL_SAFE_UPDATES = 0;

#clear the test tables
DELETE FROM mailing;
DELETE FROM domainOccurrence;

#run the python generator file: indexExhReportTest.py or indexExhDataTest.py
LOAD DATA INFILE "domainOccurrenceTest.csv" INTO TABLE domainOccurrence FIELDS TERMINATED BY ',';
LOAD DATA INFILE "mailingTest.csv" INTO TABLE mailing FIELDS ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n';

SELECT * FROM mailing;
SELECT * FROM domainOccurrence;