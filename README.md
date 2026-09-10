# Kisan Mitra AI

## Smart Agriculture & Offline-First Crop Health Monitoring

> **Project Name:** Kisan Mitra AI  
> **Created by:** Circuit Maze Team  
> **Event:** Smart India Hackathon 2026 (SIH 2026)  
> **Goal:** Build an intelligent, offline-first AI crop monitoring and disease detection system with IoT environmental telemetry (Raspberry Pi & ESP32 + Firebase RTDB) using edge AI ViT models.


------------------------------------------------------------------------

## Table of Contents

1.  [Project Overview](#1-project-overview)
2.  [Project Goals](#2-project-goals)
3.  [System Architecture](#3-system-architecture)
4.  [Hardware Requirements](#4-hardware-requirements)
5.  [Target Hardware Constraint](#5-target-hardware-constraint)
6.  [AI Model](#6-ai-model)
7.  [Supported Crop/Disease Classes](#7-supported-cropdisease-classes)
8.  [Core Features](#8-core-features)
9.  [Software Stack](#9-software-stack)
10. [Repository Structure](#10-repository-structure)
11. [Development Strategy](#11-development-strategy)
12. [Phase 1 - Inspect the Model](#12-phase-1---inspect-the-model)
13. [Phase 2 - Test the Original Model on
    PC](#13-phase-2---test-the-original-model-on-pc)
14. [Phase 3 - Convert and Optimize the
    Model](#14-phase-3---convert-and-optimize-the-model)
15. [Phase 4 - Validate the Converted
    Model](#15-phase-4---validate-the-converted-model)
16. [Phase 5 - Prepare Raspberry Pi Zero
    W](#16-phase-5---prepare-raspberry-pi-zero-w)
17. [Phase 6 - Deploy the AI Model](#17-phase-6---deploy-the-ai-model)
18. [Phase 7 - Camera Integration](#18-phase-7---camera-integration)
19. [Phase 8 - SQLite Database](#19-phase-8---sqlite-database)
20. [Phase 9 - Flask Dashboard](#20-phase-9---flask-dashboard)
21. [Phase 10 - Automatic
    Monitoring](#21-phase-10---automatic-monitoring)
22. [Phase 11 - Systemd Autostart](#22-phase-11---systemd-autostart)
23. [Phase 12 - ESP32 Integration](#23-phase-12---esp32-integration)
24. [Future Irrigation AI](#24-future-irrigation-ai)
25. [Future Flood-Risk AI](#25-future-flood-risk-ai)
26. [Offline-First Design](#26-offline-first-design)
27. [AI Confidence and Safety](#27-ai-confidence-and-safety)
28. [Camera Installation Guidelines](#28-camera-installation-guidelines)
29. [Performance Optimization](#29-performance-optimization)
30. [Image Storage and Retention](#30-image-storage-and-retention)
31. [Logging and Error Handling](#31-logging-and-error-handling)
32. [API Design](#32-api-design)
33. [Testing Strategy](#33-testing-strategy)
34. [Security](#34-security)
35. [Troubleshooting](#35-troubleshooting)
36. [Deployment Checklist](#36-deployment-checklist)
37. [Future Enhancements](#37-future-enhancements)
38. [Important Limitations](#38-important-limitations)
39. [License and Model Attribution](#39-license-and-model-attribution)

------------------------------------------------------------------------

# 1. Project Overview
 
**Kisan Mitra AI** (created by **Circuit Maze Team** as part of **SIH 2026**) is an edge-AI agricultural monitoring and decision-support system designed for farms and rural agricultural communities where Internet connectivity may be weak or intermittent.


The first version focuses on:

-   Crop/leaf image capture
-   AI crop disease detection
-   Local AI inference
-   Local result storage
-   Local dashboard
-   Automatic periodic monitoring
-   Offline operation

The system is intentionally designed around the **original Raspberry Pi
Zero W**, not the more powerful Raspberry Pi Zero 2 W.

The Raspberry Pi Zero W acts as the local AI/camera gateway.

The architecture is designed so that an **ESP32** can later be added
for:

-   Soil-moisture monitoring
-   Temperature
-   Humidity
-   Rainfall
-   Water level
-   Automatic irrigation
-   Buzzer/LED alerts
-   GSM notifications

**LoRa is not used in this project.**

------------------------------------------------------------------------

# 2. Project Goals

## Primary goals

The system should:

1.  Capture crop images using a Raspberry Pi Camera.
2.  Run crop-disease inference locally.
3.  Identify the predicted crop.
4.  Identify the predicted disease or healthy class.
5.  Calculate/display model confidence.
6.  Store results in SQLite.
7.  Display results in a local web dashboard.
8.  Work without Internet.
9.  Automatically analyze crops at configurable intervals.
10. Start automatically after Raspberry Pi boot.
11. Be lightweight enough for Raspberry Pi Zero W.
12. Provide a clean software architecture for future ESP32 integration.

## Secondary goals

The architecture should eventually support:

-   Irrigation prediction
-   Flood-risk prediction
-   Environmental monitoring
-   GSM alerts
-   Remote synchronization when Internet becomes available
-   Historical crop-health analytics

------------------------------------------------------------------------

# 3. System Architecture

## Version 1 architecture

``` text
                 ┌─────────────────────────┐
                 │ Raspberry Pi Zero W     │
                 │                         │
                 │  Flask Dashboard        │
                 │  SQLite Database        │
                 │  AI Inference           │
                 │  Scheduler              │
                 └────────────┬────────────┘
                              │
                              │ CSI
                              ▼
                    ┌─────────────────┐
                    │ Raspberry Pi    │
                    │ Camera Module   │
                    └─────────────────┘
                              │
                              ▼
                       Image Capture
                              │
                              ▼
                    Image Preprocessing
                              │
                              ▼
                     Edge AI Inference
                              │
                              ▼
                  Crop Disease Prediction
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
           SQLite Database           Web Dashboard
```

## Future architecture

``` text
                       ┌─────────────────────┐
                       │ Raspberry Pi Zero W │
                       │                     │
                       │ Crop AI             │
                       │ Irrigation AI       │
                       │ Flood AI            │
                       │ Database            │
                       │ Dashboard           │
                       └──────────┬──────────┘
                                  │
                    Local Wi-Fi / Serial / HTTP
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ ESP32               │
                       │                     │
                       │ Soil Moisture       │
                       │ Temperature         │
                       │ Humidity            │
                       │ Rain Sensor         │
                       │ Water Level         │
                       │ Pump Control        │
                       │ Buzzer              │
                       │ LEDs                │
                       │ GSM Interface       │
                       └─────────────────────┘
```

------------------------------------------------------------------------

# 4. Hardware Requirements

## Required for Version 1

  Component                      Quantity Purpose
  ---------------------------- ---------- ---------------------------------
  Raspberry Pi Zero W                   1 Main edge computer
  Raspberry Pi Camera Module            1 Crop image capture
  microSD card                          1 Raspberry Pi OS and application
  5V power supply                       1 Raspberry Pi power
  Camera cable                          1 Camera-to-Pi connection
  Wi-Fi network                  Optional Local dashboard/updates

## Future hardware

  Component                                   Purpose
  ------------------------------------------- -----------------------------------------------------
  ESP32 DevKit                                Sensor/control node
  Capacitive soil-moisture sensor             Soil moisture
  DHT22                                       Temperature/humidity
  BMP280/BMP390                               Atmospheric pressure/environmental data if required
  Rain sensor/rain gauge                      Rainfall
  Water-level sensor                          Flood monitoring
  DC water pump                               Irrigation
  MOSFET module                               Pump switching
  Water tank                                  Irrigation water
  Buzzer                                      Local warning
  LEDs                                        Status indication
  GSM module                                  SMS alerts
  12V DC supply                               Pump/system power
  Buck converter                              Convert 12V to required lower voltage
  Solar panel + charge controller + battery   Future off-grid power

> **Note:** A BMP280/BMP390 measures pressure and temperature; it is not
> a humidity sensor. Use a DHT22 or another humidity-capable sensor if
> humidity is required.

------------------------------------------------------------------------

# 5. Target Hardware Constraint

## Raspberry Pi Zero W

This project targets the **original Raspberry Pi Zero W**.

Important characteristics include:

-   ARMv6 architecture
-   Single-core CPU
-   Approximately 1 GHz CPU frequency
-   512 MB RAM
-   Wi-Fi
-   Bluetooth
-   CSI camera interface

These limitations are extremely important for AI deployment.

## Do not assume this will work

``` bash
pip install torch transformers
```

followed by running a full Hugging Face PyTorch model directly on the
Pi.

That approach may be too heavy or incompatible with the original Pi Zero
W.

Instead, the intended architecture is:

``` text
Hugging Face model
       │
       ▼
Development PC
       │
       ▼
Model conversion/optimization
       │
       ▼
Lightweight edge model
       │
       ▼
ARMv6-compatible runtime
       │
       ▼
Raspberry Pi Zero W
```

The conversion must be **tested**, not assumed.

------------------------------------------------------------------------

# 6. AI Model

The project uses this exact model:

**Hugging Face repository**

``` text
LishaV01/agriculture-crop-disease-detection
```

Repository:

``` text
https://huggingface.co/LishaV01/agriculture-crop-disease-detection/tree/main
```

The model is an image-classification model based on a Vision Transformer
architecture.

The model repository contains model configuration and preprocessing
information.

The application must inspect the actual model configuration rather than
guessing:

-   Input resolution
-   Image normalization
-   Labels
-   Output shape
-   Data type
-   Model architecture
-   Processor configuration

## Model input

The model is expected to use RGB images with a model input resolution of
approximately:

``` text
224 × 224
```

However, the application should read the actual model processor
configuration and use that as the source of truth.

## Model preprocessing

Do not invent preprocessing.

The preprocessing pipeline should be derived from the model's actual
configuration, including:

-   Resize
-   RGB conversion
-   Rescaling
-   Normalization
-   Tensor conversion
-   Data type

------------------------------------------------------------------------

# 7. Supported Crop/Disease Classes

The model contains classes covering crops including:

-   Corn
-   Potato
-   Rice
-   Wheat
-   Sugarcane

The model configuration contains 20 classification labels.

Examples include:

``` text
Corn___Common_Rust
Corn___Gray_Leaf_Spot
Corn___Healthy

Potato___Early_Blight
Potato___Healthy
Potato___Late_Blight

Rice___Brown_Spot
Rice___Healthy
Rice___Leaf_Blast

Wheat___Brown_Rust
Wheat___Healthy
Wheat___Yellow_Rust

Rice_Bacterial Blight Disease
Rice_Blast Disease
Rice_brown Spot Disease
Rice_False Smut Disease

sugarcane_Bacterial Blight
sugarcane_Healthy
sugarcane_Red Rot
```

There is also an `Invalid` class in the model configuration.

> **Important:** Preserve the exact class mapping from the downloaded
> model. Do not silently rename or reorder classes.

------------------------------------------------------------------------

# 8. Core Features

## 8.1 Manual analysis

The dashboard should provide:

``` text
[ Capture & Analyze ]
```

When clicked:

``` text
Camera
   ↓
Capture image
   ↓
Preprocess
   ↓
AI inference
   ↓
Prediction
   ↓
Save result
   ↓
Display result
```

## 8.2 Automatic monitoring

The system should support configurable intervals such as:

-   15 minutes
-   30 minutes
-   60 minutes

Default:

``` text
60 minutes
```

The interval must be configurable.

## 8.3 Local dashboard

The dashboard should show:

-   System status
-   Camera status
-   AI model status
-   Latest prediction
-   Confidence
-   Crop
-   Disease
-   Image
-   Prediction history

## 8.4 Local database

All prediction results should be stored locally in SQLite.

## 8.5 Offline operation

Core AI functionality must not require Internet.

------------------------------------------------------------------------

# 9. Software Stack

## Raspberry Pi

Recommended:

-   Raspberry Pi OS
-   Python 3
-   Flask
-   SQLite
-   Picamera2 where supported
-   Lightweight edge inference runtime

## Development PC

The PC can use:

-   Python
-   PyTorch
-   Transformers
-   Pillow
-   Hugging Face Hub
-   Conversion tools required by the selected edge runtime

## Frontend

Use:

-   HTML
-   CSS
-   Vanilla JavaScript

Avoid unnecessary frontend frameworks on the Pi Zero W.

------------------------------------------------------------------------

# 10. Repository Structure

Recommended structure:

``` text
crop_assistant/
│
├── README.md
├── requirements-pc.txt
├── requirements-pi.txt
├── config.py
├── app.py
│
├── ai/
│   ├── __init__.py
│   ├── inference.py
│   ├── preprocessing.py
│   ├── labels.py
│   └── model/
│       └── crop_disease.tflite
│
├── camera/
│   ├── __init__.py
│   └── capture.py
│
├── database/
│   ├── __init__.py
│   ├── db.py
│   └── schema.sql
│
├── services/
│   ├── inference_service.py
│   ├── scheduler.py
│   └── health_service.py
│
├── api/
│   └── routes.py
│
├── templates/
│   ├── index.html
│   ├── history.html
│   ├── image.html
│   └── settings.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── captured_images/
│
├── logs/
│
├── scripts/
│   ├── test_model.py
│   ├── convert_model.py
│   └── validate_model.py
│
└── systemd/
    └── crop-assistant.service
```

The structure can be modified if a better lightweight design is
identified.

------------------------------------------------------------------------

# 11. Development Strategy

Do not build the entire application first.

Follow this sequence:

``` text
Phase 1
Model inspection
        ↓
Phase 2
Original model on PC
        ↓
Phase 3
Model conversion
        ↓
Phase 4
Converted model validation
        ↓
Phase 5
Raspberry Pi setup
        ↓
Phase 6
AI deployment
        ↓
Phase 7
Camera integration
        ↓
Phase 8
SQLite
        ↓
Phase 9
Dashboard
        ↓
Phase 10
Automatic monitoring
        ↓
Phase 11
Systemd
        ↓
Phase 12
ESP32 integration
```

This prevents the project from becoming difficult to debug.

------------------------------------------------------------------------

# 12. Phase 1 - Inspect the Model

First inspect:

``` text
https://huggingface.co/LishaV01/agriculture-crop-disease-detection/tree/main
```

Determine:

-   Model architecture
-   Base model
-   Number of parameters
-   Input dimensions
-   Labels
-   Processor configuration
-   Normalization
-   Data type
-   Model size
-   License
-   Conversion options

Important files include:

``` text
config.json
preprocessor_config.json
model.safetensors
README.md
```

The model configuration should be treated as the source of truth.

------------------------------------------------------------------------

# 13. Phase 2 - Test the Original Model on PC

The original model should first be tested on a normal development
computer.

## Create project

``` bash
mkdir crop_assistant
cd crop_assistant

python -m venv .venv
```

Activate the environment.

### Linux/macOS

``` bash
source .venv/bin/activate
```

### Windows

``` powershell
.venv\Scripts\activate
```

Install development dependencies:

``` bash
pip install torch torchvision transformers pillow huggingface_hub
```

Create:

``` text
scripts/test_model.py
```

Example baseline test:

``` python
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

MODEL_ID = "LishaV01/agriculture-crop-disease-detection"

processor = AutoImageProcessor.from_pretrained(MODEL_ID)
model = AutoModelForImageClassification.from_pretrained(MODEL_ID)

image = Image.open("leaf.jpg").convert("RGB")

inputs = processor(images=image, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

probabilities = torch.softmax(outputs.logits, dim=-1)

top_probability, top_index = probabilities[0].max(dim=0)

label = model.config.id2label[top_index.item()]

print("Prediction:", label)
print("Confidence:", float(top_probability))
```

Run:

``` bash
python scripts/test_model.py
```

Expected result:

``` text
Prediction: <model class>
Confidence: <value>
```

Do not invent expected disease results. The result depends on the
supplied image.

------------------------------------------------------------------------

# 14. Phase 3 - Convert and Optimize the Model

The original model is not the final deployment format.

The objective is to create a lightweight model that can run on the
original Raspberry Pi Zero W.

Preferred direction:

``` text
PyTorch / Hugging Face
        ↓
Conversion
        ↓
TensorFlow Lite / LiteRT
        ↓
ARMv6-compatible runtime
        ↓
Raspberry Pi Zero W
```

## Critical rule

Do not assume conversion works.

Conversion must be tested on the development PC.

Potential conversion tools may include:

-   LiteRT Torch
-   PyTorch export tools
-   ONNX as an intermediate format
-   TensorFlow Lite conversion tools

However, the final runtime must be compatible with the original Pi Zero
W.

## Important ONNX warning

ONNX may be useful as an intermediate representation, but standard ONNX
Runtime Python packages may not provide a convenient ARMv6-compatible
deployment path for the original Pi Zero W.

Therefore:

``` text
ONNX ≠ automatically suitable for Pi Zero W
```

The runtime compatibility must be verified independently.

------------------------------------------------------------------------

# 15. Phase 4 - Validate the Converted Model

This is a mandatory stage.

Use the same test images with:

``` text
Original Hugging Face model
```

and:

``` text
Converted edge model
```

Compare:

-   Predicted class
-   Confidence
-   Inference time
-   Output tensor shape
-   Output data type

Example validation table:

  Image        Original Prediction        Converted Prediction       Match
  ------------ -------------------------- -------------------------- -------
  leaf01.jpg   Rice\_\_\_Healthy          Rice\_\_\_Healthy          Yes
  leaf02.jpg   Corn\_\_\_Common_Rust      Corn\_\_\_Common_Rust      Yes
  leaf03.jpg   Potato\_\_\_Early_Blight   Potato\_\_\_Early_Blight   Yes

Small numerical differences in confidence can be acceptable.

Large prediction differences require investigation.

Do not deploy an unvalidated converted model.

------------------------------------------------------------------------

# 16. Phase 5 - Prepare Raspberry Pi Zero W

Install Raspberry Pi OS on the microSD card.

Boot the Pi and connect it to the local network.

Update packages:

``` bash
sudo apt update
sudo apt upgrade -y
```

Install common packages:

``` bash
sudo apt install -y python3 python3-pip python3-venv git sqlite3
```

Create the application directory:

``` bash
mkdir -p ~/crop_assistant
cd ~/crop_assistant
```

Create a virtual environment:

``` bash
python3 -m venv .venv
```

Activate:

``` bash
source .venv/bin/activate
```

Do not install large machine-learning frameworks simply because they
were used during PC development.

The Pi should receive the smallest practical inference runtime.

------------------------------------------------------------------------

# 17. Phase 6 - Deploy the AI Model

Copy the optimized model:

``` text
ai/model/crop_disease.tflite
```

to the Raspberry Pi.

The Pi-side inference program should:

1.  Load the model once.
2.  Keep the interpreter/model loaded.
3.  Read the image.
4.  Apply exact preprocessing.
5.  Run inference.
6.  Decode the output.
7.  Apply softmax if required by the model.
8.  Select the highest probability class.
9.  Apply confidence rules.
10. Return a standard result object.

Example result:

``` python
{
    "crop": "Rice",
    "disease": "Rice Leaf Blast",
    "status": "diseased",
    "confidence": 0.91,
    "confidence_level": "high",
    "timestamp": "2026-01-01T12:00:00",
    "model_version": "1.0",
    "inference_time_ms": 8500
}
```

The exact values must be generated by inference.

------------------------------------------------------------------------

# 18. Phase 7 - Camera Integration

The camera should capture still images rather than continuous video.

## Manual operation

``` text
Dashboard
    ↓
Capture & Analyze
    ↓
Camera captures image
    ↓
Image saved
    ↓
AI inference
    ↓
Result displayed
```

## Automatic operation

``` text
Scheduler
    ↓
Capture image
    ↓
AI inference
    ↓
Store result
    ↓
Wait
    ↓
Repeat
```

Default interval:

``` text
60 minutes
```

Configurable intervals:

``` text
15 minutes
30 minutes
60 minutes
```

------------------------------------------------------------------------

# 19. Phase 8 - SQLite Database

Use SQLite because it is lightweight and works offline.

## Prediction table

Recommended schema:

``` sql
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    image_path TEXT,
    crop TEXT,
    disease TEXT,
    status TEXT,
    confidence REAL,
    confidence_level TEXT,
    model_version TEXT,
    inference_time_ms REAL,
    image_quality TEXT,
    notes TEXT
);
```

## Optional sensor table

For future ESP32 integration:

``` sql
CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    soil_moisture REAL,
    temperature REAL,
    humidity REAL,
    rainfall REAL,
    water_level REAL
);
```

## Optional irrigation table

``` sql
CREATE TABLE IF NOT EXISTS irrigation_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    mode TEXT,
    duration_seconds INTEGER,
    reason TEXT,
    soil_moisture REAL,
    status TEXT
);
```

------------------------------------------------------------------------

# 20. Phase 9 - Flask Dashboard

The dashboard should be lightweight.

## Main dashboard

Display:

``` text
========================================
           AI CROP ASSISTANT
========================================

System:       ONLINE
Camera:       READY
AI Model:     READY

Last Analysis:
2026-XX-XX XX:XX

Crop:
Rice

Health:
Diseased

Disease:
Rice Leaf Blast

Confidence:
91%

----------------------------------------

[ CAPTURE & ANALYZE ]

----------------------------------------

Recent Analyses
```

## History page

Display:

``` text
Timestamp
Crop
Disease
Status
Confidence
Image
```

## Image detail page

Display:

-   Captured image
-   Prediction
-   Crop
-   Disease
-   Confidence
-   Timestamp
-   Model version
-   Inference time

## Settings page

Allow:

-   Automatic monitoring interval
-   Confidence thresholds
-   Image retention
-   Camera settings
-   System configuration

------------------------------------------------------------------------

# 21. Phase 10 - Automatic Monitoring

Implement a lightweight scheduler.

Example:

``` text
Every 60 minutes:

1. Check camera.
2. Capture image.
3. Validate image.
4. Run inference.
5. Save result.
6. Update dashboard.
7. Log operation.
```

Do not create a new Python process for every prediction unless
necessary.

Prefer a long-running lightweight service with proper error handling.

------------------------------------------------------------------------

# 22. Phase 11 - Systemd Autostart

Create:

``` text
systemd/crop-assistant.service
```

Example structure:

``` ini
[Unit]
Description=AI Crop Assistant
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/crop_assistant
ExecStart=/home/pi/crop_assistant/.venv/bin/python /home/pi/crop_assistant/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

The exact username and paths must be adapted to the actual Pi
installation.

Install:

``` bash
sudo cp systemd/crop-assistant.service /etc/systemd/system/
```

Reload:

``` bash
sudo systemctl daemon-reload
```

Enable:

``` bash
sudo systemctl enable crop-assistant
```

Start:

``` bash
sudo systemctl start crop-assistant
```

Check:

``` bash
sudo systemctl status crop-assistant
```

Logs:

``` bash
journalctl -u crop-assistant -f
```

------------------------------------------------------------------------

# 23. Phase 12 - ESP32 Integration

The ESP32 will become the sensor and actuator controller.

## ESP32 responsibilities

The ESP32 should handle:

-   Soil moisture
-   Temperature
-   Humidity
-   Rainfall
-   Water level
-   Pump
-   Buzzer
-   LEDs
-   GSM

The Pi should handle:

-   Crop disease AI
-   Irrigation AI
-   Flood AI
-   Database
-   Dashboard
-   Data analysis

## Communication

Possible options:

``` text
ESP32 ↔ Wi-Fi ↔ Raspberry Pi
```

or:

``` text
ESP32 ↔ Serial ↔ Raspberry Pi
```

For a local prototype, HTTP over the local Wi-Fi network is a practical
option.

------------------------------------------------------------------------

# 24. Future Irrigation AI

The irrigation system should eventually use:

### Inputs

``` text
soil moisture
temperature
humidity
rainfall
light
crop type
historical irrigation
```

### Output

``` text
irrigation_required
confidence
recommended_duration
```

Example:

``` json
{
  "irrigation_required": true,
  "confidence": 0.88,
  "recommended_duration_minutes": 8
}
```

The ESP32 should still have basic safety rules.

AI should not be the only protection against:

-   Dry-run pump operation
-   Empty water tank
-   Excessive irrigation
-   Sensor failure
-   Abnormal readings

------------------------------------------------------------------------

# 25. Future Flood-Risk AI

Flood prediction can use:

``` text
rainfall
water level
water-level rise rate
soil moisture
recent rainfall
```

The **rate of water-level rise** is particularly useful because a
rapidly increasing water level can indicate a developing flooding
condition even before the absolute level becomes extreme.

## Output

``` text
flood_probability
risk_category
```

Risk categories:

``` text
LOW
MEDIUM
HIGH
CRITICAL
```

Example:

``` json
{
  "flood_probability": 0.82,
  "risk_category": "HIGH"
}
```

This system should be treated as **decision support**, not as an
official emergency-warning system.

------------------------------------------------------------------------

# 26. Offline-First Design

The system must continue functioning without Internet.

## Functions that must work offline

-   Camera
-   Disease AI
-   SQLite
-   Dashboard
-   Historical records
-   Automatic monitoring
-   Basic irrigation/flood logic

## Functions that may require Internet later

-   Cloud synchronization
-   Remote dashboard
-   Software updates
-   Remote backups
-   Model updates

The application should detect connectivity but must not depend on it for
local AI inference.

Dashboard example:

``` text
Internet: OFFLINE
Local AI: READY
Camera: READY
Database: READY
```

The system should continue normally.

------------------------------------------------------------------------

# 27. AI Confidence and Safety

The model output must not be presented as guaranteed agricultural
diagnosis.

Recommended thresholds:

``` text
>= 0.80
High confidence

0.60 - 0.79
Medium confidence

< 0.60
Low confidence
```

These thresholds must be configurable.

## High confidence

``` text
AI Prediction:
Rice Leaf Blast

Confidence:
91%

Status:
Diseased
```

## Medium confidence

``` text
AI Prediction:
Rice Leaf Blast

Confidence:
68%

Status:
Possible disease

Recommendation:
Inspect the crop manually.
```

## Low confidence

``` text
AI Prediction:
Uncertain

Confidence:
42%

Recommendation:
Capture another image or inspect manually.
```

The system must never imply that an AI prediction is a confirmed
diagnosis.

------------------------------------------------------------------------

# 28. Camera Installation Guidelines

AI performance depends heavily on image quality.

The camera should be installed so that:

-   Leaf is visible
-   Leaf is centered
-   Lighting is sufficient
-   Camera position is stable
-   Camera angle is consistent
-   Background is not excessively cluttered
-   Lens is protected from water
-   Lens is kept clean

## Recommended practical setup

Use a fixed camera position.

For example:

``` text
        Camera
           │
           │
           ▼
     ┌───────────┐
     │   Leaf    │
     │           │
     └───────────┘
```

Avoid:

-   Strong shadows
-   Direct glare
-   Heavy motion
-   Wet lens
-   Extremely dark images
-   Very distant leaves

A fixed camera setup can make the model more consistent than random
handheld images.

------------------------------------------------------------------------

# 29. Performance Optimization

The Raspberry Pi Zero W is resource constrained.

## Recommended optimizations

### 1. Load model once

Do not load the AI model for every image.

Bad:

``` text
Capture
→ load model
→ inference
→ unload
```

Better:

``` text
Start application
→ load model once
→ capture
→ inference
→ capture
→ inference
```

### 2. Periodic inference

Do not run continuous video inference.

Use:

``` text
1 image / 15-60 minutes
```

depending on the application.

### 3. Lightweight database

Use SQLite.

### 4. Image retention

Do not store unlimited images.

### 5. Avoid unnecessary services

Run only required processes.

### 6. Measure actual performance

Record:

``` text
Preprocessing time
Inference time
Total time
RAM usage
```

Never invent benchmark values.

------------------------------------------------------------------------

# 30. Image Storage and Retention

Images can quickly consume the microSD card.

Recommended configuration:

``` text
Maximum stored images: 500
```

or:

``` text
Delete images older than X days
```

When old images are deleted:

-   Keep prediction metadata in SQLite.
-   Delete only the image file.

Example:

``` text
SQLite:
Prediction #1024
Crop: Rice
Disease: Rice Leaf Blast
Confidence: 0.91
Image: deleted due to retention policy
```

The system should periodically clean old images.

------------------------------------------------------------------------

# 31. Logging and Error Handling

Log important events.

Examples:

``` text
Application started
Camera initialized
AI model loaded
Image captured
Inference started
Inference completed
Database record saved
Scheduler started
Camera error
Model error
Database error
Insufficient storage
```

Use rotating logs where possible.

Do not generate enormous log files.

## Error examples

### Camera unavailable

``` text
Camera: ERROR
Reason: Camera initialization failed
```

The dashboard should still load.

### AI failure

``` text
AI Model: ERROR
Last successful inference: ...
```

### Low storage

``` text
Storage warning:
Less than 10% free space.
```

------------------------------------------------------------------------

# 32. API Design

Prepare the application for ESP32 integration.

## System status

``` http
GET /api/status
```

Example:

``` json
{
  "system": "online",
  "camera": "ready",
  "ai_model": "ready",
  "database": "ready",
  "internet": false
}
```

## Latest prediction

``` http
GET /api/latest
```

Example:

``` json
{
  "crop": "Rice",
  "disease": "Rice Leaf Blast",
  "status": "diseased",
  "confidence": 0.91
}
```

## Prediction history

``` http
GET /api/predictions
```

## Sensor upload

Future:

``` http
POST /api/sensors
```

Example:

``` json
{
  "soil_moisture": 42.5,
  "temperature": 29.2,
  "humidity": 71.4,
  "rainfall": 2.3,
  "water_level": 18.5
}
```

## Irrigation control

Future:

``` http
POST /api/irrigation
```

The final API should include validation and safe error handling.

------------------------------------------------------------------------

# 33. Testing Strategy

Testing should occur at multiple levels.

## Unit tests

Test:

-   Image preprocessing
-   Label mapping
-   Confidence classification
-   Database insertion
-   Database retrieval
-   API responses
-   Image-quality checks

## AI test

Test:

``` text
image
→ preprocessing
→ inference
→ prediction
```

## Camera test

Test:

``` text
camera
→ image
→ save
```

## End-to-end test

Test:

``` text
Camera
 ↓
Image
 ↓
Preprocessing
 ↓
AI
 ↓
Prediction
 ↓
SQLite
 ↓
Dashboard
```

## Reboot test

After reboot:

``` text
Pi boots
 ↓
Systemd starts service
 ↓
Flask starts
 ↓
AI model loads
 ↓
Camera becomes ready
 ↓
Scheduler starts
```

------------------------------------------------------------------------

# 34. Security

The first version is intended for a local agricultural network.

Recommendations:

-   Do not expose Flask directly to the public Internet.
-   Do not store API keys in source code.
-   Do not transmit crop images externally by default.
-   Use a non-root service account where practical.
-   Restrict unnecessary network ports.
-   Validate API input.
-   Keep the Raspberry Pi OS updated.
-   Change default credentials.

If remote access is required later, use an appropriate secure
architecture rather than exposing the development Flask server directly.

------------------------------------------------------------------------

# 35. Troubleshooting

## Problem: Camera not detected

Check:

``` bash
libcamera-hello
```

or the appropriate camera diagnostic command for the installed Raspberry
Pi OS.

Check:

-   Camera cable
-   CSI connector
-   Camera support
-   OS version
-   Camera permissions

## Problem: AI model too slow

Measure actual inference time first.

Then investigate:

-   Model optimization
-   Quantization
-   Runtime configuration
-   Input processing
-   Image resolution
-   Unnecessary background processes

Do not immediately assume a different model is required.

## Problem: Model conversion fails

Document:

1.  Conversion tool
2.  Error message
3.  Unsupported operation
4.  Model architecture
5.  Runtime requirements

Then investigate another supported conversion path.

Do not claim successful deployment without running the converted model.

## Problem: Predictions change after conversion

Run the same image set through both models.

Compare:

``` text
Class
Confidence
Logits if available
```

Investigate preprocessing first.

A preprocessing mismatch can produce apparently incorrect conversion
results.

## Problem: Raspberry Pi runs out of RAM

Check:

``` bash
free -h
```

Also inspect:

``` bash
top
```

or:

``` bash
htop
```

Reduce:

-   Background services
-   Image resolution
-   Number of loaded models
-   Large buffers
-   Unnecessary processes

------------------------------------------------------------------------

# 36. Deployment Checklist

## Hardware

-   [ ] Raspberry Pi Zero W
-   [ ] Camera connected
-   [ ] microSD installed
-   [ ] Stable power supply
-   [ ] Camera physically secured

## Raspberry Pi

-   [ ] Raspberry Pi OS installed
-   [ ] Python installed
-   [ ] Virtual environment created
-   [ ] Camera tested
-   [ ] SQLite working
-   [ ] Flask working

## AI

-   [ ] Hugging Face model inspected
-   [ ] Original model tested on PC
-   [ ] Edge conversion completed
-   [ ] Converted model tested on PC
-   [ ] Predictions compared
-   [ ] Model deployed to Pi
-   [ ] Pi inference tested
-   [ ] Inference time measured

## Application

-   [ ] Camera capture works
-   [ ] AI inference works
-   [ ] SQLite stores predictions
-   [ ] Dashboard works
-   [ ] Manual analysis works
-   [ ] Automatic scheduler works
-   [ ] Image retention works
-   [ ] Logging works
-   [ ] Error handling works

## System

-   [ ] Systemd service installed
-   [ ] Service starts automatically
-   [ ] Reboot tested
-   [ ] Offline mode tested
-   [ ] Low-storage behavior tested

## Future

-   [ ] ESP32 communication API ready
-   [ ] Sensor database ready
-   [ ] Irrigation AI architecture ready
-   [ ] Flood AI architecture ready
-   [ ] GSM integration planned

------------------------------------------------------------------------

# 37. Future Enhancements

Possible future features:

## Crop health trends

Show:

``` text
Healthy %
Diseased %
Uncertain %
```

over time.

## Multiple cameras

Support:

``` text
Camera 1 → Field A
Camera 2 → Field B
Camera 3 → Field C
```

## Crop-specific monitoring

Store:

``` text
Field
Crop
Plant/Zone
Camera
```

with each prediction.

## Sensor fusion

Combine:

``` text
Image AI
+
Soil moisture
+
Temperature
+
Humidity
+
Rainfall
```

to improve crop-health decision support.

## Irrigation automation

Eventually:

``` text
Soil moisture
+
Rain forecast/data
+
Crop stage
+
Temperature
+
AI
        ↓
Irrigation decision
        ↓
ESP32
        ↓
Pump
```

## Flood monitoring

Eventually:

``` text
Rainfall
+
Water level
+
Water-level rise rate
+
Soil moisture
        ↓
Flood-risk AI
        ↓
Risk level
        ↓
Buzzer / GSM
```

## GSM alerts

When Internet is unavailable:

``` text
AI / Sensor event
       ↓
ESP32 / GSM
       ↓
SMS
```

Example:

``` text
ALERT:
High flood risk detected.
Water level rising rapidly.
Please inspect the field.
```

Such alerts should clearly be presented as system alerts/decision
support rather than official emergency warnings.

------------------------------------------------------------------------

# 38. Important Limitations

## 38.1 AI accuracy

The supplied model may not perform equally well on every real-world
field image.

Performance can change because of:

-   Lighting
-   Camera quality
-   Background
-   Crop variety
-   Leaf age
-   Disease stage
-   Image angle
-   Unseen field conditions

The model documentation itself warns that predictions may be inaccurate
for low-quality or unseen crop images.

## 38.2 Raspberry Pi Zero W performance

The original Pi Zero W is significantly more resource constrained than
modern Raspberry Pi hardware.

Inference may take several seconds or longer depending on the optimized
model and runtime.

The exact performance must be measured on the target device.

## 38.3 Model conversion

A successful conversion cannot be assumed.

Every conversion must be tested against the original model.

## 38.4 Camera placement

A poor camera installation can reduce AI accuracy even when the model
itself is working correctly.

## 38.5 Agricultural diagnosis

This system is an AI decision-support tool.

It should not replace:

-   Agronomists
-   Agricultural extension officers
-   Laboratory diagnosis
-   Professional crop inspection

------------------------------------------------------------------------

# 39. License and Model Attribution

The AI model repository should be checked before redistribution or
commercial deployment.

Model:

``` text
LishaV01/agriculture-crop-disease-detection
```

Repository:

``` text
https://huggingface.co/LishaV01/agriculture-crop-disease-detection/tree/main
```

The model is listed under an Apache-2.0 license in its repository.

Keep appropriate attribution and license information with the deployed
project.

------------------------------------------------------------------------

# Final Architecture Summary

The completed first version should look like this:

``` text
                   ┌───────────────────────┐
                   │ Raspberry Pi Camera   │
                   └───────────┬───────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Image Capture       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Image Quality Check  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Preprocessing        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Edge AI Model       │
                    │                     │
                    │ Crop Disease        │
                    │ Classification      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Confidence Handling │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ SQLite Database  │        │ Flask Dashboard  │
       └──────────────────┘        └──────────────────┘


                     FUTURE EXTENSION

                         ESP32
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
  Soil Moisture       Environment       Water Level
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                    Raspberry Pi
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
         Crop AI     Irrigation AI    Flood AI
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    Decision Support
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
                Pump          Buzzer/GSM
```

------------------------------------------------------------------------

## Definition of Done

The project is considered successfully deployed when the following
workflow works entirely on the **original Raspberry Pi Zero W**:

``` text
Pi boots
   ↓
Application starts automatically
   ↓
Camera initializes
   ↓
Optimized disease model loads
   ↓
Camera captures leaf image
   ↓
Image is preprocessed locally
   ↓
AI runs locally
   ↓
Crop + disease + confidence generated
   ↓
Result saved to SQLite
   ↓
Dashboard displays result
   ↓
System continues operating without Internet
   ↓
Next scheduled analysis runs automatically
```

The core system must not depend on cloud inference, continuous Internet
access, LoRa, or a Raspberry Pi Zero 2 W.

**Recommended implementation order:**

``` text
1. Model inspection
2. PC inference
3. Edge conversion
4. Converted-model validation
5. Pi runtime
6. Camera
7. SQLite
8. Flask
9. Scheduler
10. Systemd
11. ESP32
12. Irrigation AI
13. Flood AI
14. GSM alerts
```

This order keeps the most technically risky part --- running the
selected Hugging Face model on the original Raspberry Pi Zero W ---
validated before the rest of the system is built around it.
