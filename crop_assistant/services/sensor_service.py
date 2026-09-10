"""
services/sensor_service.py — Environmental IoT Telemetry & Irrigation Engine.

Supports:
  1. Firebase Realtime Database (RTDB): Live bidirectional synchronization
     with schema:
       agriculture/current
         ├── temperature, humidity, gas, soilRaw, soilMoisture, soilStatus
         ├── relay, led, temperatureStatus, humidityStatus, gasStatus, overallStatus
         ├── timestamp
         └── limits: temperature, humidity, gas, soilMoisture
  2. Physical ESP32 direct push via /api/sensors
  3. Seamless fallback to local realistic diurnal simulation when offline.
"""

import os
import time
import math
import json
import random
import logging
import threading
import urllib.request
from datetime import datetime, timedelta

from config import FIREBASE_ENABLED, FIREBASE_RTDB_URL
from database import db

logger = logging.getLogger(__name__)


class SensorService:
    def __init__(self):
        self._lock = threading.Lock()
        self._manual_relay_override = None   # None = auto mode; True/False = manual override
        self._last_esp32_push = None
        self._last_firebase_fetch = None

        # Default limits matching RTDB schema
        self._default_limits = {
            "temperature": 35.0,
            "humidity": 30.0,
            "gas": 2000,
            "soilMoisture": 30.0
        }

        # Current live state (seeded with schema baseline)
        self._current = {
            "temperature": 28.5,
            "humidity": 67.0,
            "gas": 850,
            "gasRaw": 850,
            "soilRaw": 1350,
            "soilMoisture": 67.0,
            "soilStatus": "WET",
            "soilDry": False,
            "relay": False,
            "relayMode": "auto",            # "auto" or "manual"
            "led": "OFF",
            "temperatureStatus": "NORMAL",
            "humidityStatus": "NORMAL",
            "gasStatus": "NORMAL",
            "overallStatus": "NORMAL",
            "temperatureDanger": False,
            "humidityDanger": False,
            "gasDanger": False,
            "danger": False,
            "status": "NORMAL",
            "warnings": [],
            "limits": dict(self._default_limits),
            "timestamp": datetime.now().isoformat(),
            "source": "firebase-rtdb" if FIREBASE_ENABLED else "simulated"
        }

        # In-memory fast ring buffer for high-frequency chart updates
        self._history = []
        self._max_history = 120

        # Background simulator / Firebase synchronization thread
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True, name="SensorServiceLoop")
        self._thread.start()

    def get_current(self) -> dict:
        """Get snapshot of current environmental parameters."""
        with self._lock:
            # If Firebase has been recently active
            if self._last_firebase_fetch and (time.time() - self._last_firebase_fetch < 15):
                self._current["source"] = "firebase-rtdb"
            elif self._last_esp32_push and (time.time() - self._last_esp32_push < 45):
                self._current["source"] = "esp32"
            elif not self._last_firebase_fetch and not self._last_esp32_push:
                self._current["source"] = "firebase-rtdb" if FIREBASE_ENABLED else "simulated"
            return dict(self._current)

    def get_history(self, hours: int = 24) -> list:
        """Get time-series history for charts."""
        with self._lock:
            if not self._history:
                self._seed_history()
            return list(self._history)

    def _fetch_firebase(self) -> dict | None:
        """Fetch current sensor state directly from Firebase Realtime Database REST API."""
        if not FIREBASE_ENABLED or not FIREBASE_RTDB_URL:
            return None

        url = f"{FIREBASE_RTDB_URL}/agriculture/current.json"
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "AI-Crop-Monitor/1.0", "Accept": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                if resp.status == 200:
                    raw_bytes = resp.read()
                    if raw_bytes:
                        data = json.loads(raw_bytes.decode("utf-8"))
                        if isinstance(data, dict):
                            return data
        except Exception as e:
            logger.debug(f"[sensor_service] Firebase RTDB fetch note: {e}")
        return None

    def _update_from_firebase(self, data: dict):
        """Update internal state and history using Firebase RTDB schema."""
        if not isinstance(data, dict):
            return

        # Extract limits
        raw_limits = data.get("limits") if isinstance(data.get("limits"), dict) else {}
        limits = {
            "temperature": float(raw_limits.get("temperature", self._default_limits["temperature"])),
            "humidity": float(raw_limits.get("humidity", self._default_limits["humidity"])),
            "gas": int(raw_limits.get("gas", self._default_limits["gas"])),
            "soilMoisture": float(raw_limits.get("soilMoisture", self._default_limits["soilMoisture"]))
        }

        # Temperature & humidity
        temp = float(data.get("temperature", self._current.get("temperature", 28.5)))
        hum = float(data.get("humidity", self._current.get("humidity", 67.0)))

        # Gas (supports schema 'gas' or legacy 'gasRaw')
        gas_val = data.get("gas")
        if gas_val is None:
            gas_val = data.get("gasRaw", 850)
        gas = int(gas_val)

        # Soil Moisture & Soil Raw
        soil_m = float(data.get("soilMoisture", 67.0))
        soil_raw = int(data.get("soilRaw", int(4095 - (soil_m / 100.0 * 4095))))

        # Soil Status
        soil_status = str(data.get("soilStatus") or ("DRY" if soil_m < limits["soilMoisture"] else "WET")).upper()
        soil_dry = (soil_m < limits["soilMoisture"]) or (soil_status == "DRY") or bool(data.get("soilDry", False))

        # Relay status: supports "ON" / "OFF" or boolean
        relay_raw = data.get("relay")
        if isinstance(relay_raw, str):
            relay_state = relay_raw.strip().upper() in ("ON", "TRUE", "ACTIVE", "1")
        elif isinstance(relay_raw, bool):
            relay_state = relay_raw
        elif isinstance(relay_raw, (int, float)):
            relay_state = bool(relay_raw)
        else:
            relay_state = False

        # LED status: "ON" / "OFF"
        led_raw = data.get("led", "OFF")
        if isinstance(led_raw, str):
            led_str = led_raw.strip().upper()
        else:
            led_str = "ON" if led_raw else "OFF"

        # Status tags
        temp_status = str(data.get("temperatureStatus") or ("HIGH" if temp >= limits["temperature"] else "NORMAL")).upper()
        hum_status = str(data.get("humidityStatus") or ("LOW" if hum <= limits["humidity"] else "NORMAL")).upper()
        gas_status = str(data.get("gasStatus") or ("HIGH" if gas >= limits["gas"] else "NORMAL")).upper()

        overall_status = str(data.get("overallStatus") or data.get("status") or "NORMAL").upper()

        temp_danger = (temp >= limits["temperature"]) or (temp_status in ("HIGH", "DANGER")) or bool(data.get("temperatureDanger", False))
        hum_danger = (hum <= limits["humidity"]) or (hum_status in ("LOW", "DANGER")) or bool(data.get("humidityDanger", False))
        gas_danger = (gas >= limits["gas"]) or (gas_status in ("HIGH", "DANGER")) or bool(data.get("gasDanger", False))
        danger = temp_danger or hum_danger or gas_danger or bool(data.get("danger", False))

        warnings = []
        if temp_danger: warnings.append(f"High Temperature (>= {limits['temperature']}°C)")
        if hum_danger:  warnings.append(f"Low Humidity (<= {limits['humidity']}%)")
        if gas_danger:  warnings.append(f"High Gas/Smoke Level (>= {limits['gas']} ADC)")
        if soil_dry:    warnings.append(f"Soil Moisture Low (< {limits['soilMoisture']}%) — Irrigation Required")

        if overall_status in ("DANGER", "WARNING", "NORMAL", "IRRIGATION"):
            status = overall_status
        elif danger:
            status = "DANGER"
        elif warnings:
            status = "WARNING"
        else:
            status = "NORMAL"

        ts = data.get("timestamp") or datetime.now().isoformat()

        with self._lock:
            # If user has a manual local override, keep that relay state unless auto
            final_relay = self._manual_relay_override if (self._manual_relay_override is not None) else relay_state
            relay_mode = "manual" if (self._manual_relay_override is not None) else "auto"

            self._current = {
                "temperature": round(temp, 2),
                "humidity": round(hum, 2),
                "gas": gas,
                "gasRaw": gas,
                "soilRaw": soil_raw,
                "soilMoisture": round(soil_m, 1),
                "soilStatus": soil_status,
                "soilDry": soil_dry,
                "relay": final_relay,
                "relayMode": relay_mode,
                "led": led_str,
                "temperatureStatus": temp_status,
                "humidityStatus": hum_status,
                "gasStatus": gas_status,
                "overallStatus": status,
                "temperatureDanger": temp_danger,
                "humidityDanger": hum_danger,
                "gasDanger": gas_danger,
                "danger": danger,
                "status": status,
                "warnings": warnings,
                "limits": limits,
                "timestamp": ts,
                "source": "firebase-rtdb"
            }

            self._history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "timestamp": ts,
                "temperature": round(temp, 1),
                "humidity": round(hum, 1),
                "gasRaw": gas,
                "soilMoisture": round(soil_m, 1),
                "relay": 1 if final_relay else 0,
                "danger": 1 if danger else 0
            })

            if len(self._history) > self._max_history:
                self._history.pop(0)

    def set_relay(self, state: bool, mode: str = "manual") -> dict:
        """Manually toggle or reset the irrigation relay, syncing to Firebase RTDB."""
        with self._lock:
            if mode == "auto":
                self._manual_relay_override = None
                self._current["relayMode"] = "auto"
                self._current["relay"] = self._current["soilDry"]
            else:
                self._manual_relay_override = state
                self._current["relayMode"] = "manual"
                self._current["relay"] = state

            current_relay = self._current["relay"]
            relay_mode = self._current["relayMode"]

        # Sync to Firebase RTDB asynchronously
        if FIREBASE_ENABLED and FIREBASE_RTDB_URL:
            def _push_relay():
                try:
                    patch_body = json.dumps({
                        "relay": "ON" if current_relay else "OFF"
                    }).encode("utf-8")
                    req = urllib.request.Request(
                        f"{FIREBASE_RTDB_URL}/agriculture/current.json",
                        data=patch_body,
                        headers={"Content-Type": "application/json"},
                        method="PATCH"
                    )
                    with urllib.request.urlopen(req, timeout=2.5) as _:
                        pass
                except Exception as ex:
                    logger.debug(f"[sensor_service] Firebase relay patch note: {ex}")

            threading.Thread(target=_push_relay, daemon=True).start()

        return {
            "relay": current_relay,
            "relayMode": relay_mode,
            "message": f"Irrigation set to {'ON' if current_relay else 'OFF'} ({relay_mode} mode)"
        }

    def ingest_esp32_data(self, payload: dict) -> dict:
        """
        Ingest live reading from physical ESP32 DevKit V1.
        Expected JSON keys: temperature, humidity, gasRaw, soilRaw (or soilMoisture)
        """
        with self._lock:
            temp = float(payload.get("temperature", self._current["temperature"]))
            hum = float(payload.get("humidity", self._current["humidity"]))
            gas = int(payload.get("gasRaw") or payload.get("gas", self._current["gasRaw"]))

            # Soil moisture conversion
            if "soilMoisture" in payload:
                soil_m = float(payload["soilMoisture"])
                soil_raw = int(payload.get("soilRaw", 2000))
            elif "soilRaw" in payload:
                soil_raw = int(payload["soilRaw"])
                soil_m = max(0.0, min(100.0, (4095.0 - soil_raw) / 4095.0 * 100.0))
            else:
                soil_m = self._current["soilMoisture"]
                soil_raw = self._current["soilRaw"]

            self._update_state(temp, hum, gas, soil_raw, soil_m, source="esp32")
            self._last_esp32_push = time.time()

            return dict(self._current)

    def _update_state(self, temp: float, hum: float, gas: int, soil_raw: int, soil_m: float, source: str = "simulated"):
        """Calculate danger thresholds and update current reading for ESP32/Simulated data."""
        limits = self._current.get("limits", self._default_limits)
        temp_danger = temp >= limits["temperature"]
        hum_danger = hum <= limits["humidity"]
        gas_danger = gas >= limits["gas"]
        soil_dry = soil_m < limits["soilMoisture"]

        danger = temp_danger or hum_danger or gas_danger

        warnings = []
        if temp_danger: warnings.append(f"High Temperature (>= {limits['temperature']}°C)")
        if hum_danger:  warnings.append(f"Low Humidity (<= {limits['humidity']}%)")
        if gas_danger:  warnings.append(f"High Gas/Smoke Level (>= {limits['gas']} ADC)")
        if soil_dry:    warnings.append(f"Soil Moisture Deficit (< {limits['soilMoisture']}%) — Irrigation Required")

        if danger:
            status = "DANGER"
        elif warnings:
            status = "WARNING"
        else:
            status = "NORMAL"

        if self._manual_relay_override is not None:
            relay = self._manual_relay_override
            relay_mode = "manual"
        else:
            relay = soil_dry
            relay_mode = "auto"

        now_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        self._current = {
            "temperature": round(temp, 1),
            "humidity": round(hum, 1),
            "gas": int(gas),
            "gasRaw": int(gas),
            "soilRaw": int(soil_raw),
            "soilMoisture": round(soil_m, 1),
            "soilStatus": "DRY" if soil_dry else "WET",
            "soilDry": soil_dry,
            "relay": relay,
            "relayMode": relay_mode,
            "led": "ON" if danger else "OFF",
            "temperatureStatus": "HIGH" if temp_danger else "NORMAL",
            "humidityStatus": "LOW" if hum_danger else "NORMAL",
            "gasStatus": "HIGH" if gas_danger else "NORMAL",
            "overallStatus": status,
            "temperatureDanger": temp_danger,
            "humidityDanger": hum_danger,
            "gasDanger": gas_danger,
            "danger": danger,
            "status": status,
            "warnings": warnings,
            "limits": limits,
            "timestamp": now_str,
            "source": source
        }

        # Append to time-series
        self._history.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "timestamp": now_str,
            "temperature": round(temp, 1),
            "humidity": round(hum, 1),
            "gasRaw": int(gas),
            "soilMoisture": round(soil_m, 1),
            "relay": 1 if relay else 0,
            "danger": 1 if danger else 0
        })

        if len(self._history) > self._max_history:
            self._history.pop(0)

    def _run_loop(self):
        """Continuous synchronization loop: checks Firebase RTDB, then ESP32, then simulation fallback."""
        self._seed_history()
        tick = 0

        while self._running:
            tick += 1

            # 1. Check Firebase RTDB first
            if FIREBASE_ENABLED:
                fb_data = self._fetch_firebase()
                if fb_data:
                    self._update_from_firebase(fb_data)
                    self._last_firebase_fetch = time.time()
                    time.sleep(2.5)
                    continue

            # 2. Check if local ESP32 is feeding data
            if self._last_esp32_push and (time.time() - self._last_esp32_push <= 30):
                time.sleep(2.5)
                continue

            # 3. Completely offline fallback simulation: gentle diurnal drift
            time.sleep(3.0)
            with self._lock:
                t_drift = math.sin(tick * 0.05) * 2.5 + random.uniform(-0.2, 0.2)
                h_drift = -math.sin(tick * 0.05) * 4.0 + random.uniform(-0.4, 0.4)
                g_drift = random.randint(-15, 15)

                current_soil = self._current["soilMoisture"]
                if self._current["relay"]:
                    current_soil = min(85.0, current_soil + 1.2)
                else:
                    current_soil = max(18.0, current_soil - 0.15)

                new_temp = max(15.0, min(42.0, 28.5 + t_drift))
                new_hum = max(20.0, min(95.0, 67.0 + h_drift))
                new_gas = max(300, min(2500, self._current.get("gasRaw", 850) + g_drift))
                soil_raw = int(4095 - (current_soil / 100.0 * 4095))

                self._update_state(new_temp, new_hum, new_gas, soil_raw, current_soil, source="simulated")

    def _seed_history(self):
        """Generate initial historical data points for instant rich charts on load."""
        now = datetime.now()
        self._history = []
        for i in range(40, 0, -1):
            t_point = now - timedelta(minutes=i * 5)
            sine = math.sin(i * 0.2)
            temp = round(28.0 + sine * 2.5 + random.uniform(-0.3, 0.3), 1)
            hum = round(67.0 - sine * 4.0 + random.uniform(-0.5, 0.5), 1)
            soil = round(55.0 + sine * 6.0 + random.uniform(-1.0, 1.0), 1)
            gas = int(820 + random.randint(-40, 50))
            relay = 1 if soil < 30.0 else 0

            self._history.append({
                "time": t_point.strftime("%H:%M"),
                "timestamp": t_point.isoformat(),
                "temperature": temp,
                "humidity": hum,
                "gasRaw": gas,
                "soilMoisture": soil,
                "relay": relay,
                "danger": 0
            })


# Global singleton instance
sensor_service = SensorService()
