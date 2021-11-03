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
    database = "vaccine.db"

    sql_create_citizen_table = """CREATE TABLE IF NOT EXISTS citizen (
                                    id_citizen TEXT PRIMARY KEY,
                                    email TEXT NOT NULL,
                                    name TEXT NOT NULL,
                                    surname TEXT NOT NULL,
                                    date_of_birth TEXT NOT NULL,
                                    mobile_num TEXT NOT NULL,
                                    medical_aid TEXT NOT NULL,
                                    address TEXT NOT NULL,
                                    FOREIGN KEY (id_citizen) REFERENCES citizen (parent_id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create citizen table
        create_table(conn, sql_create_citizen_table)
    else:
        print("Error")


if __name__ == '__main__':
    main()
