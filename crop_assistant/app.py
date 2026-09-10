"""
app.py — AI Crop Assistant — Main Flask application entry point.

Startup sequence:
  1. Configure logging
  2. Initialise SQLite database
  3. Load AI model (once — kept in RAM)
  4. Detect camera
  5. Register API blueprint
  6. Start background scheduler (if enabled)
  7. Serve Flask dashboard

Runs on Pi Zero W:  python app.py
Dashboard URL:      http://<pi-ip>:5000
API URL:            http://<pi-ip>:5000/api/status
"""

import os
import logging
import logging.handlers
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, abort

from config import (FLASK_HOST, FLASK_PORT, FLASK_DEBUG,
                    LOG_FILE, LOG_DIR, LOG_MAX_BYTES, LOG_BACKUP_COUNT,
                    IMAGE_DIR, DB_PATH, BASE_DIR, SECRET_KEY,
                    FIREBASE_CONFIG, FIREBASE_RTDB_URL, FIREBASE_ENABLED,
                    SCHEDULER_ENABLED)

# ─── Logging Setup ────────────────────────────────────────────────────────────

def _setup_logging():
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        os.makedirs(IMAGE_DIR, exist_ok=True)
        os.makedirs(os.path.join(BASE_DIR, "ai", "model"), exist_ok=True)
    except Exception:
        pass

    fmt     = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Console handler (standard output for Vercel and local terminal)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(fmt, datefmt))
    root_logger.addHandler(ch)

    # Rotating file handler (when running on a writable filesystem)
    try:
        fh = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT
        )
        fh.setFormatter(logging.Formatter(fmt, datefmt))
        root_logger.addHandler(fh)
    except Exception:
        pass


_setup_logging()
logger = logging.getLogger(__name__)

# ─── Flask App ────────────────────────────────────────────────────────────────

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, "templates"),
            static_folder=os.path.join(BASE_DIR, "static"))

app.config["SECRET_KEY"]          = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"]  = 16 * 1024 * 1024   # 16 MB upload limit

# Jinja2 custom filter: {{ path|basename }}
app.jinja_env.filters["basename"] = os.path.basename

# ─── Initialise subsystems ────────────────────────────────────────────────────

logger.info("=" * 60)
logger.info(" KISAN MITRA AI — Circuit Maze Team (SIH 2026)")
logger.info(f" Flask {FLASK_HOST}:{FLASK_PORT}")
logger.info("=" * 60)

# 1. Database
from database.db import init_db
if not init_db():
    logger.critical("Database initialisation failed — check permissions and path")

# 2. AI Model
from ai.inference import engine as inference_engine
inference_engine.load()   # model stays loaded for the lifetime of the process

# 3. Camera
from camera.capture import detect_camera
camera_status = detect_camera()
logger.info(
    f"[app] Camera: {'READY' if camera_status['available'] else 'ERROR'} "
    f"(backend={camera_status['backend']})"
)

# 4. Health service — inject references
from services import health_service
health_service.set_inference_engine(inference_engine)
health_service.set_camera_status(camera_status)

# 5. API Blueprint
try:
    from api.routes import api_bp
except ModuleNotFoundError:
    from crop_assistant.api.routes import api_bp
app.register_blueprint(api_bp)

# 6. Scheduler
from services.scheduler import scheduler
if SCHEDULER_ENABLED:
    scheduler.start()
else:
    logger.info("[app] Scheduler disabled (serverless environment)")

logger.info("[app] All subsystems initialised — Flask starting")

# ─── Dashboard Routes ─────────────────────────────────────────────────────────

@app.route("/")
@app.route("/api/index")
@app.route("/api/index.py")
def index():
    """Main dashboard."""
    from database.db import get_latest_prediction, get_stats
    from services.health_service import get_status

    latest = get_latest_prediction()
    stats  = get_stats()
    status = get_status()

    # Recent 10 predictions for the dashboard table
    from database.db import get_predictions
    recent = get_predictions(page=1, per_page=10)["items"]

    from services.sensor_service import sensor_service
    sensors = sensor_service.get_current()

    return render_template("index.html",
                           latest=latest,
                           stats=stats,
                           status=status,
                           recent=recent,
                           sensors=sensors,
                           firebase_config=FIREBASE_CONFIG,
                           firebase_url=FIREBASE_RTDB_URL,
                           firebase_enabled=FIREBASE_ENABLED,
                           scheduler=scheduler.status,
                           now=datetime.now())


@app.route("/analytics")
def analytics():
    """Historical analytics, trends, and sensor graphs page."""
    from database.db import get_stats, get_predictions
    from services.sensor_service import sensor_service

    stats   = get_stats()
    sensors = sensor_service.get_current()
    history = sensor_service.get_history(hours=24)
    recent  = get_predictions(page=1, per_page=50)["items"]

    return render_template("analytics.html",
                           stats=stats,
                           sensors=sensors,
                           sensor_history=history,
                           recent=recent)


@app.route("/alerts")
def alerts():
    """Real-time environmental and crop disease alerts center."""
    from database.db import get_latest_prediction
    from services.sensor_service import sensor_service

    sensors = sensor_service.get_current()
    latest_pred = get_latest_prediction()

    return render_template("alerts.html",
                           sensors=sensors,
                           latest=latest_pred)


@app.route("/history")
def history():
    """Prediction history page."""
    from flask import request as freq
    from database.db import get_predictions

    page     = max(1, int(freq.args.get("page",   1)))
    crop     = freq.args.get("crop")
    status_f = freq.args.get("status")

    result = get_predictions(page=page, per_page=20, crop=crop, status=status_f)
    return render_template("history.html",
                           predictions=result["items"],
                           pagination=result,
                           crop_filter=crop,
                           status_filter=status_f)


@app.route("/image/<int:pred_id>")
def image_detail(pred_id):
    """Image + prediction detail page."""
    from database.db import get_prediction_by_id
    from ai.disease_knowledge import get_disease_dossier
    pred = get_prediction_by_id(pred_id)
    if pred is None:
        abort(404)
    
    # Enrich with dossier
    dossier = get_disease_dossier(pred.get("crop"), pred.get("disease"), pred.get("confidence") or 0.85)
    return render_template("image.html", prediction=pred, dossier=dossier)


@app.route("/settings")
def settings():
    """Settings page."""
    from database.db import get_all_settings
    all_settings = get_all_settings()
    return render_template("settings.html",
                           settings=all_settings,
                           scheduler=scheduler.status)


# ─── Captured image serving ───────────────────────────────────────────────────

@app.route("/captured_images/<path:filename>")
def serve_captured_image(filename):
    """Serve captured images directly from the filesystem."""
    from flask import send_from_directory
    return send_from_directory(IMAGE_DIR, filename)


# ─── Error handlers ──────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template("base.html",
                           error="Page not found (404)",
                           page_title="Not Found"), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"[app] 500 error: {e}")
    return render_template("base.html",
                           error=f"Internal server error: {e}",
                           page_title="Error"), 500


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG,
        use_reloader=False,     # disable reloader — it double-loads the model
        threaded=True,          # allow concurrent requests on LAN
    )
