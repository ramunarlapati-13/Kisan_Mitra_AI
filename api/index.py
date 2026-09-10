import os
import sys

# Ensure crop_assistant and workspace root are on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
CROP_ASSISTANT_DIR = os.path.join(ROOT_DIR, "crop_assistant")

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if CROP_ASSISTANT_DIR not in sys.path:
    sys.path.insert(0, CROP_ASSISTANT_DIR)

# Mark serverless environment
os.environ.setdefault("VERCEL", "1")

from app import app

# Vercel Serverless Function entry point
app = app
