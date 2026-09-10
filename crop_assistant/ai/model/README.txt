# Place your converted TFLite model file here:
#   ai/model/crop_disease.tflite
#
# Steps:
#   1. Run: python scripts/test_model.py        (Phase 2 — PC)
#   2. Run: python scripts/convert_model.py     (Phase 3 — PC)
#   3. Run: python scripts/validate_model.py    (Phase 4 — PC)
#   4. Copy crop_disease.tflite to this directory on the Pi
#
# If no .tflite file is present:
#   - On PC: the app falls back to the PyTorch/HuggingFace model (requires internet once)
#   - On Pi: the app runs in Demo mode (clearly labelled)
