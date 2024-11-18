CREATE TABLE
  room (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
  );

CREATE TABLE
  energy_consumption (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    room_id INTEGER NOT NULL,
    presence BOOLEAN NOT NULL,
    light_level INTEGER NOT NULL,
    energy_consumption REAL NOT NULL,
    relay_status BOOLEAN NOT NULL,
    FOREIGN KEY (room_id) REFERENCES room (id) ON DELETE CASCADE
  );

-- Fictitious rooms
-- INSERT INTO
--   room (name)
-- VALUES
--   ('Sala'),
--   ('Quarto'),
--   ('Cozinha'),
--   ('Área Externa');
--
-- Fictitious energy consumption data
-- INSERT INTO
--   energy_consumption (
--     room_id,
--     presence,
--     light_level,
--     energy_consumption,
--     relay_status
--   )
-- VALUES
--   (1, TRUE, 300, 1.5, TRUE),
--   (2, FALSE, 0, 0.0, FALSE),
--   (3, TRUE, 500, 2.1, TRUE),
--   (4, TRUE, 150, 0.8, TRUE);
