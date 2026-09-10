"""
services/health_service.py — System health checker.

Checks camera, AI model, database, storage, and internet (optional).
Internet check is passive — a failed check NEVER blocks any local operation.
"""

import os
import socket
import logging
import shutil
from datetime import datetime

from config import (IMAGE_DIR, DB_PATH, LOG_DIR,
                    INTERNET_CHECK_HOST, INTERNET_CHECK_PORT,
                    INTERNET_CHECK_TIMEOUT)

logger = logging.getLogger(__name__)

# Injected at app startup to avoid circular imports
_inference_engine = None
_camera_status    = None    # cached from last camera check


def set_inference_engine(engine):
    global _inference_engine
    _inference_engine = engine


def set_camera_status(status: dict):
    global _camera_status
    _camera_status = status


def get_status() -> dict:
    """
    Return a full system health status dict.

    All checks are non-blocking and fail-safe.
    Internet connectivity failure does NOT affect the "system" status.
    """
    status = {
        "system":     "online",
        "camera":     _check_camera(),
        "ai_model":   _check_ai_model(),
        "database":   _check_database(),
        "internet":   _check_internet(),
        "storage":    _check_storage(),
        "timestamp":  datetime.now().isoformat(),
    }
    return status


# ─── Individual checks ────────────────────────────────────────────────────────

def _check_camera() -> dict:
    if _camera_status is not None:
        return _camera_status
    # If not set yet, try a quick detect
    try:
        from camera.capture import detect_camera
        result = detect_camera()
        return result
    except Exception as e:
        return {"available": False, "backend": "unknown", "error": str(e)}


def _check_ai_model() -> dict:
    if _inference_engine is None:
        return {"ready": False, "mode": "not_loaded", "error": "Engine not initialised"}
    return {
        "ready": _inference_engine.is_ready,
        "mode":  _inference_engine.mode,
        "error": None,
    }


def _check_database() -> dict:
    try:
        from database.db import get_stats
        stats = get_stats()
        return {"ready": True, "total_predictions": stats.get("total", 0), "error": None}
    except Exception as e:
        return {"ready": False, "total_predictions": 0, "error": str(e)}


def _check_internet() -> dict:
    """
    Passive internet check via TCP socket.
    Returns immediately on failure — never blocks the system.
    The result is only used to display an indicator on the dashboard.
    """
    try:
        socket.setdefaulttimeout(INTERNET_CHECK_TIMEOUT)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((INTERNET_CHECK_HOST, INTERNET_CHECK_PORT))
        return {"connected": True, "error": None}
    except Exception:
        return {"connected": False, "error": None}   # silently offline


def _check_storage() -> dict:
    """Check disk space on the Pi microSD / PC drive."""
    try:
        usage  = shutil.disk_usage(IMAGE_DIR if os.path.exists(IMAGE_DIR) else os.getcwd())
        pct_free = (usage.free / usage.total) * 100
        warning  = pct_free < 10.0
        return {
            "total_gb":    round(usage.total / 1e9, 1),
            "free_gb":     round(usage.free  / 1e9, 1),
            "used_pct":    round(100 - pct_free, 1),
            "free_pct":    round(pct_free, 1),
            "low_warning": warning,
            "error":       None,
        }
    except Exception as e:
        return {"error": str(e), "low_warning": False}


def get_storage_warning() -> str | None:
    """Return a warning message if storage is low, else None."""
    s = _check_storage()
    if s.get("low_warning"):
        return f"Low storage: only {s['free_pct']:.1f}% free ({s['free_gb']} GB)"
    return None
