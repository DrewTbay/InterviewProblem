#make sure we are using our test database
USE IndexExch;

#turn off safe updates
SET SQL_SAFE_UPDATES = 0;

#clear the test tables
DELETE FROM mailing;
DELETE FROM domainOccurrence;

#check to see if borders are correct
INSERT INTO mailing VALUES ('test1@domain3.com');
INSERT INTO mailing VALUES ('test1@domain3.com');
INSERT INTO mailing VALUES ('test1@domain3.com');
INSERT INTO mailing VALUES ('test1@domain3.com');

#check to see if report only displays domains that have occurred at least 30 days ago.
INSERT INTO mailing VALUES ('test1@domain1.com');
INSERT INTO mailing VALUES ('test2@domain1.com');

#check to see if the report does not displays new domains that have never been logged before.
INSERT INTO mailing VALUES ('test1@domain2.com');

#check to see if incorrect email addresses are excluded from the report
INSERT INTO mailing VALUES ('nodomain@');
INSERT INTO mailing VALUES ('nodomain');
INSERT INTO mailing VALUES ('@noemail.com');
INSERT INTO mailing VALUES ('noemail.com');

#Border test
INSERT INTO domainOccurrence (domainName, domainCount, domainDay) VALUES ('domain3.com', 1, DATE_ADD(NOW(), INTERVAL -30 DAY)); #should be included
INSERT INTO domainOccurrence (domainName, domainCount, domainDay) VALUES ('domain3.com', 2, DATE_ADD(NOW(), INTERVAL -29 DAY)); #should be included
INSERT INTO domainOccurrence (domainName, domainCount, domainDay) VALUES ('domain3.com', 3, DATE_ADD(NOW(), INTERVAL -31 DAY)); #should not included

#Out of scope date test
INSERT INTO domainOccurrence (domainName, domainCount, domainDay) VALUES ('domain2.com', 1, DATE_ADD(NOW(), INTERVAL -31 DAY)); #should not included
INSERT INTO domainOccurrence (domainName, domainCount, domainDay) VALUES ('domain3.com', 2, DATE_ADD(NOW(), INTERVAL -2 MONTH)); #should not included
INSERT INTO domainOccurrence (domainName, domainCount, domainDay) VALUES ('domain3.com', 3, DATE_ADD(NOW(), INTERVAL -1 YEAR)); #should not included

SELECT * FROM mailing;
SELECT * FROM domainOccurrence;