"""
database/db.py — SQLite database wrapper for Kisan Mitra AI.
Created by Circuit Maze Team as part of SIH 2026.

Uses Python's built-in sqlite3 module — no external dependencies.
Fully offline. Thread-safe via check_same_thread=False + manual locking.
"""

import os
import sqlite3
import logging
import threading
from datetime import datetime, timedelta

from config import (DB_PATH, MAX_STORED_IMAGES, IMAGE_RETENTION_DAYS, IMAGE_DIR)

logger = logging.getLogger(__name__)

# Schema file path
_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

# Global connection (long-lived; Pi Zero W has limited RAM — reuse connection)
_conn  = None
_lock  = threading.Lock()


# ─── Initialisation ───────────────────────────────────────────────────────────

def init_db() -> bool:
    """
    Open the SQLite database and apply the schema.
    Creates the database file and parent directories if needed.
    Returns True on success.
    """
    global _conn

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    try:
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row          # rows as dict-like objects
        _conn.execute("PRAGMA journal_mode=WAL")  # safer concurrent access
        _conn.execute("PRAGMA synchronous=NORMAL")

        with open(_SCHEMA_PATH, "r") as f:
            schema = f.read()
        _conn.executescript(schema)
        _conn.commit()

        logger.info(f"[db] Database initialised at {DB_PATH}")
        return True

    except Exception as e:
        logger.error(f"[db] init_db failed: {e}")
        return False


def _get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        init_db()
    return _conn


# ─── Predictions ─────────────────────────────────────────────────────────────

def insert_prediction(data: dict) -> int:
    """
    Insert a prediction result into the database.

    Args:
        data: dict with keys matching the predictions table columns

    Returns:
        new row id (int), or -1 on error
    """
    sql = """
        INSERT INTO predictions
            (timestamp, image_path, crop, disease, status, confidence,
             confidence_level, raw_label, model_version, inference_time_ms,
             image_quality, notes, mode)
        VALUES
            (:timestamp, :image_path, :crop, :disease, :status, :confidence,
             :confidence_level, :raw_label, :model_version, :inference_time_ms,
             :image_quality, :notes, :mode)
    """
    row = {
        "timestamp":        data.get("timestamp", datetime.now().isoformat()),
        "image_path":       data.get("image_path"),
        "crop":             data.get("crop"),
        "disease":          data.get("disease"),
        "status":           data.get("status"),
        "confidence":       data.get("confidence"),
        "confidence_level": data.get("confidence_level"),
        "raw_label":        data.get("raw_label"),
        "model_version":    data.get("model_version", "1.0"),
        "inference_time_ms":data.get("inference_time_ms"),
        "image_quality":    data.get("image_quality"),
        "notes":            data.get("notes"),
        "mode":             data.get("mode"),
    }

    with _lock:
        try:
            conn   = _get_conn()
            cursor = conn.execute(sql, row)
            conn.commit()
            row_id = cursor.lastrowid
            logger.info(f"[db] Prediction saved (id={row_id})")
            return row_id
        except Exception as e:
            logger.error(f"[db] insert_prediction failed: {e}")
            return -1


def get_latest_prediction() -> dict | None:
    """Return the most recent prediction as a dict, or None."""
    sql = "SELECT * FROM predictions ORDER BY id DESC LIMIT 1"
    with _lock:
        try:
            row = _get_conn().execute(sql).fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"[db] get_latest_prediction failed: {e}")
            return None


def get_predictions(page: int = 1, per_page: int = 20,
                    crop: str = None, status: str = None) -> dict:
    """
    Return paginated predictions, newest first.

    Args:
        page:     1-indexed page number
        per_page: results per page
        crop:     optional filter by crop name
        status:   optional filter by status

    Returns:
        {"items": [...], "total": int, "page": int, "per_page": int, "pages": int}
    """
    where_clauses = []
    params: list  = []

    if crop:
        where_clauses.append("LOWER(crop) = LOWER(?)")
        params.append(crop)
    if status:
        where_clauses.append("status = ?")
        params.append(status)

    where = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    count_sql = f"SELECT COUNT(*) FROM predictions {where}"
    data_sql  = f"""
        SELECT * FROM predictions {where}
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """

    with _lock:
        try:
            conn    = _get_conn()
            total   = conn.execute(count_sql, params).fetchone()[0]
            offset  = (page - 1) * per_page
            rows    = conn.execute(data_sql, params + [per_page, offset]).fetchall()
            pages   = max(1, (total + per_page - 1) // per_page)
            return {
                "items":    [dict(r) for r in rows],
                "total":    total,
                "page":     page,
                "per_page": per_page,
                "pages":    pages,
            }
        except Exception as e:
            logger.error(f"[db] get_predictions failed: {e}")
            return {"items": [], "total": 0, "page": 1, "per_page": per_page, "pages": 0}


def get_prediction_by_id(pred_id: int) -> dict | None:
    """Return a single prediction by id."""
    with _lock:
        try:
            row = _get_conn().execute(
                "SELECT * FROM predictions WHERE id = ?", (pred_id,)
            ).fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"[db] get_prediction_by_id failed: {e}")
            return None


def get_stats() -> dict:
    """Return summary statistics for the dashboard."""
    sql = """
        SELECT
            COUNT(*)                                          AS total,
            SUM(CASE WHEN status='healthy'  THEN 1 ELSE 0 END) AS healthy,
            SUM(CASE WHEN status='diseased' THEN 1 ELSE 0 END) AS diseased,
            AVG(confidence)                                   AS avg_confidence,
            MAX(timestamp)                                    AS last_analysis
        FROM predictions
    """
    with _lock:
        try:
            row = _get_conn().execute(sql).fetchone()
            if row:
                return {
                    "total":          row["total"] or 0,
                    "healthy":        row["healthy"] or 0,
                    "diseased":       row["diseased"] or 0,
                    "avg_confidence": round(row["avg_confidence"] or 0, 3),
                    "last_analysis":  row["last_analysis"],
                }
            return {"total": 0, "healthy": 0, "diseased": 0,
                    "avg_confidence": 0, "last_analysis": None}
        except Exception as e:
            logger.error(f"[db] get_stats failed: {e}")
            return {}


# ─── Image Retention ──────────────────────────────────────────────────────────

def apply_image_retention() -> int:
    """
    Enforce image retention policy:
      - Delete image files when MAX_STORED_IMAGES is exceeded (oldest first)
      - Delete image files older than IMAGE_RETENTION_DAYS days
    Prediction metadata in SQLite is always kept.

    Returns: number of image files deleted
    """
    deleted = 0

    with _lock:
        conn = _get_conn()

        # 1. Count-based: delete oldest image files beyond limit
        count = conn.execute("SELECT COUNT(*) FROM predictions WHERE image_path IS NOT NULL").fetchone()[0]
        if count > MAX_STORED_IMAGES:
            excess = count - MAX_STORED_IMAGES
            old_rows = conn.execute(
                "SELECT id, image_path FROM predictions WHERE image_path IS NOT NULL "
                "ORDER BY id ASC LIMIT ?", (excess,)
            ).fetchall()
            for row in old_rows:
                deleted += _delete_image_file(conn, row["id"], row["image_path"])

        # 2. Age-based: delete images older than retention period
        cutoff = (datetime.now() - timedelta(days=IMAGE_RETENTION_DAYS)).isoformat()
        old_rows = conn.execute(
            "SELECT id, image_path FROM predictions "
            "WHERE image_path IS NOT NULL AND timestamp < ?", (cutoff,)
        ).fetchall()
        for row in old_rows:
            deleted += _delete_image_file(conn, row["id"], row["image_path"])

        conn.commit()

    if deleted:
        logger.info(f"[db] Image retention: deleted {deleted} image files")
    return deleted


def _delete_image_file(conn: sqlite3.Connection, pred_id: int, image_path: str) -> int:
    """Delete an image file and clear its path in the DB."""
    try:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        conn.execute(
            "UPDATE predictions SET image_path = NULL, notes = 'Image deleted (retention policy)' "
            "WHERE id = ?", (pred_id,)
        )
        return 1
    except Exception as e:
        logger.warning(f"[db] Failed to delete image {image_path}: {e}")
        return 0


# ─── Settings ─────────────────────────────────────────────────────────────────

def get_setting(key: str, default=None):
    """Retrieve a persisted setting value."""
    with _lock:
        try:
            row = _get_conn().execute(
                "SELECT value FROM settings WHERE key = ?", (key,)
            ).fetchone()
            return row["value"] if row else default
        except Exception as e:
            logger.error(f"[db] get_setting({key}) failed: {e}")
            return default


def set_setting(key: str, value) -> bool:
    """Persist a setting value (insert or replace)."""
    with _lock:
        try:
            conn = _get_conn()
            conn.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, str(value))
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"[db] set_setting({key}) failed: {e}")
            return False


def get_all_settings() -> dict:
    """Return all settings as a dict."""
    with _lock:
        try:
            rows = _get_conn().execute("SELECT key, value FROM settings").fetchall()
            return {r["key"]: r["value"] for r in rows}
        except Exception as e:
            logger.error(f"[db] get_all_settings failed: {e}")
            return {}


# ─── Sensor readings (future ESP32) ──────────────────────────────────────────

def insert_sensor_reading(data: dict) -> int:
    """Insert a sensor reading from the ESP32."""
    sql = """
        INSERT INTO sensor_readings
            (timestamp, soil_moisture, temperature, humidity, rainfall, water_level)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    with _lock:
        try:
            conn = _get_conn()
            cursor = conn.execute(sql, (
                data.get("timestamp", datetime.now().isoformat()),
                data.get("soil_moisture"),
                data.get("temperature"),
                data.get("humidity"),
                data.get("rainfall"),
                data.get("water_level"),
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"[db] insert_sensor_reading failed: {e}")
            return -1


def get_latest_sensor_reading() -> dict | None:
    """Return the most recent sensor reading."""
    with _lock:
        try:
            row = _get_conn().execute(
                "SELECT * FROM sensor_readings ORDER BY id DESC LIMIT 1"
            ).fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"[db] get_latest_sensor_reading failed: {e}")
            return None
