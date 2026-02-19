# 1 Ensure connected to server
# 2 Does DB exist?
# 3 Create The database
# 4 Create the tables
# 5 insert .csv
# 6 Clean up and print "all done"

import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()


def test_connection():
    # 1
    F1_DB = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    cursor = F1_DB.cursor()

    # 2 & 3
    db_name = os.getenv("DB_NAME")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")
    print(f"Using databese: {db_name}")

    # 4
    TABLES = {}

    TABLES["circuits"] = (
        "CREATE TABLE IF NOT EXISTS circuits ("
        "  circuitId INT PRIMARY KEY,"
        "  circuitRef VARCHAR(255),"
        "  name VARCHAR(255),"
        "  location VARCHAR(255),"
        "  country VARCHAR(255),"
        "  lat FLOAT,"
        "  lng FLOAT,"
        "  alt INT"
        ")"
    )

    TABLES["drivers"] = (
        "CREATE TABLE IF NOT EXISTS drivers ("
        "  driverId INT PRIMARY KEY,"
        "  driverRef VARCHAR(255),"
        "  number VARCHAR(255),"
        "  code VARCHAR(255),"
        "  forename VARCHAR(255),"
        "  surname VARCHAR(255),"
        "  dob DATE,"
        "  nationality VARCHAR(255)"
        ")"
    )

    TABLES["constructors"] = (
        "CREATE TABLE IF NOT EXISTS constructors ("
        "  constructorId INT PRIMARY KEY,"
        "  constructorRef VARCHAR(255),"
        "  name VARCHAR(255),"
        "  nationality VARCHAR(255)"
        ")"
    )

    TABLES["status"] = (
        "CREATE TABLE IF NOT EXISTS status ("
        "  statusId INT PRIMARY KEY,"
        "  status VARCHAR(255)"
        ")"
    )

    TABLES["races"] = (
        "CREATE TABLE IF NOT EXISTS races ("
        "  raceId INT PRIMARY KEY,"
        "  year INT,"
        "  round INT,"
        "  circuitId INT,"
        "  name VARCHAR(255),"
        "  date DATE,"
        "  time TIME,"
        "  FOREIGN KEY (circuitId) REFERENCES circuits(circuitId)"
        ")"
    )

    TABLES["lap_times"] = (
        "CREATE TABLE IF NOT EXISTS lap_times ("
        "  raceId INT,"
        "  driverId INT,"
        "  lap INT,"
        "  position INT,"
        "  time VARCHAR(255),"
        "  milliseconds INT,"
        "  PRIMARY KEY (raceId, driverId, lap),"
        "  FOREIGN KEY (raceId) REFERENCES races(raceId),"
        "  FOREIGN KEY (driverId) REFERENCES drivers(driverId)"
        ")"
    )

    TABLES["pit_stops"] = (
        "CREATE TABLE IF NOT EXISTS pit_stops ("
        "  raceId INT,"
        "  driverId INT,"
        "  stop INT,"
        "  lap INT,"
        "  time TIME,"
        "  duration VARCHAR(255),"
        "  PRIMARY KEY (raceId, driverId, stop),"
        "  FOREIGN KEY (raceId) REFERENCES races(raceId),"
        "  FOREIGN KEY (driverId) REFERENCES drivers(driverId)"
        ")"
    )

    TABLES["qualifying"] = (
        "CREATE TABLE IF NOT EXISTS qualifying ("
        "  qualifyId INT PRIMARY KEY,"
        "  raceId INT,"
        "  driverId INT,"
        "  constructorId INT,"
        "  number INT,"
        "  position INT,"
        "  q1 VARCHAR(255),"
        "  q2 VARCHAR(255),"
        "  q3 VARCHAR(255),"
        "  FOREIGN KEY (raceId) REFERENCES races(raceId),"
        "  FOREIGN KEY (driverId) REFERENCES drivers(driverId),"
        "  FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)"
        ")"
    )

    TABLES["results"] = (
        "CREATE TABLE IF NOT EXISTS results ("
        "  resultId INT PRIMARY KEY,"
        "  raceId INT,"
        "  driverId INT,"
        "  constructorId INT,"
        "  statusId INT,"
        "  number INT,"
        "  grid INT,"
        "  position INT,"
        "  points FLOAT,"
        "  laps INT,"
        "  time VARCHAR(255),"
        "  fastestLap VARCHAR(255),"
        "  FOREIGN KEY (raceId) REFERENCES races(raceId),"
        "  FOREIGN KEY (driverId) REFERENCES drivers(driverId),"
        "  FOREIGN KEY (constructorId) REFERENCES constructors(constructorId),"
        "  FOREIGN KEY (statusId) REFERENCES status(statusId)"
        ")"
    )

    for table_name, query in TABLES.items():
        try:
            cursor.execute(query)
            print(f"{table_name} exists")
        except Error as e:
            print(f"Error while creating table: {table_name}: {e}")

    F1_DB.commit()
    cursor.close()
    F1_DB.close()


if __name__ == "__main__":
    test_connection()
