import sqlite3
import os

DB_PATH = "./ctwp/database/data.db"
INIT_SQL_PATH = "./ctwp/database/init.sql"
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


def get_latest_consumption():
    connection = connect()
    cursor = connection.cursor()
    query = """
    SELECT SUM(numeric_value) AS total_consumption
    FROM device_event
    WHERE type = 'energy-consumption'
    """
    cursor.execute(query)
    result = cursor.fetchone()
    connection.close()
    return round(result[0] if result[0] else 0, 2)


def get_current_rate():
    # Placeholder for real tariff retrieval
    # Replace this with a query to fetch from the database if tariffs are stored
    return 0.45  # Static rate as a placeholder


def get_total_cost():
    """Calculate the total cost of energy consumption from the database."""
    connection = connect()
    query = """
    SELECT SUM(numeric_value * 0.45) AS total_cost
    FROM device_event
    WHERE type = 'energy-consumption'
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    connection.close()
    return round(result[0] if result[0] else 0, 2)


def get_cost_by_device():
    """Calculate energy cost per device and include additional details."""
    connection = connect()
    query = """
    SELECT 
        d.id,
        d.name,
        d.type,
        d.power,
        SUM(de.numeric_value * 0.45) AS cost
    FROM device_event de
    JOIN device d ON de.device_id = d.id
    WHERE de.type = 'energy-consumption'
    GROUP BY d.id, d.name, d.type, d.power
    ORDER BY d.id
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert the results into a list of dictionaries for Streamlit table
    return [
        {
            "ID": row[0],
            "Nome": row[1],
            "Tipo": row[2],
            "Potência (W)": row[3],
            "Custo (R$)": round(row[4], 2),
        }
        for row in result
    ]


def get_all_zones():
    """Fetch all zones (cômodos) from the database."""
    connection = connect()
    query = """
    SELECT id, name, description
    FROM zone
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert to a list of dictionaries for Streamlit
    return [{"ID": row[0], "Nome": row[1], "Descrição": row[2]} for row in result]


def get_all_devices():
    """Fetch all devices from the database."""
    connection = connect()
    query = """
    SELECT id, name, type, power, zone_id
    FROM device
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert to a list of dictionaries for Streamlit
    return [
        {
            "ID": row[0],
            "Nome": row[1],
            "Tipo": row[2],
            "Potência (W)": row[3],
            "Cômodo ID": row[4],
        }
        for row in result
    ]


def get_devices_by_zone(zone_id):
    """Fetch all devices for a specific zone from the database."""
    connection = connect()
    query = """
    SELECT id, name, type, power, zone_id
    FROM device
    WHERE zone_id = ?
    """
    cursor = connection.cursor()
    cursor.execute(query, (zone_id,))
    result = cursor.fetchall()
    connection.close()

    # Convert to a list of dictionaries for Streamlit
    return [
        {
            "ID": row[0],
            "Nome": row[1],
            "Tipo": row[2],
            "Potência (W)": row[3],
            "Zona ID": row[4],
        }
        for row in result
    ]


def get_cost_by_zone():
    """Calculate total energy cost per zone."""
    connection = connect()
    query = """
    SELECT 
        z.id AS zone_id,
        z.name AS zone_name,
        SUM(de.numeric_value * 0.45) AS total_cost
    FROM zone z
    LEFT JOIN device d ON z.id = d.zone_id
    LEFT JOIN device_event de ON d.id = de.device_id
    WHERE de.type = 'energy-consumption'
    GROUP BY z.id, z.name
    ORDER BY z.id
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert results to a list of dictionaries
    return [
        {
            "ID": row[0],
            "Zona": row[1],
            "Custo Total (R$)": round(row[2] if row[2] else 0, 2),
        }
        for row in result
    ]


def get_consumption_by_zone():
    """Fetch total consumption (kWh) grouped by zone."""
    connection = connect()
    query = """
    SELECT 
        z.name AS zone_name,
        SUM(de.numeric_value) AS total_consumption
    FROM zone z
    LEFT JOIN device d ON z.id = d.zone_id
    LEFT JOIN device_event de ON d.id = de.device_id
    WHERE de.type = 'energy-consumption'
    GROUP BY z.name
    ORDER BY z.name
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert results to a list of dictionaries
    return [
        {"Zona": row[0], "Consumo Total (kWh)": round(row[1] if row[1] else 0, 2)}
        for row in result
    ]


def get_consumption_by_device():
    """Fetch total consumption (kWh) grouped by device."""
    connection = connect()
    query = """
    SELECT 
        d.name AS device_name,
        SUM(de.numeric_value) AS total_consumption
    FROM device d
    LEFT JOIN device_event de ON d.id = de.device_id
    WHERE de.type = 'energy-consumption'
    GROUP BY d.name
    ORDER BY d.name
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert results to a list of dictionaries
    return [
        {
            "Dispositivo": row[0],
            "Consumo Total (kWh)": round(row[1] if row[1] else 0, 2),
        }
        for row in result
    ]


def get_consumption_by_period(period):
    """Fetch total consumption (kWh) grouped by zone and filtered by period."""
    connection = connect()
    period_filter = {
        "Diário": "strftime('%Y-%m-%d', de.timestamp) AS period",
        "Semanal": "strftime('%Y-%W', de.timestamp) AS period",
        "Mensal": "strftime('%Y-%m', de.timestamp) AS period",
    }

    query = f"""
    SELECT 
        z.name AS zone_name,
        {period_filter[period]},
        SUM(de.numeric_value) AS total_consumption
    FROM zone z
    LEFT JOIN device d ON z.id = d.zone_id
    LEFT JOIN device_event de ON d.id = de.device_id
    WHERE de.type = 'energy-consumption'
    GROUP BY period, z.name
    ORDER BY period
    """

    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert results to a list of dictionaries
    return [
        {
            "Zona": row[0],
            "Período": row[1],
            "Consumo Total (kWh)": round(row[2] if row[2] else 0, 2),
        }
        for row in result
    ]
