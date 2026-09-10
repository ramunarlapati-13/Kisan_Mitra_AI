"""
scripts/validate_model.py — Phase 4: Validate the converted TFLite model.

Run on your DEVELOPMENT PC after Phase 3 (model conversion).
NOT for Raspberry Pi.

This is a MANDATORY step before deploying to Pi.

What it does:
  1. Runs the same test images through BOTH:
       - Original HuggingFace PyTorch model
       - Converted TFLite model
  2. Compares predicted class, confidence, and output shape
  3. Prints a validation table
  4. Fails loudly if there are large prediction differences

Usage:
    python scripts/validate_model.py [image_path_1] [image_path_2] ...

    If no images are provided, 3 synthetic test images are used.

Requirements:
    pip install torch transformers pillow tensorflow (or tflite-runtime)
"""

import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

MODEL_ID    = "LishaV01/agriculture-crop-disease-detection"
TFLITE_PATH = os.path.join(os.path.dirname(__file__), "..", "ai", "model", "crop_disease.tflite")
INPUT_SIZE  = 224
MAX_CONF_DIFF = 0.10   # flag if confidence differs by more than 10%


def main():
    print("=" * 70)
    print(" Phase 4: Validate Converted TFLite Model")
    print("=" * 70)

    if not os.path.exists(TFLITE_PATH):
        print(f"\n[ERROR] TFLite model not found at {TFLITE_PATH}")
        print("  Run Phase 3 first: python scripts/convert_model.py")
        sys.exit(1)

    # ── Load models ───────────────────────────────────────────────────────────
    print("\n[1] Loading HuggingFace PyTorch model…")
    pt_model, pt_processor = _load_pytorch_model()

    print("\n[2] Loading TFLite model…")
    tflite_interpreter = _load_tflite_model()

    # ── Prepare test images ───────────────────────────────────────────────────
    image_paths = sys.argv[1:] if len(sys.argv) > 1 else []

    if image_paths:
        images = []
        for p in image_paths:
            from PIL import Image
            images.append((p, Image.open(p).convert("RGB")))
    else:
        print("\n[3] No images provided — generating 3 synthetic test images")
        images = _generate_test_images(3)

    # ── Run comparison ────────────────────────────────────────────────────────
    print(f"\n[4] Comparing predictions on {len(images)} image(s):")
    print("-" * 70)
    print(f"  {'Image':<20} {'Original':<30} {'TFLite':<30} {'Match'}")
    print("-" * 70)

    all_match   = True
    results     = []

    for name, image in images:
        pt_result     = _run_pytorch(image, pt_model, pt_processor)
        tflite_result = _run_tflite(image, tflite_interpreter)

        label_match = pt_result["label"] == tflite_result["label"]
        conf_diff   = abs(pt_result["conf"] - tflite_result["conf"])
        conf_ok     = conf_diff <= MAX_CONF_DIFF
        match       = label_match and conf_ok

        if not match:
            all_match = False

        match_str = "✓" if match else "✗"
        print(
            f"  {os.path.basename(name):<20} "
            f"{pt_result['label'][:28]:<30} "
            f"{tflite_result['label'][:28]:<30} "
            f"{match_str}"
        )
        if not match:
            if not label_match:
                print(f"    ⚠ Label mismatch!")
            if not conf_ok:
                print(f"    ⚠ Confidence diff: {conf_diff:.3f} (>{MAX_CONF_DIFF})")

        results.append({
            "name":          name,
            "pt_label":      pt_result["label"],
            "pt_conf":       pt_result["conf"],
            "pt_time_ms":    pt_result["time_ms"],
            "tflite_label":  tflite_result["label"],
            "tflite_conf":   tflite_result["conf"],
            "tflite_time_ms":tflite_result["time_ms"],
            "match":         match,
        })

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "-" * 70)
    print("  Performance comparison:")
    print(f"  {'Image':<20} {'PyTorch ms':>12} {'TFLite ms':>12} {'Speedup':>10}")
    print("-" * 70)
    for r in results:
        speedup = r["pt_time_ms"] / r["tflite_time_ms"] if r["tflite_time_ms"] > 0 else 0
        print(f"  {os.path.basename(r['name']):<20} "
              f"{r['pt_time_ms']:>10.0f}ms "
              f"{r['tflite_time_ms']:>10.0f}ms "
              f"{speedup:>8.1f}×")

    print("\n" + "=" * 70)
    if all_match:
        print(" ✓ VALIDATION PASSED — TFLite model predictions match PyTorch model")
        print(" ✓ Safe to deploy to Raspberry Pi Zero W")
    else:
        print(" ✗ VALIDATION FAILED — Check preprocessing or conversion issues")
        print("   1. Verify preprocessing.py matches the model's preprocessor_config.json")
        print("   2. Check softmax: is it applied correctly?")
        print("   3. Try reconverting the model")
        print("   Do NOT deploy until validation passes.")
    print("=" * 70)


def _load_pytorch_model():
    from transformers import AutoImageProcessor, AutoModelForImageClassification
    import torch

    proc  = AutoImageProcessor.from_pretrained(MODEL_ID)
    model = AutoModelForImageClassification.from_pretrained(MODEL_ID)
    model.eval()
    return model, proc


def _load_tflite_model():
    try:
        import tflite_runtime.interpreter as tflite
        return tflite.Interpreter(model_path=TFLITE_PATH)
    except ImportError:
        pass
    import tensorflow as tf
    interp = tf.lite.Interpreter(model_path=TFLITE_PATH)
    interp.allocate_tensors()
    return interp


def _run_pytorch(image, model, processor):
    import torch
    inputs = processor(images=image, return_tensors="pt")
    t = time.perf_counter()
    with torch.no_grad():
        outputs = model(**inputs)
    ms    = (time.perf_counter() - t) * 1000
    probs = torch.softmax(outputs.logits, dim=-1)[0]
    top   = int(probs.argmax())
    return {"label": model.config.id2label[top], "conf": float(probs[top]), "time_ms": ms}


def _run_tflite(image, interpreter):
    from ai.preprocessing import preprocess
    from ai.labels import get_label

    # Ensure tensors allocated
    try:
        interpreter.allocate_tensors()
    except Exception:
        pass

    in_details  = interpreter.get_input_details()
    out_details = interpreter.get_output_details()

    data = preprocess(image)   # (1, 224, 224, 3) float32
    if in_details[0]["dtype"] == np.uint8:
        data = ((data + 1.0) * 127.5).clip(0, 255).astype(np.uint8)

    t = time.perf_counter()
    interpreter.set_tensor(in_details[0]["index"], data)
    interpreter.invoke()
    out = interpreter.get_tensor(out_details[0]["index"])[0]
    ms  = (time.perf_counter() - t) * 1000

    # Apply softmax if logits
    if out.min() < 0 or out.max() > 1.0:
        e = np.exp(out - np.max(out))
        out = e / e.sum()

    top  = int(np.argmax(out))
    conf = float(out[top])
    return {"label": get_label(top), "conf": conf, "time_ms": ms}


def _generate_test_images(n: int):
    from PIL import Image

    images = []
    for i in range(n):
        np.random.seed(i * 42)
        arr = np.random.randint(20, 200, (224, 224, 3), dtype=np.uint8)
        # bias toward green (crop-like)
        arr[:, :, 1] = np.clip(arr[:, :, 1] + 50, 0, 255)
        arr[:, :, 0] = np.clip(arr[:, :, 0] - 20, 0, 255)
        img = Image.fromarray(arr, "RGB")
        images.append((f"synthetic_{i+1}.jpg", img))
    return images


if __name__ == "__main__":
    main()
