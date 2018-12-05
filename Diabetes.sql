-- Create a database called diabetes_db --
DROP DATABASE IF EXISTS diabetes_db;
CREATE DATABASE diabetes_db;

-- Use diabetes_db to create tables --
USE diabetes_db;

-- Create tables within the database --

CREATE TABLE obesity(
	ID int primary key not null auto_increment,
    `Year`text,
	US_State text,
    Obese_Children_Percent float
);

CREATE TABLE diabetes(
	ID int primary key not null auto_increment,
    `Year` text,
    US_State text,
    Adult_Diabetics_Percent float
);

-- View tables --
SELECT * FROM diabetes;
SELECT * FROM obesity;

-- Join tables --
SELECT 
	t1.`Year`,
    t1.US_State,
    t1.Adult_Diabetics_Percent,
    t2.Obese_Children_Percent
FROM diabetes as t1
JOIN obesity as t2 on t1.US_State = t2.US_State;





