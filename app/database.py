import sqlite3
import os

DB_PATH = "./database/data.db"
INIT_SQL_PATH = "./database/init.sql"
DB_INITIALIZED = False


def initialize_database():
    if not os.path.exists(DB_PATH) or os.stat(DB_PATH).st_size == 0:
        with open(INIT_SQL_PATH, "r") as sql_file:
            sql_script = sql_file.read()
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.executescript(sql_script)
        connection.commit()
        connection.close()


def connect():
    global DB_INITIALIZED
    if not DB_INITIALIZED:
        initialize_database()
        DB_INITIALIZED = True
    return sqlite3.connect(DB_PATH)


def save_event(device_id, event_type, value=None, numeric_value=None):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO device_event (device_id, type, value, numeric_value)
        VALUES (?, ?, ?, ?);
        """,
        (device_id, event_type, value, numeric_value),
    )
    connection.commit()
    connection.close()
    print(f"Event saved: {device_id}, {event_type}, {value}, {numeric_value}")
