Before running the project, ensure you have the following installed:
* Python 3
* MySQL Server

You will also need to install the required Python libraries. If you are using a virtual environment (.venv), activate it first, then install the dependencies:

pip install mysql-connector-python python-dotenv matplotlib

Configuration:
This application uses environment variables to securely connect to the MySQL database.

1. Locate the "env_template.txt" file in the root directory.
2. Create a new file named ".env" in the root directory.
3. Copy the contents of "env_template.txt" into ".env" and fill in your specific MySQL database credentials (host, port, user and password).

Before running the main application, you must initialize the database and populate it with the F1 data.
You can either run the setup_db.py script to create the database and populate it or you can use the Data_Dump.sql.

Usage:
To start the F1 Analysis tool run the F1_analysis.py

You will be greeted by an interactive menu with different options
