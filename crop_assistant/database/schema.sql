-- schema.sql — SQLite database schema for AI Crop Assistant
-- Applied automatically at startup via database/db.py
-- SQLite is used because it is lightweight, file-based, and works fully offline.

-- ─── Predictions ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS predictions (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp        TEXT    NOT NULL,
    image_path       TEXT,
    crop             TEXT,
    disease          TEXT,
    status           TEXT,          -- "healthy" | "diseased" | "uncertain" | "invalid" | "error"
    confidence       REAL,
    confidence_level TEXT,          -- "high" | "medium" | "low"
    raw_label        TEXT,
    model_version    TEXT,
    inference_time_ms REAL,
    image_quality    TEXT,
    notes            TEXT,
    mode             TEXT           -- "tflite" | "pytorch" | "demo"
);

-- Index for time-ordered queries (dashboard, history page)
CREATE INDEX IF NOT EXISTS idx_predictions_timestamp
    ON predictions (timestamp DESC);

-- ─── Sensor Readings (future ESP32 integration) ───────────────────────────────
CREATE TABLE IF NOT EXISTS sensor_readings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp     TEXT    NOT NULL,
    soil_moisture REAL,
    temperature   REAL,
    humidity      REAL,
    rainfall      REAL,
    water_level   REAL
);

CREATE INDEX IF NOT EXISTS idx_sensors_timestamp
    ON sensor_readings (timestamp DESC);

-- ─── Irrigation Events (future) ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS irrigation_events (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp        TEXT    NOT NULL,
    mode             TEXT,          -- "manual" | "auto"
    duration_seconds INTEGER,
    reason           TEXT,
    soil_moisture    REAL,
    status           TEXT           -- "completed" | "aborted" | "error"
);

-- ─── Settings (persisted configuration) ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Default settings (ignore if already set)
INSERT OR IGNORE INTO settings (key, value) VALUES ('scheduler_interval_min', '60');
INSERT OR IGNORE INTO settings (key, value) VALUES ('scheduler_enabled',      'true');
INSERT OR IGNORE INTO settings (key, value) VALUES ('confidence_high',        '0.80');
INSERT OR IGNORE INTO settings (key, value) VALUES ('confidence_medium',      '0.60');
INSERT OR IGNORE INTO settings (key, value) VALUES ('max_stored_images',      '500');
INSERT OR IGNORE INTO settings (key, value) VALUES ('image_retention_days',   '30');
