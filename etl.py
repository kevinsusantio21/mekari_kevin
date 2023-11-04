import pandas as pd
from sqlalchemy import create_engine
import pymysql

# For batch processing daily, the csv file could be added date identifier, 
# for example employees_2023-11-02.csv, thus the file format employees_{date}.csv
# Later the {date} variable can be parameterized

# Extract employees csv to pandas dataframe
pd_df_employees = pd.read_csv("employees.csv")

# Extract timesheets csv to pandas dataframe
pd_df_timesheets = pd.read_csv("timesheets.csv")

# Transform checkin checkout column to HH:mm:ss format
pd_df_timesheets["checkin"] = pd.to_datetime(pd_df_timesheets["checkin"]).dt.strftime("%H:%M:%S")
pd_df_timesheets["checkout"] = pd.to_datetime(pd_df_timesheets["checkout"]).dt.strftime("%H:%M:%S")

# Setup MySQL config (mine is localhost)
mysql_config = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "port": 3306,
    "database": "mkr",
}

# Create SQLAlchemy engine to connect to MySQL database
engine = create_engine((f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['database']}"))

# Load employees dataframe to table employees
pd_df_employees.to_sql(
    name="employees",
    con=engine,
    if_exists="append",
    index=False,
)

# Load timesheets dataframe to table timesheets
pd_df_timesheets.to_sql(
    name="timesheets",
    con=engine,
    if_exists="append",
    index=False,
)