"""
scripts/convert_model.py — Phase 3: Convert PyTorch ViT model to TFLite.

Run on your DEVELOPMENT PC only. NOT for Raspberry Pi.

Conversion path:
    HuggingFace PyTorch ViT
        ↓
    ONNX (intermediate)
        ↓
    TensorFlow SavedModel (via onnx-tf)
        ↓
    TFLite (ai/model/crop_disease.tflite)

The TFLite file is what you copy to the Raspberry Pi.

Usage:
    python scripts/convert_model.py

Requirements:
    pip install torch transformers onnx onnxruntime
    pip install onnx-tf tensorflow   (or tensorflow-cpu)

NOTE: onnx-tf can be tricky to install. Alternative paths:
  - Use optimum[exporters]: pip install optimum
    python -c "from optimum.exporters.tflite import main_export; ..."
  - Use ai2onnx + tflite converter
  - Use LiteRT Torch (experimental) for direct PyTorch → TFLite

If TFLite conversion fails, see README section "Problem: Model conversion fails".
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

MODEL_ID    = "LishaV01/agriculture-crop-disease-detection"
ONNX_PATH   = os.path.join(os.path.dirname(__file__), "..", "ai", "model", "crop_disease.onnx")
TFLITE_PATH = os.path.join(os.path.dirname(__file__), "..", "ai", "model", "crop_disease.tflite")
INPUT_SIZE  = 224


def main():
    print("=" * 60)
    print(" Phase 3: Convert Model to TFLite")
    print("=" * 60)

    os.makedirs(os.path.dirname(ONNX_PATH), exist_ok=True)

    # ── Step 1: Export to ONNX ────────────────────────────────────────────────
    print("\n[1] Exporting PyTorch model to ONNX…")
    try:
        _export_onnx()
        print(f"    ONNX saved to: {ONNX_PATH}")
        print(f"    Size: {os.path.getsize(ONNX_PATH) / 1e6:.1f} MB")
    except Exception as e:
        print(f"\n[ERROR] ONNX export failed: {e}")
        print("    Make sure torch and transformers are installed.")
        sys.exit(1)

    # ── Step 2: ONNX → TFLite ─────────────────────────────────────────────────
    print("\n[2] Converting ONNX to TFLite…")
    success = False

    # Try method A: onnx-tf
    try:
        success = _convert_onnx_to_tflite_via_onnxtf()
    except ImportError:
        print("    onnx-tf not available — trying alternative method…")
    except Exception as e:
        print(f"    onnx-tf conversion failed: {e}")

    # Try method B: optimum CLI
    if not success:
        try:
            success = _convert_via_optimum()
        except Exception as e:
            print(f"    optimum conversion failed: {e}")

    if not success:
        print("\n[PARTIAL] ONNX file created but TFLite conversion failed.")
        print("  Options:")
        print("  1. Install onnx-tf: pip install onnx-tf tensorflow")
        print("  2. Install optimum: pip install optimum[exporters]")
        print("  3. Use a Docker container with full TF+onnx-tf stack")
        print("  4. Check HuggingFace model page for pre-converted versions")
        print(f"\n  ONNX file is at: {ONNX_PATH}")
        print("  You can convert it manually using another tool.")
        return

    print(f"\n[OK] TFLite model saved to: {TFLITE_PATH}")
    print(f"     Size: {os.path.getsize(TFLITE_PATH) / 1e6:.1f} MB")
    print("\n[OK] Phase 3 complete.")
    print("     Next: scripts/validate_model.py (Phase 4)")
    print(f"\n     Copy to Pi: scp {TFLITE_PATH} pi@<pi-ip>:~/crop_assistant/ai/model/")


def _export_onnx():
    import torch
    from transformers import AutoModelForImageClassification

    print(f"    Loading {MODEL_ID}…")
    model = AutoModelForImageClassification.from_pretrained(MODEL_ID)
    model.eval()

    dummy = torch.zeros(1, 3, INPUT_SIZE, INPUT_SIZE)

    print(f"    Exporting to ONNX (opset 14)…")
    torch.onnx.export(
        model,
        dummy,
        ONNX_PATH,
        opset_version=14,
        input_names=["pixel_values"],
        output_names=["logits"],
        dynamic_axes={
            "pixel_values": {0: "batch_size"},
            "logits":       {0: "batch_size"},
        },
        do_constant_folding=True,
    )

    # Verify ONNX
    import onnx
    onnx_model = onnx.load(ONNX_PATH)
    onnx.checker.check_model(onnx_model)
    print("    ONNX model is valid.")


def _convert_onnx_to_tflite_via_onnxtf():
    """Convert ONNX → TF SavedModel → TFLite using onnx-tf."""
    import onnx
    from onnx_tf.backend import prepare
    import tensorflow as tf

    SAVED_MODEL_DIR = TFLITE_PATH.replace(".tflite", "_savedmodel")

    print("    Converting ONNX → TF SavedModel (onnx-tf)…")
    onnx_model = onnx.load(ONNX_PATH)
    tf_rep     = prepare(onnx_model)
    tf_rep.export_graph(SAVED_MODEL_DIR)

    print("    Converting SavedModel → TFLite…")
    converter = tf.lite.TFLiteConverter.from_saved_model(SAVED_MODEL_DIR)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    with open(TFLITE_PATH, "wb") as f:
        f.write(tflite_model)

    return True


def _convert_via_optimum():
    """Convert using HuggingFace Optimum exporters (alternative path)."""
    print("    Trying HuggingFace Optimum export…")
    import subprocess
    result = subprocess.run([
        sys.executable, "-m", "optimum.exporters.tflite",
        "--model", MODEL_ID,
        "--task", "image-classification",
        "--output", os.path.dirname(TFLITE_PATH),
    ], capture_output=True, text=True)

    if result.returncode == 0:
        # optimum may use a different output name — find and rename
        output_dir = os.path.dirname(TFLITE_PATH)
        for f in os.listdir(output_dir):
            if f.endswith(".tflite"):
                src = os.path.join(output_dir, f)
                if src != TFLITE_PATH:
                    os.rename(src, TFLITE_PATH)
                return True

    print(f"    optimum stderr: {result.stderr[:500]}")
    return False


if __name__ == "__main__":
    main()
