# Code Challenge: Salary Per Hour by Kevin Susantio

There are 2 main files in this repo: etl.py and sql_file.sql

etl.py is a python script that extracts data from CSV files, transforms the data, and loads it into a MySQL database. The script is designed for batch processing of daily data and can be customized to include a date identifier in the file names.

sql_file.sql is the SQL query used for find the salary per hour of every branch_id grouped by the year and month.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Data Sources](#data-sources)
- [Configuration](#configuration)
- [Transformations](#transformations)
- [Loading Data](#loading-data)
- [Append Data](#append-data)
- [Salary Per Hour Analysis](#salary-per hour-analysis)

## Introduction

This Python script is designed to perform Extract, Transform, and Load (ETL) operations on employee and timesheet data from CSV files into a MySQL database.

## Prerequisites

Before running the script, ensure you have the following prerequisites:

- Python: You need a Python environment (Python 3 recommended) installed on your system.

- Required Python Packages: You should have the following Python packages installed. You can install them using `pip`:

  - `pandas`
  - `SQLAlchemy`
  - `pymysql`

- MySQL Database: You should have access to a MySQL database where the data will be loaded. I used the MySQL workbench and MySQL in XAMPP running on my local machine.

## Getting Started

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/kevinsusantio21/mekari_kevin.git

2. **Running the Python ETL Script:**
   
   ```bash
   python etl.py
This command will execute the Python ETL script, extracting data from CSV files, transforming it, and loading it into the MySQL database.

## Data Sources
**CSV Files**:

The script assumes the presence of two CSV files: "employees.csv" and "timesheets.csv." These files contain the data to be loaded into the database.

employees.csv: Contains employee data.

timesheets.csv: Contains timesheet data.

Ensure that these files are in the same directory as the script.

## Configuration
Before running the script, you should configure the script to match your database settings. Open the script and modify the mysql_config dictionary to specify your MySQL database connection details:

```
mysql_config = {
    "user": "your_username",
    "password": "your_password",
    "host": "your_host",
    "port": 3306,  # Default MySQL port
    "database": "your_database",
}
```

Replace "your_username", "your_password", "your_host", and "your_database" with your MySQL database credentials.

## Transformations
The script performs the following transformations on the timesheets data:

Converts the "checkin" and "checkout" columns to HH:mm:ss format.

## Loading Data
The script loads the transformed data into the following tables in the MySQL database:

**employees**: Contains employee data.

**timesheets**: Contains timesheet data.

## Append Data
By default, the script appends data to the existing tables in the MySQL database. If the tables do not exist, they will be created. If you want to perform other actions, you can modify the if_exists parameter in the to_sql method in the script.

## Salary Per Hour Analysis
The script includes an SQL query for data analysis. The query calculates the salary_per_hour for each employee and summarizes the results by year, month, and branch. Here is the SQL query:

```
SELECT
    r.year,
    r.month,
    r.branch_id,
    ROUND(SUM(r.salary) / SUM(r.hours_worked)) AS salary_per_hour
FROM
(
    SELECT 
        t.employee_id,
        e.branch_id,
        CASE WHEN t.employee_id = '218078'
            THEN 13000000
            ELSE e.salary
        END AS salary,
        LEFT(t.date, 4) AS year,
        SUBSTRING(t.date, 6, 2) AS month,
        SUM(TIME_TO_SEC(IFNULL(t.checkout, '17:00:00')) - TIME_TO_SEC(IFNULL(t.checkin, '09:00:00')))/3600.0 AS hours_worked,
        e.salary / (SUM(TIME_TO_SEC(IFNULL(t.checkout, '17:00:00')) - TIME_TO_SEC(IFNULL(t.checkin, '09:00:00')))/3600.0) AS salary_per_hour
    FROM timesheets t
    INNER JOIN employees e
    ON t.employee_id = e.employe_id
    GROUP BY t.employee_id, e.branch_id, year, month, e.salary
) r
GROUP BY r.branch_id, r.year, r.month
ORDER BY r.year, r.month, r.branch_id;
```
**Some Query Explanation**
```
IFNULL(t.checkin, '09:00:00')
IFNULL(t.checkout, '17:00:00')
```
This query is used to assume that each employee that didn't do check-in or check-out is set to default:
Check-in: 9 am
Check-out: 5 pm
Assuming that the working hour is 9 to 5
```
CASE WHEN t.employee_id = '218078'
    THEN 13000000
    ELSE e.salary
END AS salary, 
```
When analyzing the employee data, I found that employee_id 218078 has 2 records with 2 different salary: 13.000.000 and 10.500.000.

To improve the data accuracy, I assumed that the current salary is 13.000.000

You can customize this query to suit your data analysis needs.