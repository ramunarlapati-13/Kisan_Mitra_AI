"""
config.py — Central configuration for Kisan Mitra AI.
Created by Circuit Maze Team as part of SIH 2026.
All settings can be overridden via environment variables or .env file.
"""

import os

# ─── Base Paths ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Environment Variables Loader (Zero-dependency .env reader) ───────────────
def _load_dotenv():
    """Discover and parse .env files automatically without external dependencies."""
    candidates = [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(BASE_DIR, ".env"),
        os.path.join(os.path.dirname(BASE_DIR), ".env")
    ]
    for env_path in candidates:
        if os.path.isfile(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        key, val = line.split("=", 1)
                        key = key.strip()
                        val = val.strip().strip("\"'")
                        if key and key not in os.environ:
                            os.environ[key] = val
            except Exception:
                pass
            break

_load_dotenv()

# ─── Secret Key ───────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get("SECRET_KEY", "crop-assistant-local-secret-key")

# ─── AI Model ─────────────────────────────────────────────────────────────────
MODEL_PATH        = os.path.join(BASE_DIR, "ai", "model", "crop_disease.tflite")
HUGGINGFACE_MODEL = os.environ.get("HUGGINGFACE_MODEL", "LishaV01/agriculture-crop-disease-detection")
MODEL_VERSION     = "1.0"

# Input resolution (read from preprocessor_config.json; 224 is the ViT default)
MODEL_INPUT_SIZE = int(os.environ.get("MODEL_INPUT_SIZE", 224))

# Normalization (ViT standard — derived from model's preprocessor_config.json)
NORMALIZE_MEAN = [0.5, 0.5, 0.5]
NORMALIZE_STD  = [0.5, 0.5, 0.5]

# ─── Confidence Thresholds ────────────────────────────────────────────────────
CONFIDENCE_HIGH   = float(os.environ.get("CONFIDENCE_HIGH",   0.80))
CONFIDENCE_MEDIUM = float(os.environ.get("CONFIDENCE_MEDIUM", 0.60))

# ─── Serverless Detection ───────────────────────────────────────────────────
IS_SERVERLESS = bool(os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))

# ─── Database ─────────────────────────────────────────────────────────────────
if IS_SERVERLESS:
    import tempfile
    _tmp = tempfile.gettempdir()
    DB_PATH = os.environ.get("DB_PATH", os.path.join(_tmp, "crop_assistant.db"))
    IMAGE_DIR = os.path.join(_tmp, "captured_images")
    LOG_DIR = os.path.join(_tmp, "logs")
    LOG_FILE = os.path.join(LOG_DIR, "crop_assistant.log")
    SCHEDULER_ENABLED = False
else:
    DB_PATH = os.path.join(BASE_DIR, "database", "crop_assistant.db")
    IMAGE_DIR = os.path.join(BASE_DIR, "captured_images")
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    LOG_FILE = os.path.join(LOG_DIR, "crop_assistant.log")
    SCHEDULER_ENABLED = os.environ.get("SCHEDULER_ENABLED", "true").lower() == "true"

MAX_STORED_IMAGES    = int(os.environ.get("MAX_STORED_IMAGES", 500))
IMAGE_RETENTION_DAYS = int(os.environ.get("IMAGE_RETENTION_DAYS", 30))

# ─── Scheduler ────────────────────────────────────────────────────────────────
SCHEDULER_INTERVALS   = [15, 30, 60]
SCHEDULER_DEFAULT_MIN = int(os.environ.get("SCHEDULER_DEFAULT_MIN", 60))

# ─── Camera ───────────────────────────────────────────────────────────────────
CAMERA_RESOLUTION     = (1920, 1080)   # capture resolution; resized before inference
CAMERA_WARMUP_SECONDS = 2              # stabilisation time before capture
CAMERA_JPEG_QUALITY   = 85

# ─── Logging ──────────────────────────────────────────────────────────────────
LOG_MAX_BYTES    = 5 * 1024 * 1024    # 5 MB
LOG_BACKUP_COUNT = 3

# ─── Flask / Dashboard ────────────────────────────────────────────────────────
FLASK_HOST  = os.environ.get("FLASK_HOST",  "0.0.0.0")
FLASK_PORT  = int(os.environ.get("FLASK_PORT",  5000))
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

# ─── Internet check (passive / non-blocking) ──────────────────────────────────
INTERNET_CHECK_HOST    = "8.8.8.8"
INTERNET_CHECK_PORT    = 53
INTERNET_CHECK_TIMEOUT = 2   # seconds

# ─── Firebase Realtime Database (RTDB) ─────────────────────────────────────────
FIREBASE_ENABLED  = os.environ.get("FIREBASE_ENABLED", "true").lower() == "true"
FIREBASE_RTDB_URL = os.environ.get("FIREBASE_RTDB_URL", "").rstrip("/")

FIREBASE_CONFIG = {
    "apiKey":            os.environ.get("FIREBASE_API_KEY", ""),
    "authDomain":        os.environ.get("FIREBASE_AUTH_DOMAIN", ""),
    "databaseURL":       FIREBASE_RTDB_URL,
    "projectId":         os.environ.get("FIREBASE_PROJECT_ID", ""),
    "storageBucket":     os.environ.get("FIREBASE_STORAGE_BUCKET", ""),
    "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID", ""),
    "appId":             os.environ.get("FIREBASE_APP_ID", "")
}
