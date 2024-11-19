CREATE TABLE
  zones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL, -- Name of the zone (e.g., "Living Room", "Kitchen")
    description TEXT
  );

CREATE TABLE
  device (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL, -- Name of the device (e.g., "Lamp #1", "Sensor #4")
    type VARCHAR(50) NOT NULL, -- Type of the device (e.g., "lamp", "presence-sensor", "light-sensor")
    zone_id INTEGER,
    power REAL, -- Power consumption in watts (optional, for energy-consuming devices)
    description TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES zones (id)
  );

CREATE TABLE
  device_event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER,
    type VARCHAR(50) NOT NULL, -- Type of the event (e.g., "state-change", "sensor-reading", "energy-consumption")
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    value TEXT, -- Value associated with the event (e.g., "on", "250 lux")
    numeric_value REAL, -- Optional numeric value (e.g., 1.23 kWh, 300 lux)
    FOREIGN KEY (device_id) REFERENCES device (id)
  );

-- Insert some sample zones
INSERT INTO
  zones (name, description)
VALUES
  ('Living Room', 'Main area of the house'),
  ('Kitchen', 'Cooking and dining area'),
  ('Bedroom', 'Sleeping area'),
  ('Garage', 'Car parking area');

-- Insert some sample devices
INSERT INTO
  devices (name, type, zone_id, power, description)
VALUES
  (
    'Ceiling Lamp',
    'lamp',
    1,
    15.0,
    'LED ceiling lamp in the living room'
  ),
  (
    'Presence Sensor',
    'presence-sensor',
    1,
    NULL,
    'Motion sensor for the living room'
  ),
  (
    'Light Sensor',
    'light-sensor',
    2,
    NULL,
    'Light intensity sensor in the kitchen'
  ),
  (
    'Table Lamp',
    'lamp',
    3,
    10.0,
    'Small bedside table lamp'
  ),
  (
    'Garage Light',
    'lamp',
    4,
    20.0,
    'Bright light for the garage'
  );

-- Insert some sample device events
INSERT INTO
  device_event (device_id, type, value, numeric_value)
VALUES
  (1, 'state-change', 'on', NULL), -- Ceiling Lamp turned on
  (2, 'sensor-reading', 'motion detected', NULL), -- Presence detected in Living Room
  (3, 'sensor-reading', '250 lux', 250.0), -- Light level detected in Kitchen
  (4, 'state-change', 'off', NULL), -- Table Lamp turned off
  (5, 'state-change', 'on', NULL), -- Garage Light turned on
  (1, 'energy-consumption', NULL, 0.015), -- Ceiling Lamp consumed 0.015 kWh
  (5, 'energy-consumption', NULL, 0.020) -- Garage Light consumed 0.020 kWh
;
