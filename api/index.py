import os
import sys
import urllib.parse

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
# When Vercel rewrites requests to /api/index?__vercel_path=$1, this middleware
# dynamically restores the true original route requested by the browser.
class VercelPathMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        query_string = environ.get("QUERY_STRING", "")
        if "__vercel_path=" in query_string:
            try:
                parsed = urllib.parse.parse_qs(query_string, keep_blank_values=True)
                if "__vercel_path" in parsed:
                    raw_path = parsed["__vercel_path"][0]
                    clean_path = "/" + raw_path.lstrip("/")
                    environ["PATH_INFO"] = clean_path

                    # Filter out __vercel_path from QUERY_STRING so request.args stays clean
                    filtered = [
                        (k, v) for k, vs in parsed.items() if k != "__vercel_path" for v in vs
                    ]
                    environ["QUERY_STRING"] = urllib.parse.urlencode(filtered)
            except Exception:
                pass
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

# Vercel Serverless Function WSGI entry point
app = app
