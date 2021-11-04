import sqlite3
from sqlite3 import Error

# create connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

# create the table
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "./app/vaccine.db"

    sql_create_citizen_table = """CREATE TABLE IF NOT EXISTS citizen (
                                    id_citizen TEXT PRIMARY KEY,
                                    email TEXT NOT NULL,
                                    name TEXT NOT NULL,
                                    surname TEXT NOT NULL,
                                    date_of_birth TEXT NOT NULL,
                                    mobile_num TEXT NOT NULL,
                                    medical_aid TEXT NOT NULL,
                                    address TEXT NOT NULL,
                                    parent_id TEXT,
                                    FOREIGN KEY (parent_id) REFERENCES citizen (id_citizen)
                                );"""
    
    sql_create_vaccine_table = """CREATE TABLE IF NOT EXISTS vaccine (
                                    id_vaccine INT PRIMARY KEY,
                                    vaccine_name TEXT NOT NULL,
                                    target_disease TEXT NOT NULL,
                                    number_to_administer INT NOT NULL,
                                    dosage_interval INT
                                );"""

    sql_create_vile_table = """CREATE TABLE IF NOT EXISTS vile (
                                    id_vile TEXT PRIMARY KEY,
                                    vaccine_id INT NOT NULL,
                                    FOREIGN KEY (vaccine_id) REFERENCES vaccine (id_vaccine)
                                );"""

    sql_create_location_table = """CREATE TABLE IF NOT EXISTS location (
                                    id_location INT PRIMARY KEY,
                                    address TEXT NOT NULL,
                                    name_of_place TEXT NOT NULL
                                );"""

    sql_create_vaccination_table = """CREATE TABLE IF NOT EXISTS vaccination (
                                    id_vaccination TEXT PRIMARY KEY,
                                    citizen_id TEXT NOT NULL,
                                    vile_id TEXT NOT NULL,
                                    location_id INT NOT NULL,
                                    date_of_vaccination TEXT NOT NULL,
                                    dosage_number INT NOT NULL,
                                    side_effects INT NOT NULL,
                                    description_side_effects TEXT,
                                    FOREIGN KEY (citizen_id) REFERENCES citizen (id_citizen),
                                    FOREIGN KEY (vile_id) REFERENCES vile (id_vile),
                                    FOREIGN KEY (location_id) REFERENCES location (id_location)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tables
        create_table(conn, sql_create_citizen_table)
        create_table(conn, sql_create_vaccine_table)
        create_table(conn, sql_create_vile_table)
        create_table(conn, sql_create_location_table)
        create_table(conn, sql_create_vaccination_table)
    else:
        print("Error")


if __name__ == '__main__':
    main()
