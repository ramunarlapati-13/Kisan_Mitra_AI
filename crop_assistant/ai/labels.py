"""
ai/labels.py — Hardcoded class labels from LishaV01/agriculture-crop-disease-detection.

Labels are sourced from the model's config.json id2label mapping.
They are embedded here so the Pi can classify without any network access.

DO NOT reorder or rename — mapping must exactly match the trained model.
"""

# ─── Full 20-class label list (index → label string) ─────────────────────────
# Source: model config.json id2label
# These are embedded offline — no Hugging Face API call needed on Pi.
LABELS = [
    "Corn___Common_Rust",
    "Corn___Gray_Leaf_Spot",
    "Corn___Healthy",
    "Invalid",
    "Potato___Early_Blight",
    "Potato___Healthy",
    "Potato___Late_Blight",
    "Rice___Brown_Spot",
    "Rice___Healthy",
    "Rice___Leaf_Blast",
    "Rice_Bacterial Blight Disease",
    "Rice_Blast Disease",
    "Rice_brown Spot Disease",
    "Rice_False Smut Disease",
    "sugarcane_Bacterial Blight",
    "sugarcane_Healthy",
    "sugarcane_Red Rot",
    "Wheat___Brown_Rust",
    "Wheat___Healthy",
    "Wheat___Yellow_Rust",
]

# NOTE: When the actual model is downloaded (scripts/test_model.py),
# run update_labels_from_model() to verify / correct the ordering.
# The above ordering is an approximation; the model's id2label is authoritative.

NUM_CLASSES = len(LABELS)


def get_label(index: int) -> str:
    """Return the label string for a given class index."""
    if 0 <= index < len(LABELS):
        return LABELS[index]
    return "Unknown"


def parse_label(label: str) -> dict:
    """
    Parse a raw label string into structured crop/disease/status.

    Examples:
        "Corn___Common_Rust"          → crop=Corn, disease=Common Rust, status=diseased
        "Rice___Healthy"              → crop=Rice, disease=None, status=healthy
        "Rice_Bacterial Blight Disease" → crop=Rice, disease=Bacterial Blight Disease, status=diseased
        "Invalid"                     → crop=Unknown, disease=None, status=invalid
        "sugarcane_Red Rot"           → crop=Sugarcane, disease=Red Rot, status=diseased
    """
    if label == "Invalid":
        return {"crop": "Unknown", "disease": None, "status": "invalid", "raw_label": label}

    # Try triple-underscore separator first (___), then single underscore
    if "___" in label:
        parts = label.split("___", 1)
        crop    = parts[0].strip()
        disease = parts[1].replace("_", " ").strip() if len(parts) > 1 else None
    elif "_" in label:
        # e.g. "Rice_Bacterial Blight Disease" or "sugarcane_Red Rot"
        parts   = label.split("_", 1)
        crop    = parts[0].strip()
        disease = parts[1].strip() if len(parts) > 1 else None
    else:
        crop    = label
        disease = None

    # Normalise crop name capitalisation
    crop = crop.capitalize() if crop.islower() else crop

    # Determine health status
    if disease and disease.lower() in ("healthy",):
        status  = "healthy"
        disease = None
    elif disease is None or disease.lower() == "healthy":
        status  = "healthy"
        disease = None
    else:
        status = "diseased"

    return {
        "crop":      crop,
        "disease":   disease,
        "status":    status,
        "raw_label": label,
    }


def classify_confidence(confidence: float, high_thresh: float = 0.80,
                         medium_thresh: float = 0.60) -> str:
    """
    Classify a confidence score into a named level.

    Returns: "high" | "medium" | "low"
    """
    if confidence >= high_thresh:
        return "high"
    elif confidence >= medium_thresh:
        return "medium"
    else:
        return "low"


def update_labels_from_model(id2label: dict) -> None:
    """
    Update the global LABELS list with the actual model's id2label mapping.
    Call this once after downloading the model on PC (not needed on Pi).
    """
    global LABELS
    new_labels = [None] * len(id2label)
    for idx, lbl in id2label.items():
        new_labels[int(idx)] = lbl
    LABELS[:] = new_labels
    print(f"[labels] Updated {len(LABELS)} labels from model config.")
    for i, lbl in enumerate(LABELS):
        print(f"  {i:2d}: {lbl}")
