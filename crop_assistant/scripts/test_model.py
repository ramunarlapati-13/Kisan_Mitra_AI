"""
scripts/test_model.py — Phase 2: Test the original HuggingFace model on PC.

Run on your DEVELOPMENT PC only (requires internet for first download).
This script is NOT for the Raspberry Pi.

Usage:
    python scripts/test_model.py [image_path]

    If no image_path is provided, a synthetic test image is generated.

What this does:
  1. Downloads the model from HuggingFace (cached locally after first run)
  2. Prints the actual id2label mapping → use this to verify/update ai/labels.py
  3. Prints the actual preprocessor_config → use to verify ai/preprocessing.py
  4. Runs inference on the provided image
  5. Prints top-5 predictions with confidence

Requirements:
    pip install torch transformers pillow huggingface_hub
"""

import sys
import os
import time

# Allow running from scripts/ or from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

MODEL_ID = "LishaV01/agriculture-crop-disease-detection"


def main():
    print("=" * 60)
    print(" Phase 2: Test Original HuggingFace Model on PC")
    print("=" * 60)

    try:
        import torch
        from transformers import AutoImageProcessor, AutoModelForImageClassification
        from PIL import Image
    except ImportError as e:
        print(f"\n[ERROR] Missing dependency: {e}")
        print("Install with: pip install torch transformers pillow")
        sys.exit(1)

    # ── Load model ────────────────────────────────────────────────────────────
    print(f"\n[1] Loading model: {MODEL_ID}")
    print("    (downloads to ~/.cache/huggingface on first run)")

    t_load = time.perf_counter()
    processor = AutoImageProcessor.from_pretrained(MODEL_ID)
    model     = AutoModelForImageClassification.from_pretrained(MODEL_ID)
    model.eval()
    print(f"    Model loaded in {time.perf_counter() - t_load:.1f}s")

    # ── Print model config ────────────────────────────────────────────────────
    print("\n[2] Model configuration:")
    print(f"    Architecture: {type(model).__name__}")
    print(f"    Num labels:   {model.config.num_labels}")

    print("\n[3] id2label mapping (copy this to ai/labels.py if different):")
    for idx in sorted(model.config.id2label.keys()):
        print(f"    {idx:2d}: {model.config.id2label[idx]}")

    # ── Print preprocessor config ─────────────────────────────────────────────
    print("\n[4] Preprocessor configuration:")
    print(f"    Type: {type(processor).__name__}")
    if hasattr(processor, 'size'):
        print(f"    Size: {processor.size}")
    if hasattr(processor, 'image_mean'):
        print(f"    Mean: {processor.image_mean}")
    if hasattr(processor, 'image_std'):
        print(f"    Std:  {processor.image_std}")
    if hasattr(processor, 'do_rescale'):
        print(f"    Rescale: {processor.do_rescale}")
    if hasattr(processor, 'rescale_factor'):
        print(f"    Rescale factor: {processor.rescale_factor}")

    # ── Prepare image ─────────────────────────────────────────────────────────
    image_path = sys.argv[1] if len(sys.argv) > 1 else None

    if image_path:
        print(f"\n[5] Loading image: {image_path}")
        image = Image.open(image_path).convert("RGB")
    else:
        print("\n[5] No image provided — generating synthetic test image")
        import numpy as np
        arr   = np.random.randint(30, 150, (224, 224, 3), dtype=np.uint8)
        arr[:, :, 1] = np.random.randint(80, 200, (224, 224), dtype=np.uint8)   # more green
        image = Image.fromarray(arr)
        print("    (Synthetic image — results will not be meaningful)")

    print(f"    Image size: {image.size}, mode: {image.mode}")

    # ── Run inference ─────────────────────────────────────────────────────────
    print("\n[6] Running inference…")
    inputs = processor(images=image, return_tensors="pt")

    t_inf = time.perf_counter()
    with torch.no_grad():
        outputs = model(**inputs)
    inf_ms = (time.perf_counter() - t_inf) * 1000

    probabilities  = torch.softmax(outputs.logits, dim=-1)[0]
    top5_probs, top5_idx = probabilities.topk(5)

    print(f"\n[7] Results (inference time: {inf_ms:.0f} ms):")
    print("-" * 50)
    for i, (prob, idx) in enumerate(zip(top5_probs, top5_idx)):
        label = model.config.id2label[idx.item()]
        bar   = "█" * int(prob.item() * 30)
        print(f"  #{i+1}: {label:<35} {prob.item():.4f}  {bar}")

    top_label = model.config.id2label[top5_idx[0].item()]
    top_conf  = float(top5_probs[0])

    print("\n" + "=" * 60)
    print(f" PREDICTION:  {top_label}")
    print(f" CONFIDENCE:  {top_conf:.2%}")
    print("=" * 60)
    print("\n[OK] Phase 2 complete.")
    print("     Next: scripts/convert_model.py (Phase 3)")


if __name__ == "__main__":
    main()
