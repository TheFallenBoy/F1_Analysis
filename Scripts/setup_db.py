# 1 Ensure connected to DB
# 2 Does DB exist?
# 3 Create The database
# 4 Create the tables
# 5 insert .csv
# 6 print "all set"

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

    # 2 & 3
    cursor = F1_DB.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    DB_exists = False
    for (db_name,) in databases:
        if db_name == os.getenv("DB_NAME"):
            DB_exists = True
    if not DB_exists:
        cursor.execute("CREATE DATABASE F1_DB")

    # 4


if __name__ == "__main__":
    test_connection()
