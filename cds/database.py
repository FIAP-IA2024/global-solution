import sqlite3
import os
import pandas as pd

DB_PATH = "./cds/database/data.db"
INIT_SQL_PATH = "./cds/database/init.sql"
CSV_PATH = "./cds/data-source/br_mme_consumo_energia_eletrica.csv"
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


def load_csv_to_database():
    connection = connect()
    cursor = connection.cursor()

    data = pd.read_csv(CSV_PATH)

    states = data[["sigla_uf", "sigla_uf_nome"]].drop_duplicates()
    for _, row in states.iterrows():
        cursor.execute(
            "INSERT OR IGNORE INTO state (code, name) VALUES (?, ?);",
            (row["sigla_uf"], row["sigla_uf_nome"]),
        )

    consumption_types = data["tipo_consumo"].drop_duplicates()
    for consumption_type in consumption_types:
        cursor.execute(
            "INSERT OR IGNORE INTO consumption_type (name) VALUES (?);",
            (consumption_type,),
        )

    for _, row in data.iterrows():
        cursor.execute(
            """
            INSERT INTO energy_data (
                year, month, state_id, consumption_type_id, consumption, consumer_count
            )
            VALUES (
                ?, ?, 
                (SELECT id FROM state WHERE code = ?), 
                (SELECT id FROM consumption_type WHERE name = ?), 
                ?, ?
            );
            """,
            (
                row["ano"],
                row["mes"],
                row["sigla_uf"],
                row["tipo_consumo"],
                row["consumo"],
                row["numero_consumidores"],
            ),
        )

    connection.commit()
    connection.close()


# Useful queries
def get_total_consumption_by_year():
    connection = connect()
    query = """
    SELECT year, SUM(consumption) AS total_consumption
    FROM energy_data
    GROUP BY year
    ORDER BY year;
    """
    result = pd.read_sql_query(query, connection)
    connection.close()
    return result


def get_consumption_by_state(year):
    connection = connect()
    query = """
    SELECT s.name AS state, SUM(e.consumption) AS total_consumption
    FROM energy_data e
    JOIN state s ON e.state_id = s.id
    WHERE e.year = ?
    GROUP BY s.name
    ORDER BY total_consumption DESC;
    """
    result = pd.read_sql_query(query, connection, params=(year,))
    connection.close()
    return result


def get_consumption_by_type():
    connection = connect()
    query = """
    SELECT c.name AS consumption_type, SUM(e.consumption) AS total_consumption
    FROM energy_data e
    JOIN consumption_type c ON e.consumption_type_id = c.id
    GROUP BY c.name
    ORDER BY total_consumption DESC;
    """
    result = pd.read_sql_query(query, connection)
    connection.close()
    return result


def get_avg_consumption_per_capita():
    connection = connect()
    query = """
    SELECT s.name AS state, 
           ROUND(SUM(e.consumption) * 1.0 / SUM(e.consumer_count), 2) AS avg_consumption_per_capita
    FROM energy_data e
    JOIN state s ON e.state_id = s.id
    WHERE e.consumer_count IS NOT NULL
    GROUP BY s.name
    ORDER BY avg_consumption_per_capita DESC;
    """
    result = pd.read_sql_query(query, connection)
    connection.close()
    return result


def get_trends_by_state(state_code):
    connection = connect()
    query = """
    SELECT e.year, SUM(e.consumption) AS total_consumption
    FROM energy_data e
    JOIN state s ON e.state_id = s.id
    WHERE s.code = ?
    GROUP BY e.year
    ORDER BY e.year;
    """
    result = pd.read_sql_query(query, connection, params=(state_code,))
    connection.close()
    return result


def get_all_states():
    """Retrieve all states from the database."""
    connection = connect()
    query = """
    SELECT code, name
    FROM state
    ORDER BY name;
    """
    result = pd.read_sql_query(query, connection)
    connection.close()
    return result


def get_total_consumption_by_month(year):
    """Retrieve total energy consumption by month for a specific year."""
    connection = connect()
    query = """
    SELECT month, SUM(consumption) AS total_consumption
    FROM energy_data
    WHERE year = ?
    GROUP BY month
    ORDER BY month;
    """
    result = pd.read_sql_query(query, connection, params=(year,))
    connection.close()
    return result
