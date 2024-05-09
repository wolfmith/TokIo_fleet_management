import sqlite3
from faker import Faker
import random
import bcrypt



fake = Faker()

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established to the database.")
    except Exception as e:
        print(f"Failed to connect due to {e}")
    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
        print("Table created successfully.")
    except Exception as e:
        print(f"Failed to create table due to {e}")

def insert_user(conn, user):
    name, email, password, user_type = user
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    sql = ''' INSERT INTO Users(name, email, password, user_type)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (name, email, hashed_password, user_type))
    conn.commit()


def insert_vehicle(conn, vehicle):
    sql = ''' INSERT INTO Vehicles(make, model, category, transmission, vehicle_type, daily_rate, last_revision_date, next_revision_date, last_inspection_date, passenger_capacity)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, vehicle)
    conn.commit()

def insert_customer(conn, customer):
    sql = ''' INSERT INTO Customers(name, identification, phone, address, email)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()

def check_password(email, password, conn):
    """Check if the provided password for a user is correct"""
    cur = conn.cursor()
    cur.execute("SELECT password FROM Users WHERE email = ?", (email,))
    stored_password = cur.fetchone()  # fetch the hashed password from the database
    if stored_password:
        return bcrypt.checkpw(password.encode('utf-8'), stored_password[0].encode('utf-8'))
    return False

def main():
    database = "LuxuryWheels.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS Users (
                                        user_id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        email TEXT NOT NULL UNIQUE,
                                        password TEXT NOT NULL,
                                        user_type TEXT NOT NULL
                                    ); """

    sql_create_vehicles_table = """ CREATE TABLE IF NOT EXISTS Vehicles (
                                        vehicle_id INTEGER PRIMARY KEY,
                                        make TEXT NOT NULL,
                                        model TEXT NOT NULL,
                                        category TEXT NOT NULL,
                                        transmission TEXT NOT NULL,
                                        vehicle_type TEXT NOT NULL,
                                        daily_rate REAL NOT NULL,
                                        last_revision_date TEXT NOT NULL,
                                        next_revision_date TEXT NOT NULL,
                                        last_inspection_date TEXT NOT NULL,
                                        passenger_capacity INTEGER NOT NULL
                                    ); """

    sql_create_customers_table = """ CREATE TABLE IF NOT EXISTS Customers (
                                        customer_id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        identification TEXT NOT NULL,
                                        phone TEXT NOT NULL,
                                        address TEXT NOT NULL,
                                        email TEXT NOT NULL UNIQUE
                                    ); """

    # Create a database connection
    conn = create_connection(database)

    # Create tables
    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_vehicles_table)
        create_table(conn, sql_create_customers_table)

        # Insert random data
        for _ in range(10):  # Assuming we want to insert data for 10 users, vehicles, and customers
            insert_user(conn, (fake.name(), fake.email(), fake.password(), random.choice(['admin', 'customer'])))
            insert_vehicle(conn, (fake.company(), fake.word(), random.choice(['Sedan', 'SUV']), random.choice(['Manual', 'Automatic']), random.choice(['Car', 'Truck']), round(random.uniform(50, 500), 2), fake.date(), fake.date(), fake.date(), random.randint(1, 8)))
            insert_customer(conn, (fake.name(), fake.ssn(), fake.phone_number(), fake.address(), fake.email()))

        print("Random data inserted successfully.")
    else:
        print("Error! cannot create the database connection.")

    conn.close()

if __name__ == '__main__':
    main()
