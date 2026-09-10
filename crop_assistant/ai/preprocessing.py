"""
ai/preprocessing.py — Image preprocessing pipeline.

Derived from LishaV01/agriculture-crop-disease-detection preprocessor_config.json:
  - image_processor_type: ViTImageProcessor
  - size: {"height": 224, "width": 224}
  - do_resize: true
  - do_rescale: true  (rescale_factor: 1/255)
  - do_normalize: true  (mean: [0.5,0.5,0.5], std: [0.5,0.5,0.5])
  - image_mean: [0.5, 0.5, 0.5]
  - image_std:  [0.5, 0.5, 0.5]

No internet required — all preprocessing is local using Pillow + numpy.
"""

import numpy as np
from PIL import Image


# ─── Preprocessing constants (from preprocessor_config.json) ─────────────────
INPUT_SIZE     = 224
RESCALE_FACTOR = 1.0 / 255.0
MEAN           = np.array([0.5, 0.5, 0.5], dtype=np.float32)
STD            = np.array([0.5, 0.5, 0.5], dtype=np.float32)


def load_image(source) -> Image.Image:
    """
    Load an image from a file path or accept an already-open PIL Image.

    Args:
        source: str (file path) or PIL.Image.Image

    Returns:
        PIL.Image.Image in RGB mode
    """
    if isinstance(source, Image.Image):
        img = source
    else:
        img = Image.open(source)
    return img.convert("RGB")


def preprocess(source, input_size: int = INPUT_SIZE) -> np.ndarray:
    """
    Full preprocessing pipeline matching the ViT model's preprocessor_config.json.

    Steps:
        1. Load image (file path or PIL Image)
        2. Convert to RGB
        3. Resize to input_size × input_size (BICUBIC, matching ViT standard)
        4. Convert to float32 numpy array
        5. Rescale: pixel values ÷ 255  →  [0.0, 1.0]
        6. Normalize: (value − mean) ÷ std  →  approx [−1.0, 1.0]
        7. Add batch dimension: (1, H, W, C)  for TFLite (NHWC)

    Args:
        source:     str file path or PIL.Image.Image
        input_size: target square size in pixels (default 224)

    Returns:
        numpy.ndarray of shape (1, input_size, input_size, 3), dtype=float32
    """
    img = load_image(source)

    # 3. Resize
    img = img.resize((input_size, input_size), Image.BICUBIC)

    # 4. To numpy float32
    arr = np.array(img, dtype=np.float32)   # (H, W, 3)

    # 5. Rescale  [0, 255] → [0.0, 1.0]
    arr = arr * RESCALE_FACTOR

    # 6. Normalize  [0,1] → ~[−1, 1]  using mean=0.5, std=0.5
    arr = (arr - MEAN) / STD

    # 7. Add batch dimension  (H, W, C) → (1, H, W, C)
    arr = np.expand_dims(arr, axis=0)

    return arr


def preprocess_for_pytorch(source, input_size: int = INPUT_SIZE):
    """
    Preprocessing for the original HuggingFace PyTorch model on PC.
    Returns a torch.Tensor of shape (1, 3, H, W) — CHW format.

    Only used on PC (scripts/test_model.py). Not required on Pi.
    """
    try:
        import torch
    except ImportError:
        raise ImportError("torch is required for PyTorch preprocessing (PC only).")

    arr = preprocess(source, input_size)      # (1, H, W, C)
    arr = arr[0]                              # (H, W, C)
    arr = np.transpose(arr, (2, 0, 1))        # (C, H, W)
    tensor = torch.from_numpy(arr).unsqueeze(0)  # (1, C, H, W)
    return tensor
