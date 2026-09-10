import os
import sys

# 1. Resolve path locations
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
CROP_ASSISTANT_DIR = os.path.join(ROOT_DIR, "crop_assistant")

# 2. Mark serverless runtime environment
os.environ.setdefault("VERCEL", "1")

# 3. Add directories to Python module search path
if CROP_ASSISTANT_DIR not in sys.path:
    sys.path.insert(0, CROP_ASSISTANT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# 4. Resolve package collision: unshadow the root "api" directory so
# that crop_assistant/api/routes.py can be cleanly resolved.
if "api" in sys.modules and not hasattr(sys.modules["api"], "routes"):
    del sys.modules["api"]

from app import app

# Vercel Serverless Function WSGI entry point
app = app
