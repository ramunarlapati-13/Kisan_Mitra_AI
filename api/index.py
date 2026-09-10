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

# 5. Vercel Path Middleware
# When Vercel rewrites requests to /api/index, PATH_INFO in WSGI is set to /api/index.
# This middleware restores the true incoming path requested by the browser.
class VercelPathMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        if path in ("/api/index", "/api/index.py", "/api/index/"):
            # Check headers injected by Vercel's edge routing for the original path
            orig = (
                environ.get("HTTP_X_FORWARDED_PATH") or
                environ.get("HTTP_X_VERCEL_FORWARDED_PATH") or
                environ.get("HTTP_X_MATCHED_PATH") or
                environ.get("REQUEST_URI") or
                environ.get("RAW_URI") or
                "/"
            )
            # Strip query string if present
            if "?" in orig:
                orig = orig.split("?")[0]
            if orig in ("/api/index", "/api/index.py", "/api/index/"):
                orig = "/"
            environ["PATH_INFO"] = orig
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

# Vercel Serverless Function WSGI entry point
app = app
