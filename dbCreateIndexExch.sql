CREATE DATABASE IndexExch;

#create a custom user so we do not need to use root
CREATE USER 'testIndEx'@'localhost' IDENTIFIED BY 'indexExchange';

USE IndexExch;

#the table I cannot manipulate
CREATE TABLE mailing (
	addr VARCHAR(255) NOT NULL
);

#Custom created table
CREATE TABLE domainOccurrence(
    domainName VARCHAR(255) NOT NULL,
    domainCount INT,
	domainDay DATE
);

#Grant custom user the insert, delete, file, and query commands on the database
GRANT DROP, DELETE, INSERT, SELECT, UPDATE ON IndexExch.* TO 'testIndEx'@'localhost';
grant file on *.* to 'testIndEx'@'localhost';
