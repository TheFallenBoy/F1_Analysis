import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
from dotenv import load_dotenv
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


def main():
    load_dotenv()
    choices = {
        "1": fastest_average_pit_stop,
        "2": won_most_races,
        "3": most_wins_driver,
        "4": avg_pit_stop_time,
        "5": add_pit_stop_time,
        "6": total_championship_points,
    }

    db = connect()

    while True:
        os.system("clear")  # need to be able to run on windows as well, right now it's only available on Linux
        print("""Please enter a number:\n1.Who has the fastest average pit stop?\n2.\n3.\n4.\n5.\n6.\n0.\n""")
        choice = input()
        if choice.isnumeric() and int(choice) == 0:
            break
        if choice in choices:
            choices[choice](db)
        else:
            print("Invalid input")
        print("Press Enter to continue")
        input()


def connect() -> MySQLConnectionAbstract | PooledMySQLConnection:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    db.cursor().execute("USE F1_DB")

    return db


# INFO: 1. What team has the fastest average pit lane time?
def fastest_average_pit_stop(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Jonathan
    sql = """SELECT constructors.name, AVG(pit_stops.milliseconds)/1000 AS average_pit_time_s
    FROM pit_stops
    JOIN results ON pit_stops.raceId = results.raceId
    AND pit_stops.driverId = results.driverId
    JOIN constructors ON results.constructorId = constructors.constructorId
    WHERE pit_stops.milliseconds < 50000
    GROUP BY constructors.name
    ORDER BY average_pit_time_s ASC
    LIMIT 1;"""
    response = execute_fetch_one(db, sql)
    if response is None:
        print("No results found.")
        return
    print(f"{response[0]} have the best avreage pit lane time with {round(response[1], 2)}s")


# INFO: 2. What team has won the most races between year x and y
def won_most_races(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Jonathan
    year1 = None
    year2 = None
    while True:
        year1 = input("From: ")
        year2 = input("To: ")
        if not year1.isnumeric() or not year2.isnumeric():
            continue

        if int(year1) in range(1950, 2025) and int(year2) in range(1950, 2025):
            break

    sql = f"""SELECT constructors.name as constructor, count(results.resultId) as TotalWins
    FROM results
    JOIN races ON results.raceId = races.raceId
    JOIN constructors ON constructors.constructorId = results.constructorId
    WHERE results.position = 1
    AND races.year between {year1} AND {year2} 
    GROUP BY constructors.name
    ORDER BY TotalWins DESC
    LIMIT 1"""
    response = execute_fetch_one(db, sql)
    if response is None:
        print("No results found.")
        return
    print(f"{response[0]} have most amount of won races between {year1} and {year2}")
    print(f"Amount of wins: {response[1]}")


# INFO: 3. Who are the top 5 best drivers in F1?
def most_wins_driver(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Elias
    sql = """SELECT results.driverId, drivers.forename, drivers.surname, COUNT(results.driverId) AS TotalWins
    FROM results
    INNER JOIN drivers
    ON drivers.driverId = results.driverId
    WHERE results.position = 1
    GROUP BY results.driverId
    ORDER BY TotalWins DESC
    LIMIT 5;"""
    response = execute_fetch_all(db, sql)
    if response is None:
        print("No results found.")
        return
    print(response)  # WARNING: Fix printout


# INFO: 4. How have the pit lane time decrease over the years? (open up a diagram showing a graph.)
def avg_pit_stop_time(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Jonathan
    sql = """SELECT races.date, pit_stops.milliseconds
    FROM pit_stops
    JOIN races ON races.raceId = pit_stops.raceId
    WHERE pit_stops.milliseconds < 50000
    ORDER BY races.date asc"""
    response = execute_fetch_all(db, sql)
    # TODO: unpack tuple and make graph


# TODO: Make query
def add_pit_stop_time(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Elias
    sql = ""
    response = execute_fetch_one(db, sql)
    print(response)  # WARNING: Fix printout


# TODO: Make query
def total_championship_points(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Elias
    sql = ""
    response = execute_fetch_one(db, sql)
    print(response)  # WARNING: Fix printout


def execute_fetch_all(db: MySQLConnectionAbstract | PooledMySQLConnection, query: str):
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def execute_fetch_one(db: MySQLConnectionAbstract | PooledMySQLConnection, query: str) -> tuple | None:
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchone()  # type: ignore


if __name__ == "__main__":
    main()
