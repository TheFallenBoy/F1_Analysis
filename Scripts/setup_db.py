# 1 Ensure connected to server
# 2 Does DB exist?
# 3 Create The database
# 4 Create the tables
# 5 insert .csv
# 6 Clean up and print "all done"

import csv
import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()


def clean_val(val):
    if val == "\\N" or val == "" or val is None:
        return None
    return val


def insert_csv_data(cursor, F1_DB):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), "Data")

    TABLE_MAP = {
        "drivers": [
            "driverId",
            "driverRef",
            "number",
            "code",
            "forename",
            "surname",
            "dob",
            "nationality",
        ],
        "constructors": ["constructorId", "constructorRef", "name", "nationality"],
        "races": ["raceId", "year", "round", "name", "date", "time"],
        "lap_times": ["raceId", "driverId", "lap", "position", "time", "milliseconds"],
        "pit_stops": [
            "raceId",
            "driverId",
            "stop",
            "lap",
            "time",
            "duration",
            "milliseconds",
        ],
        "results": [
            "resultId",
            "raceId",
            "driverId",
            "constructorId",
            "number",
            "grid",
            "position",
            "points",
            "laps",
            "time",
            "fastestLap",
        ],
    }

    insertion_order = [
        "drivers",
        "constructors",
        "races",  #
        "lap_times",
        "pit_stops",
        "results",  #
    ]

    for table in insertion_order:
        csv_file_path = os.path.join(data_dir, f"{table}.csv")
        columns_to_keep = TABLE_MAP[table]

        placeholder = ", ".join(["%s"] * len(columns_to_keep))
        column_names = ",".join(columns_to_keep)
        sql = f"INSERT IGNORE INTO {table} ({column_names}) VALUES ({placeholder})"
        data_to_insert = []
        try:
            with open(csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    clean_row = tuple(clean_val(row.get(col)) for col in columns_to_keep)
                    data_to_insert.append(clean_row)
            print(f"Inserting {len(data_to_insert)} into '{table}'")

            chunk_size = 10000
            for i in range(0, len(data_to_insert), chunk_size):
                cursor.executemany(sql, data_to_insert[i : i + chunk_size])
            F1_DB.commit()
            print(f"Done with '{table}'")
        except FileNotFoundError:
            print(f"CSV file not found: {csv_file_path}")
        except Exception as e:
            print(f"Error while inserting into {table}: {e}")


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

    TABLES["drivers"] = (
        "CREATE TABLE IF NOT EXISTS drivers ("
        "  driverId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
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
        "  constructorId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        "  constructorRef VARCHAR(255),"
        "  name VARCHAR(255),"
        "  nationality VARCHAR(255)"
        ")"
    )

    TABLES["races"] = (
        "CREATE TABLE IF NOT EXISTS races ("
        "  raceId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        "  year INT,"
        "  round INT,"
        "  name VARCHAR(255),"
        "  date DATE,"
        "  time TIME"
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
        "  milliseconds INT,"
        "  PRIMARY KEY (raceId, driverId, stop),"
        "  FOREIGN KEY (raceId) REFERENCES races(raceId),"
        "  FOREIGN KEY (driverId) REFERENCES drivers(driverId)"
        ")"
    )

    TABLES["results"] = (
        "CREATE TABLE IF NOT EXISTS results ("
        "  resultId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        "  raceId INT,"
        "  driverId INT,"
        "  constructorId INT,"
        "  number INT,"
        "  grid INT,"
        "  position INT,"
        "  points FLOAT,"
        "  laps INT,"
        "  time VARCHAR(255),"
        "  fastestLap VARCHAR(255),"
        "  FOREIGN KEY (raceId) REFERENCES races(raceId),"
        "  FOREIGN KEY (driverId) REFERENCES drivers(driverId),"
        "  FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)"
        ")"
    )

    for table_name, query in TABLES.items():
        try:
            cursor.execute(query)
            print(f"{table_name} exists")
        except Error as e:
            print(f"Error while creating table: {table_name}: {e}")

    # 5
    insert_csv_data(cursor, F1_DB)

    # 6
    # Create the function and stored procedure
    cursor.execute("DROP FUNCTION IF EXISTS ACCUMULATED_POINTS;")
    cursor.execute(""" 
    DELIMITER //

    CREATE FUNCTION ACCUMULATED_POINTS(p_team VARCHAR(255), p_year INT)
    RETURNS INT DETERMINISTIC
    BEGIN
        DECLARE total_sum INT;
        DECLARE team_id INT;
        SET team_id = (SELECT constructorId FROM constructors WHERE p_team = name LIMIT 1);
        IF team_id IS NULL OR p_year NOT IN (SELECT races.year FROM races) THEN
            RETURN -1;
        END IF;
        SELECT IFNULL(SUM(results.points),0)
        INTO total_sum
        FROM results
        JOIN races ON races.raceId = results.raceId AND races.year = p_year
        WHERE results.constructorId = team_id;
        
        RETURN total_sum;
        
    END //
    DELIMITER ;""")

    cursor.execute("DROP PROCEDURE IF EXISTS ADD_LAPTIME;")

    cursor.execute("""DELIMITER //
    CREATE PROCEDURE ADD_LAPTIME (
    IN raceName VARCHAR(255), 
    IN raceDate VARCHAR(255),
    IN driverFName VARCHAR(255),
    IN driverLName VARCHAR(255),
    IN p_lap INT, 
    IN p_position INT,
    IN p_time VARCHAR(255),
    IN p_milliseconds INT, 
    OUT success INT
    )
        BEGIN
            DECLARE v_raceId INT;
            DECLARE v_driverId INT;
            
            SET v_driverId = (SELECT drivers.driverId FROM drivers WHERE drivers.forename = driverFName AND drivers.surname = driverLName LIMIT 1);
            SET v_raceId = (SELECT races.raceId FROM races WHERE races.name = raceName AND races.date = raceDate LIMIT 1);
            IF v_driverId IS NULL OR v_raceId IS NULL THEN
                SET success = -1;
            ELSE
                INSERT IGNORE lap_times (raceId,driverId,lap,position,time,milliseconds) -- IGNORE ensures so that no dublicates of the same lap is entered.
                VALUES (v_raceId, v_driverId, p_lap, p_position,p_time,p_milliseconds);
                SET success = 0;
            END IF;
            
        END //
    DELIMITER ;""")

    # 7
    F1_DB.commit()
    cursor.close()
    F1_DB.close()
    print("All done!")


if __name__ == "__main__":
    test_connection()
