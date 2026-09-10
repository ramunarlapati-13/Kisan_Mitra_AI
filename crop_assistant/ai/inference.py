"""
ai/inference.py — AI inference engine for crop disease detection.

Supports three modes (auto-detected at startup):

  1. TFLite mode  (PRIMARY — used on Raspberry Pi Zero W)
     Requires: tflite-runtime (ARMv6 wheel) OR tensorflow (PC only)
     Model:    ai/model/crop_disease.tflite
     Completely offline — no network calls.

  2. PyTorch / HuggingFace mode  (FALLBACK — PC development only)
     Requires: torch, transformers
     Downloads model on first run (needs internet once, then cached locally).
     DO NOT use on Pi Zero W — too heavy.

  3. Demo mode  (LAST RESORT — when no model is available)
     Returns a synthetic prediction for UI testing only.
     Clearly labelled as DEMO in the result.

Model is loaded ONCE at startup and kept in memory.
Do not call load() for every inference — this is expensive on Pi Zero W.
"""

import os
import time
import logging
import numpy as np
from datetime import datetime

from config import (MODEL_PATH, HUGGINGFACE_MODEL, MODEL_VERSION,
                    CONFIDENCE_HIGH, CONFIDENCE_MEDIUM, IS_SERVERLESS)
from ai.labels import LABELS, get_label, parse_label, classify_confidence, update_labels_from_model
from ai.preprocessing import preprocess

logger = logging.getLogger(__name__)


class InferenceEngine:
    """
    Singleton-style inference engine.
    Call load() once at startup, then run() for each image.
    """

    def __init__(self):
        self._mode        = None   # "tflite" | "pytorch" | "demo"
        self._interpreter = None   # TFLite interpreter
        self._pt_model    = None   # PyTorch model (PC fallback)
        self._pt_processor= None   # HF processor (PC fallback)
        self._input_index = None
        self._output_index= None
        self._loaded      = False
        self.model_version= MODEL_VERSION

    # ──────────────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────────────

    def load(self) -> bool:
        """
        Load the AI model. Try TFLite first, then PyTorch, then Demo.
        Returns True if a real model (TFLite or PyTorch) was loaded.
        """
        if self._loaded:
            return self._mode != "demo"

        # 1. Try TFLite
        if self._try_load_tflite():
            logger.info(f"[inference] TFLite model loaded from {MODEL_PATH}")
            self._loaded = True
            return True

        # 2. Try PyTorch (PC fallback)
        if self._try_load_pytorch():
            logger.info(f"[inference] PyTorch model loaded from HuggingFace cache")
            self._loaded = True
            return True

        # 3. Demo mode
        logger.warning("[inference] No model available — running in DEMO mode")
        self._mode   = "demo"
        self._loaded = True
        return False

    @property
    def is_ready(self) -> bool:
        return self._loaded and self._mode != "demo"

    @property
    def mode(self) -> str:
        return self._mode or "not_loaded"

    def run(self, image_source) -> dict:
        """
        Run inference on an image.

        Args:
            image_source: file path (str) or PIL.Image.Image

        Returns:
            dict with keys:
                crop, disease, status, confidence, confidence_level,
                raw_label, timestamp, model_version, inference_time_ms, mode
        """
        if not self._loaded:
            self.load()

        from ai.quality_check import evaluate_image_quality
        from ai.disease_knowledge import get_disease_dossier

        # 1. Quality evaluation
        quality_eval = evaluate_image_quality(image_source)

        t_start = time.perf_counter()

        if self._mode == "tflite":
            result = self._run_tflite(image_source)
        elif self._mode == "pytorch":
            result = self._run_pytorch(image_source)
        else:
            result = self._run_demo()

        t_end = time.perf_counter()
        inference_ms = round((t_end - t_start) * 1000, 1)

        result["inference_time_ms"] = inference_ms
        result["timestamp"]         = datetime.now().isoformat()
        result["model_version"]     = self.model_version
        result["mode"]              = self._mode

        # 2. Enrich with agronomic knowledge dossier
        dossier = get_disease_dossier(result.get("crop"), result.get("disease"), result.get("confidence", 0.85))
        result.update({
            "pathogen":           dossier.get("pathogen"),
            "pathogen_type":      dossier.get("pathogen_type"),
            "severity":           dossier.get("severity"),
            "health_score":       dossier.get("health_score", 80),
            "symptoms":           dossier.get("symptoms", []),
            "immediate_action":   dossier.get("immediate_action"),
            "chemical_treatment": dossier.get("chemical_treatment", {}),
            "organic_treatment":  dossier.get("organic_treatment", {}),
            "prevention":         dossier.get("prevention", []),
            "environmental_risk": dossier.get("environmental_risk"),
            "image_quality":      quality_eval.get("quality_score", 90),
            "quality_eval":       quality_eval,
        })

        logger.info(
            f"[inference] {result['crop']} / {result['disease']} "
            f"conf={result['confidence']:.2%} ({result['confidence_level']}) "
            f"score={result['health_score']}/100 {inference_ms}ms [{self._mode}]"
        )
        return result

    # ──────────────────────────────────────────────────────────────────────────
    # TFLite
    # ──────────────────────────────────────────────────────────────────────────

    def _try_load_tflite(self) -> bool:
        if not os.path.exists(MODEL_PATH):
            logger.info(f"[inference] TFLite model not found at {MODEL_PATH}")
            return False

        interpreter = None

        # Try tflite-runtime first (lightweight, ARMv6-compatible)
        try:
            import tflite_runtime.interpreter as tflite
            interpreter = tflite.Interpreter(model_path=MODEL_PATH)
            logger.info("[inference] Using tflite-runtime")
        except ImportError:
            pass

        # Fallback to tensorflow.lite (PC only)
        if interpreter is None:
            try:
                import tensorflow as tf
                interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
                logger.info("[inference] Using tensorflow.lite (PC fallback)")
            except ImportError:
                pass

        if interpreter is None:
            logger.warning("[inference] Neither tflite-runtime nor tensorflow found")
            return False

        try:
            interpreter.allocate_tensors()
            input_details  = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            self._interpreter  = interpreter
            self._input_index  = input_details[0]["index"]
            self._output_index = output_details[0]["index"]
            self._mode         = "tflite"
            return True
        except Exception as e:
            logger.error(f"[inference] TFLite allocate_tensors failed: {e}")
            return False

    def _run_tflite(self, image_source) -> dict:
        try:
            input_data = preprocess(image_source)   # (1, 224, 224, 3) float32

            # Some quantised models expect uint8 — cast if needed
            input_details = self._interpreter.get_input_details()
            if input_details[0]["dtype"] == np.uint8:
                input_data = ((input_data + 1.0) * 127.5).clip(0, 255).astype(np.uint8)

            self._interpreter.set_tensor(self._input_index, input_data)
            self._interpreter.invoke()
            output = self._interpreter.get_tensor(self._output_index)[0]  # (num_classes,)

            # Apply softmax if raw logits (check if values are not already probabilities)
            if output.min() < 0 or output.max() > 1.0:
                output = _softmax(output)

            top_idx   = int(np.argmax(output))
            top_conf  = float(output[top_idx])
            raw_label = get_label(top_idx)
            return _build_result(raw_label, top_conf)

        except Exception as e:
            logger.error(f"[inference] TFLite inference error: {e}")
            return _error_result(str(e))

    # ──────────────────────────────────────────────────────────────────────────
    # PyTorch (PC development fallback)
    # ──────────────────────────────────────────────────────────────────────────

    def _try_load_pytorch(self) -> bool:
        if IS_SERVERLESS:
            logger.info("[inference] Serverless runtime detected — bypassing heavy PyTorch download")
            return False

        try:
            import torch
            from transformers import AutoImageProcessor, AutoModelForImageClassification
        except ImportError:
            logger.info("[inference] torch/transformers not available")
            return False

        try:
            logger.info(f"[inference] Loading PyTorch model {HUGGINGFACE_MODEL} (may download)...")
            self._pt_processor = AutoImageProcessor.from_pretrained(HUGGINGFACE_MODEL)
            self._pt_model     = AutoModelForImageClassification.from_pretrained(HUGGINGFACE_MODEL)
            self._pt_model.eval()

            # Sync labels from actual model config
            update_labels_from_model(self._pt_model.config.id2label)

            self._mode = "pytorch"
            return True
        except Exception as e:
            logger.warning(f"[inference] PyTorch model load failed: {e}")
            return False

    def _run_pytorch(self, image_source) -> dict:
        try:
            import torch
            from PIL import Image

            if isinstance(image_source, str):
                img = Image.open(image_source).convert("RGB")
            else:
                img = image_source.convert("RGB")

            inputs = self._pt_processor(images=img, return_tensors="pt")

            with torch.no_grad():
                outputs = self._pt_model(**inputs)

            probs    = torch.softmax(outputs.logits, dim=-1)[0]
            top_idx  = int(probs.argmax())
            top_conf = float(probs[top_idx])
            raw_label = get_label(top_idx)
            return _build_result(raw_label, top_conf)

        except Exception as e:
            logger.error(f"[inference] PyTorch inference error: {e}")
            return _error_result(str(e))

    # ──────────────────────────────────────────────────────────────────────────
    # Demo mode
    # ──────────────────────────────────────────────────────────────────────────

    def _run_demo(self) -> dict:
        """Synthetic result for UI testing when no model is available."""
        import random
        demo_labels = [
            ("Rice___Leaf_Blast", 0.91),
            ("Corn___Common_Rust", 0.76),
            ("Potato___Early_Blight", 0.63),
            ("Rice___Healthy", 0.88),
            ("Wheat___Healthy", 0.82),
        ]
        raw_label, conf = random.choice(demo_labels)
        result = _build_result(raw_label, conf)
        result["_demo"] = True
        return result


# ─── Module-level singleton ───────────────────────────────────────────────────
engine = InferenceEngine()


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x))
    return e / e.sum()


def _build_result(raw_label: str, confidence: float) -> dict:
    parsed = parse_label(raw_label)
    conf_level = classify_confidence(confidence, CONFIDENCE_HIGH, CONFIDENCE_MEDIUM)
    return {
        "crop":             parsed["crop"],
        "disease":          parsed["disease"],
        "status":           parsed["status"],
        "confidence":       round(confidence, 4),
        "confidence_level": conf_level,
        "raw_label":        raw_label,
    }


def _error_result(error_msg: str) -> dict:
    return {
        "crop":             "Unknown",
        "disease":          None,
        "status":           "error",
        "confidence":       0.0,
        "confidence_level": "low",
        "raw_label":        "error",
        "error":            error_msg,
    }
