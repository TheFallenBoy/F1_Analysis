import os

import matplotlib.pyplot as plt
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import DatabaseError
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


def main():
    load_dotenv()
    choices = {
        "1": fastest_average_pit_stop,
        "2": won_most_races,
        "3": most_wins_driver,
        "4": avg_pit_stop_time,
        "5": add_lap_time,
        "6": total_championship_points,
    }

    db = connect()

    while True:
        os.system("clear")  # BUG: Can't run on windows
        print(
            """Please enter a number:\n1. What constructor has the fastest average pit stop (2011 - 2024)?\n2. What constructor has won the most races between year x and y? \n3. Top 5 drivers (most won races)\n4. Pit lane time over the years 2011 - 2024\n5. Add a new lap time\n6. How much points did a team accumulate during a given year?\n0. Exit\n"""
        )
        choice = input()
        if choice.isnumeric() and int(choice) == 0:
            break
        if choice in choices:
            choices[choice](db)
        else:
            print("Invalid input")
        print("\nPress Enter to continue...")
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
            print("Invalid input")
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
    for racer in response:
        print(f"{racer[1]} {racer[2]}, wins: {racer[3]} DriverId: {racer[0]}")


# INFO: 4. How have the average pit lane time changed over the years? (open up a diagram showing a graph.)
def avg_pit_stop_time(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Jonathan
    sql = """SELECT 
    YEAR(races.date) as year, 
    AVG(pit_stops.milliseconds)/1000 as avg_time_sec,
    MIN(pit_stops.milliseconds)/1000 as min_time_sec
    FROM pit_stops
    JOIN races ON races.raceId = pit_stops.raceId
    WHERE pit_stops.milliseconds < 50000
    GROUP BY YEAR(races.date)
    ORDER BY year ASC"""
    response = execute_fetch_all(db, sql)
    if response is None:
        print("No results found.")
        return
    years = []
    avg_times = []
    min_times = []
    for pit_LaneInfo in response:
        years.append(pit_LaneInfo[0])
        avg_times.append(pit_LaneInfo[1])
        min_times.append(pit_LaneInfo[2])

    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_times, label="Average Pit Stop")
    plt.plot(years, min_times, label="Fastest Pit Stop")

    plt.xlabel("Year")
    plt.ylabel("Time (Seconds)")
    plt.title("F1 pit lane times over the Years")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.savefig("Plot.png")
    plt.close()
    print("Plot saved as Plot.png")


# INFO: 5. Add a new record for the lap time in the database. (stored procedure, need to make sure that both Driver and the race is in the database!)
def add_lap_time(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Elias
    r_name = input("Race Name: ")
    r_date = input("Race Date: ")
    d_fname = input("Drivers First Name: ")
    d_lname = input("Drivers Last Name: ")
    lap = input("Lap nr: ")
    position = input("Postition of the driver: ")
    time = input("Lap time: ")
    milliseconds = input("milliseconds of the lap: ")
    response = None

    try:
        response = call_procedure(
            db, "ADD_LAPTIME", args=(r_name, r_date, d_fname, d_lname, lap, position, time, milliseconds, response)
        )
        db.commit()
    except DatabaseError as e:
        print(f"Invalid action... \n [ERROR] {e.msg}")

    if response == None or response[8] == -1:
        print("Could not add lap time... Probably data not in database")
        return

    print(f"Successfully added {response[2]} {response[3]} new lap time")


# INFO: 6. Create a function that calculates and returns the total championship points a specific constructor has accumulated during a given racing year.
# WARNING: display team name
def total_championship_points(db: MySQLConnectionAbstract | PooledMySQLConnection):  # Elias
    team_name = input("Team Name: ")
    year = input("Year: ")
    try:
        sql = f"SELECT ACCUMULATED_POINTS('{team_name}','{year}') LIMIT 1;"
        response = execute_fetch_all(db, sql)
    except DatabaseError as e:
        print(f"Try again... \n[ERROR] {e.msg}")
        return

    if response == None:
        print("Invalid Input")
        return

    if response[0][0] == -1:
        print("Team or Year does not exist in Database, try again...")
        return

    print(f"{team_name} accumulated {response[0][0]} points in {year}")


def execute_fetch_all(db: MySQLConnectionAbstract | PooledMySQLConnection, query: str) -> tuple | None:
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()  # type: ignore


def execute_fetch_one(db: MySQLConnectionAbstract | PooledMySQLConnection, query: str) -> tuple | None:
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchone()  # type: ignore


def call_procedure(db: MySQLConnectionAbstract | PooledMySQLConnection, name: str, args: tuple) -> tuple | None:
    cursor = db.cursor()
    response = cursor.callproc(name, args)
    return response  # type: ignore


if __name__ == "__main__":
    main()
