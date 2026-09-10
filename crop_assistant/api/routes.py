"""
api/routes.py — REST API blueprint.

All endpoints return JSON.
Designed for:
  - Dashboard AJAX calls (analyze, status, latest)
  - Future ESP32 sensor/irrigation integration
  - LAN access from phones/tablets on the same Wi-Fi

No authentication required (local agricultural network).
Input validation is applied to POST endpoints.
"""

import os
import logging
from flask import Blueprint, jsonify, request, send_from_directory

from config import IMAGE_DIR, FIREBASE_CONFIG, FIREBASE_RTDB_URL, FIREBASE_ENABLED
from database import db
from services import health_service
from services.scheduler import scheduler

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__, url_prefix="/api")


# ─── Firebase RTDB Config & Sync ──────────────────────────────────────────────
@api_bp.route("/firebase/config", methods=["GET"])
def firebase_config():
    """Return Firebase RTDB web configuration for frontend client integration."""
    return jsonify({
        "enabled": FIREBASE_ENABLED,
        "databaseURL": FIREBASE_RTDB_URL,
        "config": FIREBASE_CONFIG
    })


@api_bp.route("/firebase/sync", methods=["POST"])
def firebase_sync():
    """Trigger manual fetch from Firebase RTDB and return parsed telemetry."""
    from services.sensor_service import sensor_service
    if not FIREBASE_RTDB_URL:
        return jsonify({
            "success": False,
            "message": "FIREBASE_RTDB_URL is not configured in environment variables",
            "data": sensor_service.get_current()
        }), 200

    fb_data = sensor_service._fetch_firebase()
    if fb_data:
        sensor_service._update_from_firebase(fb_data)
        return jsonify({"success": True, "source": "firebase-rtdb", "data": sensor_service.get_current()})
    return jsonify({"success": False, "message": "Could not reach Firebase RTDB or empty payload", "data": sensor_service.get_current()})



# ─── GET /api/status ──────────────────────────────────────────────────────────
@api_bp.route("/status", methods=["GET"])
def status():
    """System health status — safe to call frequently from dashboard."""
    s      = health_service.get_status()
    camera = s.get("camera", {})
    ai     = s.get("ai_model", {})
    db_s   = s.get("database", {})
    inet   = s.get("internet", {})
    stor   = s.get("storage", {})

    return jsonify({
        "system":   "online",
        "camera":   "ready"   if camera.get("available") else "error",
        "ai_model": "ready"   if ai.get("ready")        else ai.get("mode", "loading"),
        "database": "ready"   if db_s.get("ready")      else "error",
        "internet": inet.get("connected", False),
        "storage":  {
            "free_pct":    stor.get("free_pct"),
            "low_warning": stor.get("low_warning", False),
        },
        "scheduler": scheduler.status,
        "details":  s,
    })


# ─── GET /api/latest ──────────────────────────────────────────────────────────
@api_bp.route("/latest", methods=["GET"])
def latest():
    """Return the most recent prediction."""
    pred = db.get_latest_prediction()
    if pred is None:
        return jsonify({"message": "No predictions yet"}), 404
    return jsonify(_safe_prediction(pred))


# ─── GET /api/predictions ─────────────────────────────────────────────────────
@api_bp.route("/predictions", methods=["GET"])
def predictions():
    """Return paginated prediction history."""
    page     = max(1, int(request.args.get("page",     1)))
    per_page = max(1, min(100, int(request.args.get("per_page", 20))))
    crop     = request.args.get("crop")
    status_f = request.args.get("status")

    result = db.get_predictions(page=page, per_page=per_page,
                                 crop=crop, status=status_f)
    result["items"] = [_safe_prediction(p) for p in result["items"]]
    return jsonify(result)


# ─── POST /api/analyze ────────────────────────────────────────────────────────
@api_bp.route("/analyze", methods=["POST"])
def analyze():
    """
    Trigger a manual capture + inference cycle.
    Returns the inference result (may take several seconds on Pi Zero W).
    """
    from services.inference_service import run_analysis
    logger.info("[api] Manual analysis triggered via /api/analyze")
    result = run_analysis(triggered_by="manual")
    status_code = 200 if result.get("success") else 500
    return jsonify(result), status_code


# ─── POST /api/upload ─────────────────────────────────────────────────────────
@api_bp.route("/upload", methods=["POST"])
def upload_image():
    """
    Upload an image file from the browser and run AI disease analysis.
    Accepts multipart/form-data with file field 'image' or 'file'.
    """
    from services.inference_service import run_analysis_on_file
    
    file_item = request.files.get("image") or request.files.get("file")
    if not file_item or not file_item.filename:
        return jsonify({"success": False, "error": "No image file provided in upload"}), 400

    allowed_exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    ext = os.path.splitext(file_item.filename)[1].lower()
    if ext not in allowed_exts:
        return jsonify({"success": False, "error": f"Unsupported format '{ext}'. Allowed: JPG, PNG, WEBP, BMP"}), 400

    logger.info(f"[api] Image uploaded for analysis: {file_item.filename}")
    result = run_analysis_on_file(file_item, filename=file_item.filename, triggered_by="upload")
    status_code = 200 if result.get("success") else 500
    return jsonify(result), status_code


# ─── Environmental IoT Endpoints ──────────────────────────────────────────────

@api_bp.route("/sensors/live", methods=["GET"])
def live_sensors():
    """Return live environmental sensor telemetry and safety status."""
    from services.sensor_service import sensor_service
    return jsonify(sensor_service.get_current())


@api_bp.route("/sensors", methods=["POST"])
def ingest_sensors():
    """
    Ingest readings from physical ESP32.
    Payload: {"temperature": 28.5, "humidity": 65, "gasRaw": 750, "soilRaw": 2100}
    """
    from services.sensor_service import sensor_service
    payload = request.get_json(silent=True) or {}
    updated = sensor_service.ingest_esp32_data(payload)
    return jsonify({"success": True, "data": updated})


@api_bp.route("/relay", methods=["POST"])
def set_relay():
    """
    Control the irrigation relay.
    Body: {"state": true/false, "mode": "manual" | "auto"}
    """
    from services.sensor_service import sensor_service
    payload = request.get_json(silent=True) or {}
    state = bool(payload.get("state", False))
    mode = payload.get("mode", "manual")
    result = sensor_service.set_relay(state, mode)
    return jsonify({"success": True, **result})


@api_bp.route("/sensors/history", methods=["GET"])
def sensor_history():
    """Return historical time series data for dashboard analytics charts."""
    from services.sensor_service import sensor_service
    hours = max(1, min(168, int(request.args.get("hours", 24))))
    history = sensor_service.get_history(hours=hours)
    return jsonify({"success": True, "count": len(history), "data": history})


@api_bp.route("/alerts", methods=["GET"])
def get_alerts():
    """Return active and recent environmental safety / crop health alerts."""
    from services.sensor_service import sensor_service
    curr = sensor_service.get_current()
    latest_pred = db.get_latest_prediction()

    alerts = []
    # Environmental alerts
    if curr.get("temperatureDanger"):
        alerts.append({
            "id": 1, "type": "HIGH_TEMPERATURE", "severity": "CRITICAL",
            "message": f"Temperature reached {curr.get('temperature')}°C (Danger threshold: >= 35°C). Risk of crop heat stress.",
            "timestamp": curr.get("timestamp"), "status": "ACTIVE"
        })
    if curr.get("humidityDanger"):
        alerts.append({
            "id": 2, "type": "LOW_HUMIDITY", "severity": "WARNING",
            "message": f"Relative humidity dropped to {curr.get('humidity')}% (Threshold: <= 30%). Desiccation risk.",
            "timestamp": curr.get("timestamp"), "status": "ACTIVE"
        })
    if curr.get("gasDanger"):
        alerts.append({
            "id": 3, "type": "HIGH_GAS_LEVEL", "severity": "CRITICAL",
            "message": f"Gas / smoke sensor detected abnormal level: {curr.get('gasRaw')} ADC. Inspect field perimeter.",
            "timestamp": curr.get("timestamp"), "status": "ACTIVE"
        })
    if curr.get("soilDry"):
        alerts.append({
            "id": 4, "type": "SOIL_MOISTURE_DEFICIT", "severity": "WARNING",
            "message": f"Soil moisture at {curr.get('soilMoisture')}% (< 30%). Irrigation relay {'activated' if curr.get('relay') else 'recommended'}.",
            "timestamp": curr.get("timestamp"), "status": "ACTIVE"
        })

    # Disease alert from latest prediction
    if latest_pred and latest_pred.get("status") == "diseased":
        alerts.append({
            "id": 5, "type": "CROP_DISEASE_DETECTED", "severity": "HIGH",
            "message": f"Detected {latest_pred.get('disease')} on {latest_pred.get('crop')} (Confidence: {int((latest_pred.get('confidence') or 0)*100)}%). Review treatment plan.",
            "timestamp": latest_pred.get("timestamp"), "status": "ACTIVE"
        })

    return jsonify({"success": True, "alerts": alerts, "count": len(alerts)})


# ─── GET /api/settings ────────────────────────────────────────────────────────
@api_bp.route("/settings", methods=["GET"])
def get_settings():
    """Return all persisted settings."""
    return jsonify(db.get_all_settings())


# ─── POST /api/settings ───────────────────────────────────────────────────────
@api_bp.route("/settings", methods=["POST"])
def update_settings():
    """
    Update one or more settings.
    Body: {"key": "value", ...}
    """
    data    = request.get_json(silent=True) or {}
    updated = {}
    errors  = {}

    VALID_KEYS = {
        "scheduler_interval_min", "scheduler_enabled",
        "confidence_high", "confidence_medium",
        "max_stored_images", "image_retention_days",
    }

    for key, value in data.items():
        if key not in VALID_KEYS:
            errors[key] = "Unknown setting key"
            continue
        if db.set_setting(key, value):
            updated[key] = value
            # Apply live changes
            if key == "scheduler_interval_min":
                try:
                    scheduler.update_interval(int(value))
                except Exception:
                    pass
            if key == "scheduler_enabled":
                scheduler.set_enabled(str(value).lower() == "true")
        else:
            errors[key] = "Failed to save"

    return jsonify({"updated": updated, "errors": errors})


# ─── POST /api/sensors (future ESP32) ─────────────────────────────────────────
@api_bp.route("/sensors", methods=["POST"])
def sensors():
    """Accept sensor data from ESP32 (future integration)."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    ALLOWED = {"soil_moisture", "temperature", "humidity", "rainfall", "water_level"}
    clean   = {k: v for k, v in data.items() if k in ALLOWED}

    row_id = db.insert_sensor_reading(clean)
    if row_id < 0:
        return jsonify({"error": "Failed to save sensor reading"}), 500
    return jsonify({"id": row_id, "status": "saved"}), 201


# ─── GET /api/sensors/latest ──────────────────────────────────────────────────
@api_bp.route("/sensors/latest", methods=["GET"])
def sensors_latest():
    """Return the most recent sensor reading (ESP32 data)."""
    reading = db.get_latest_sensor_reading()
    if reading is None:
        return jsonify({"message": "No sensor data yet"}), 404
    return jsonify(reading)


# ─── GET /captured_images/<filename> ─────────────────────────────────────────
@api_bp.route("/image/<path:filename>", methods=["GET"])
def serve_image(filename):
    """Serve a captured crop image."""
    return send_from_directory(IMAGE_DIR, filename)


# ─── Helper ───────────────────────────────────────────────────────────────────

def _safe_prediction(pred: dict) -> dict:
    """Return a JSON-safe prediction dict."""
    p = dict(pred)
    # Make image path relative (for template use)
    if p.get("image_path"):
        p["image_filename"] = os.path.basename(p["image_path"])
    else:
        p["image_filename"] = None
    return p
