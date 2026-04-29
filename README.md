# Hotel Management Application — README 

# Team Members
- **Anupam Sai Sistla**
- **Jacob Woloch**
- **Ashika Shekhar**
- **Riya Gandhi**


## Prerequisites

Make sure the following are installed before running:

- **Python 3.8+** — https://www.python.org/downloads/
- **PostgreSQL** — https://www.postgresql.org/download/
- **psycopg2** Python library

Install psycopg2 by running:
```
pip install psycopg2-binary
```

**Note** There is  sample data available to you at ```sampleData.sql```

---

## Step 1 — Create the Database

Open a terminal and run:

```bash
psql -U <your_username>
```

Then inside psql:

```sql
CREATE DATABASE <your_database_name>;
\q
```

---

## Step 2 — Load the Schema

Run the schema SQL file to create all the tables:

```bash
psql -U <your_username> -d <your_database_name> -f schema.sql
```

Verify the tables were created:

```bash
psql -U <your_username> -d <your_database_name> -c "\dt"
```

You should see tables: `Manager`, `Client`, `Hotel`, `Room`, `Booking`, `Review`, `Address`, `ClientAddress`, `CreditCard`.

---

## Step 3 — Load the Data

```bash
psql -U <your_username> -d <your_database_name> -f data.sql
```

Verify the data loaded:

```bash
psql -U <your_username> -d <your_database_name> -c "SELECT COUNT(*) FROM Booking;"
```

Should return **9**.

---

## Step 4 — Configure the Application

Open `main.py` and update the database connection settings at the bottom of the file to match your PostgreSQL setup:

```python
conn = psycopg2.connect(
    host="localhost",
    database="your_database_name",
    user="your_username",
    port="5432"
)
```

---

## Step 5 — Run the Application

```bash
python main.py
```

On Windows if you have multiple Python versions:

```bash
py -3 main.py
```

---

## Using the Application

When the application starts you will see:

```
======Jarvis - Your Hotel Management Assistant======
1. Login
2. Register
3. Exit
```

### Logging in as a Manager

- Choose **1. Login** → **1. Manager**
- Enter your SSN when prompted

### Logging in as a Client

- Choose **1. Login** → **2. Client**
- Enter your email address when prompted

### Registering a New Account

- Choose **2. Register** → select Manager or Client
- Follow the prompts to enter your details
- A new client must provide at least one address and one credit card

---

## Resetting the Database

To wipe all data and reload fresh test data at any point:

```bash
psql -U <your_username> -d <your_database_name> -f test_data.sql
```

The file deletes all existing rows before inserting, so you do not need to drop and recreate the database.

---

## Troubleshooting

**`relation does not exist` when loading test data**
Run `schema.sql` first to create the tables before loading `test_data.sql`.

**`could not connect to server` when running main.py**
Make sure PostgreSQL is running. On Windows open Services and check that the PostgreSQL service is started.

**`ModuleNotFoundError: No module named 'psycopg2'`**
Run `pip install psycopg2-binary` and try again.

**Authentication errors connecting to the database**
Double-check that the `host`, `database`, `user`, and `port` values in `main.py` match your local PostgreSQL setup.
