## F1 Analysis Project Setup

To get your environment ready and the application running, follow the segments below.

---

### Prerequisites
Before running the project, ensure you have the following installed on your system:
* **Python 3**
* **MySQL Server**

---

### Installation
You will need to install the required Python libraries. If you are using a virtual environment (`.venv`), activate it first, then install the dependencies.

To install them via your terminal, use:
`pip install mysql-connector-python python-dotenv matplotlib`

* [mysql-connector-python documentation](https://dev.mysql.com/doc/connector-python/en/)
* [python-dotenv documentation](https://pypi.org/project/python-dotenv/)
* [matplotlib documentation](https://matplotlib.org/)

---

### Configuration
This application uses environment variables to securely connect to the MySQL database.

1. **Locate** the `env_template.txt` file in the root directory.
2. **Create** a new file named `.env` in the root directory.
3. **Copy** the contents of `env_template.txt` into `.env` and fill in your specific MySQL database credentials (**host**, **port**, **user**, and **password**).

---

### Database Initialization
Before running the main application, you must initialize the database and populate it with the F1 data. You have two options for this:

* **Script Method:** Run the `setup_db.py` script to automatically create and populate the database.
* **Manual Method:** Use the provided `Data_Dump.sql` file directly in your MySQL instance.

---

### Usage
To start the F1 Analysis tool, run the following file:
`F1_analysis.py`

Once launched, you will be greeted by an interactive menu with different analysis options.
