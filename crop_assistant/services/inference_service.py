"""
services/inference_service.py — Orchestrates the full analysis pipeline.

  Camera capture → AI inference → DB save → return result

Handles errors at each stage without crashing the Flask app.
"""

import os
import logging
from datetime import datetime

from ai.inference     import engine as inference_engine
from camera.capture   import capture_image, detect_camera
from database         import db
from services         import health_service

logger = logging.getLogger(__name__)


def run_analysis(triggered_by: str = "manual") -> dict:
    """
    Full pipeline: capture → preprocess → infer → save → return.

    Args:
        triggered_by: "manual" (dashboard button) or "scheduler" (automatic)

    Returns:
        dict with analysis result + metadata, or error dict on failure
    """
    logger.info(f"[inference_service] Analysis triggered by: {triggered_by}")

    # ── 1. Camera capture ────────────────────────────────────────────────────
    capture_result = capture_image()

    if not capture_result["success"]:
        error_msg = f"Camera capture failed: {capture_result.get('error', 'unknown')}"
        logger.error(f"[inference_service] {error_msg}")
        return _error_result(error_msg, capture_result=capture_result)

    image_path = capture_result["path"]
    logger.info(f"[inference_service] Image captured: {image_path}")

    # ── 2. AI inference ──────────────────────────────────────────────────────
    if not inference_engine._loaded:
        inference_engine.load()

    inference_result = inference_engine.run(image_path)

    if inference_result.get("status") == "error":
        error_msg = f"AI inference failed: {inference_result.get('error', 'unknown')}"
        logger.error(f"[inference_service] {error_msg}")
        return _error_result(error_msg, image_path=image_path)

    # ── 3. Save to database ──────────────────────────────────────────────────
    db_record = {**inference_result, "image_path": image_path,
                 "notes": f"triggered_by={triggered_by}"}
    pred_id = db.insert_prediction(db_record)

    if pred_id < 0:
        logger.warning("[inference_service] Failed to save prediction to database")

    # ── 4. Periodic image retention cleanup ──────────────────────────────────
    # Run occasionally (every 10th analysis) to avoid overhead on Pi
    try:
        total = db.get_stats().get("total", 0)
        if total % 10 == 0:
            db.apply_image_retention()
    except Exception:
        pass

    # ── 5. Build and return final result ────────────────────────────────────
    result = {
        **inference_result,
        "id":           pred_id,
        "image_path":   image_path,
        "triggered_by": triggered_by,
        "success":      True,
    }

    logger.info(
        f"[inference_service] Complete — "
        f"{result['crop']} / {result.get('disease') or 'Healthy'} "
        f"({result['confidence']:.0%}) id={pred_id}"
    )
    return result


def run_analysis_on_file(file_obj, filename: str = None, triggered_by: str = "upload") -> dict:
    """
    Process an uploaded image file: save to IMAGE_DIR → run AI inference → save to DB → return.

    Args:
        file_obj: File-like object (e.g., werkzeug FileStorage or PIL Image or bytes)
        filename: Optional original filename
        triggered_by: Label for tracking (default: "upload")

    Returns:
        dict with prediction details and DB record ID
    """
    from config import IMAGE_DIR
    os.makedirs(IMAGE_DIR, exist_ok=True)

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]
    safe_filename = f"upload_{timestamp_str}.jpg"
    target_path = os.path.join(IMAGE_DIR, safe_filename)

    try:
        if hasattr(file_obj, "save"):
            file_obj.save(target_path)
        elif hasattr(file_obj, "read"):
            with open(target_path, "wb") as f:
                f.write(file_obj.read())
        else:
            from PIL import Image
            if isinstance(file_obj, Image.Image):
                file_obj.convert("RGB").save(target_path, "JPEG")
            else:
                return _error_result("Unsupported file object type")
    except Exception as exc:
        err = f"Failed to save uploaded image: {exc}"
        logger.error(f"[inference_service] {err}")
        return _error_result(err)

    logger.info(f"[inference_service] Uploaded image saved: {target_path}")

    # AI inference
    if not inference_engine._loaded:
        inference_engine.load()

    inference_result = inference_engine.run(target_path)
    if inference_result.get("status") == "error":
        err = f"AI inference failed: {inference_result.get('error', 'unknown')}"
        logger.error(f"[inference_service] {err}")
        return _error_result(err, image_path=target_path)

    # Save to database
    db_record = {
        **inference_result,
        "image_path": target_path,
        "notes": f"triggered_by={triggered_by}" + (f" original={filename}" if filename else "")
    }
    pred_id = db.insert_prediction(db_record)

    result = {
        **inference_result,
        "id":             pred_id,
        "image_path":     target_path,
        "image_filename": safe_filename,
        "triggered_by":   triggered_by,
        "success":        True,
    }

    logger.info(
        f"[inference_service] Upload analysis complete — "
        f"{result['crop']} / {result.get('disease') or 'Healthy'} "
        f"({result['confidence']:.0%}) id={pred_id}"
    )
    return result


def _error_result(message: str, *, capture_result: dict = None,
                  image_path: str = None) -> dict:
    return {
        "success":          False,
        "error":            message,
        "crop":             None,
        "disease":          None,
        "status":           "error",
        "confidence":       0.0,
        "confidence_level": "low",
        "image_path":       image_path or (capture_result or {}).get("path"),
        "timestamp":        datetime.now().isoformat(),
    }
