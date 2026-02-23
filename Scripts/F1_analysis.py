import os

import mysql.connector
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
        os.system(
            "clear"
        )  # need to be able to run on windows aswell, right now it's only available on linux
        print(
            """Please enter a number:\n1.Who has the fastest average pit stop?\n2.\n3.\n4.\n5.\n6.\n0.\n"""
        )
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


# TODO: Make query
# 1. What team has the fastest average pit stop?
def fastest_average_pit_stop(
    db: MySQLConnectionAbstract | PooledMySQLConnection,
):  # Jonathan
    sql = ""
    response = execute_fetch_one(db, sql)
    print(response)


# 2. What team has won the most races between year x and y
def won_most_races(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Jonathan
    year1 = None
    year2 = None
    while True:
        year1 = input("From: ")
        year2 = input("To: ")
        if not year1.isnumeric() or not year2.isnumeric():
            continue

        if int(year1) in range(1950, 2024) and int(year2) in range(1950, 2024):
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
    print(response)  # TODO: fix a better printout


# TODO: Make query
def most_wins_driver(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Elias
    sql = ""
    response = execute_fetch_one(db, sql)
    print(response)


# TODO: Make query
def avg_pit_stop_time(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Jonathan
    sql = ""
    response = execute_fetch_one(db, sql)
    print(response)


# TODO: Make query
def add_pit_stop_time(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Elias
    sql = ""
    response = execute_fetch_one(db, sql)
    print(response)


# TODO: Make query
def total_championship_points(
    db: MySQLConnectionAbstract | PooledMySQLConnection,
):  # Elias
    sql = ""
    response = execute_fetch_one(db, sql)
    print(response)


def execute_fetch_all(db: MySQLConnectionAbstract | PooledMySQLConnection, query: str):
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def execute_fetch_one(db: MySQLConnectionAbstract | PooledMySQLConnection, query: str):
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchone()


if __name__ == "__main__":
    main()
