CREATE TABLE
  state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE, -- Abbreviation of the state (e.g., SP, RJ)
    name TEXT NOT NULL UNIQUE -- Full name of the state
  );

CREATE TABLE
  consumption_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE -- Type of consumption (e.g., Total, Cativo, Outros)
  );

CREATE TABLE
  energy_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    state_id INTEGER NOT NULL, -- Foreign key for state
    consumption_type_id INTEGER NOT NULL, -- Foreign key for consumption type
    consumption INTEGER, -- Energy consumption in MWh
    consumer_count INTEGER, -- Number of consumers
    FOREIGN KEY (state_id) REFERENCES state (id),
    FOREIGN KEY (consumption_type_id) REFERENCES consumption_type (id)
  );

