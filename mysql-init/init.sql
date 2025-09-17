CREATE DATABASE IF NOT EXISTS studentsdb;
USE studentsdb;

CREATE TABLE students(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100), email VARCHAR(100));
INSERT INTO students VALUES(1, "Testing", "test@gmail.com");
