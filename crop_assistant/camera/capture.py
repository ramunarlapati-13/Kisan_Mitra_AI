"""
camera/capture.py — Camera abstraction layer.

Auto-detects the available camera backend in this order:

  1. picamera2  (Raspberry Pi — primary backend for Pi Zero W)
  2. OpenCV     (cv2 — PC webcam fallback)
  3. Test stub  (generates a synthetic green-leaf image for UI/AI testing on PC)

The camera is NEVER imported at module level — imports are deferred so the
application starts cleanly on any platform.

All images are saved as timestamped JPEGs in the captured_images/ directory.
"""

import os
import io
import time
import logging
import numpy as np
from datetime import datetime
from PIL import Image

from config import (IMAGE_DIR, CAMERA_RESOLUTION, CAMERA_WARMUP_SECONDS,
                    CAMERA_JPEG_QUALITY)

logger = logging.getLogger(__name__)

# Ensure image directory exists
try:
    os.makedirs(IMAGE_DIR, exist_ok=True)
except Exception:
    pass


def get_backend() -> str:
    """Detect which camera backend is available."""
    try:
        import picamera2  # noqa: F401
        return "picamera2"
    except ImportError:
        pass

    try:
        import cv2  # noqa: F401
        return "opencv"
    except ImportError:
        pass

    return "stub"


_BACKEND = None   # cached after first detection


def detect_camera() -> dict:
    """
    Check camera availability and return a status dict.

    Returns:
        {"available": bool, "backend": str, "error": str|None}
    """
    global _BACKEND
    _BACKEND = get_backend()

    if _BACKEND == "picamera2":
        try:
            from picamera2 import Picamera2
            cam = Picamera2()
            cam.close()
            return {"available": True, "backend": "picamera2", "error": None}
        except Exception as e:
            return {"available": False, "backend": "picamera2", "error": str(e)}

    if _BACKEND == "opencv":
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            ok  = cap.isOpened()
            cap.release()
            if ok:
                return {"available": True, "backend": "opencv", "error": None}
            return {"available": False, "backend": "opencv",
                    "error": "VideoCapture(0) could not be opened"}
        except Exception as e:
            return {"available": False, "backend": "opencv", "error": str(e)}

    # Stub — always "available" for testing
    return {"available": True, "backend": "stub",
            "error": "Running in test-stub mode — no physical camera detected"}


def capture_image(filename: str = None) -> dict:
    """
    Capture one image and save it to IMAGE_DIR.

    Args:
        filename: optional override; if None, a timestamped name is generated

    Returns:
        {
            "success":    bool,
            "path":       str (absolute path to saved JPEG),
            "filename":   str,
            "backend":    str,
            "error":      str | None,
            "timestamp":  str (ISO format),
        }
    """
    global _BACKEND
    if _BACKEND is None:
        _BACKEND = get_backend()

    if filename is None:
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"crop_{ts}.jpg"

    save_path = os.path.join(IMAGE_DIR, filename)
    timestamp = datetime.now().isoformat()

    if _BACKEND == "picamera2":
        return _capture_picamera2(save_path, filename, timestamp)
    elif _BACKEND == "opencv":
        return _capture_opencv(save_path, filename, timestamp)
    else:
        return _capture_stub(save_path, filename, timestamp)


# ─── Backend implementations ──────────────────────────────────────────────────

def _capture_picamera2(save_path: str, filename: str, timestamp: str) -> dict:
    try:
        from picamera2 import Picamera2

        cam = Picamera2()
        config = cam.create_still_configuration(
            main={"size": CAMERA_RESOLUTION, "format": "RGB888"}
        )
        cam.configure(config)
        cam.start()
        time.sleep(CAMERA_WARMUP_SECONDS)    # let sensor stabilise

        frame = cam.capture_array()          # numpy (H, W, 3) RGB
        cam.stop()
        cam.close()

        img = Image.fromarray(frame, mode="RGB")
        img.save(save_path, "JPEG", quality=CAMERA_JPEG_QUALITY)

        logger.info(f"[camera] Captured via picamera2 → {save_path}")
        return {"success": True, "path": save_path, "filename": filename,
                "backend": "picamera2", "error": None, "timestamp": timestamp}

    except Exception as e:
        logger.error(f"[camera] picamera2 capture failed: {e}")
        return {"success": False, "path": None, "filename": filename,
                "backend": "picamera2", "error": str(e), "timestamp": timestamp}


def _capture_opencv(save_path: str, filename: str, timestamp: str) -> dict:
    try:
        import cv2

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("VideoCapture(0) could not be opened")

        time.sleep(CAMERA_WARMUP_SECONDS)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise RuntimeError("Failed to read frame from camera")

        # OpenCV returns BGR — convert to RGB for PIL
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img.save(save_path, "JPEG", quality=CAMERA_JPEG_QUALITY)

        logger.info(f"[camera] Captured via OpenCV → {save_path}")
        return {"success": True, "path": save_path, "filename": filename,
                "backend": "opencv", "error": None, "timestamp": timestamp}

    except Exception as e:
        logger.error(f"[camera] OpenCV capture failed: {e}")
        return {"success": False, "path": None, "filename": filename,
                "backend": "opencv", "error": str(e), "timestamp": timestamp}


def _capture_stub(save_path: str, filename: str, timestamp: str) -> dict:
    """
    Generate a synthetic green-leaf test image.
    Used on PC when no camera is available.
    The image is valid and will produce a real AI inference result.
    """
    try:
        img = _generate_test_leaf_image()
        img.save(save_path, "JPEG", quality=CAMERA_JPEG_QUALITY)

        logger.info(f"[camera] Generated test-stub image → {save_path}")
        return {"success": True, "path": save_path, "filename": filename,
                "backend": "stub", "error": None, "timestamp": timestamp}

    except Exception as e:
        logger.error(f"[camera] Stub image generation failed: {e}")
        return {"success": False, "path": None, "filename": filename,
                "backend": "stub", "error": str(e), "timestamp": timestamp}


def _generate_test_leaf_image(size: int = 640) -> Image.Image:
    """
    Create a synthetic green leaf image for testing.
    Includes gradients and texture so it is a valid input for the model.
    """
    rng = np.random.default_rng(int(time.time()) % 1000)

    # Green base with variation
    r_ch = rng.integers(30,  80,  (size, size), dtype=np.uint8)
    g_ch = rng.integers(80,  180, (size, size), dtype=np.uint8)
    b_ch = rng.integers(20,  60,  (size, size), dtype=np.uint8)

    arr = np.stack([r_ch, g_ch, b_ch], axis=-1)

    # Add a radial vignette to simulate a leaf shape
    cx, cy = size // 2, size // 2
    Y, X   = np.ogrid[:size, :size]
    dist   = np.sqrt((X - cx)**2 + (Y - cy)**2)
    mask   = (dist < size * 0.45).astype(np.float32)
    arr    = (arr * mask[:, :, np.newaxis]).astype(np.uint8)

    return Image.fromarray(arr, mode="RGB")
