/**
 * app.js — Kisan Mitra AI Client Engine
 * Created by Circuit Maze Team as part of SIH 2026.
 * Fully offline-compatible. Zero external CDN dependencies.
 */

'use strict';

/* ─── State ───────────────────────────────────────────────────────────────── */
let _analyzeInProgress = false;
let _selectedFile      = null;
let _webcamStream      = null;
let _sensorInterval    = null;

/* ─── Toast Notifications ─────────────────────────────────────────────────── */
function showToast(message, type = 'success', duration = 3500) {
  const toast = document.getElementById('toast');
  if (!toast) return;

  toast.textContent = message;
  toast.className   = `toast ${type} show`;

  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => {
    toast.className = 'toast';
  }, duration);
}

/* ─── Environmental Telemetry & Firebase RTDB Sync ────────────────────────── */
function refreshSensors() {
  fetch('/api/sensors/live')
    .then(r => r.json())
    .then(data => {
      _updateTelemetryUI(data);
    })
    .catch(() => {
      // Ignore transient errors on local network
    });
}

function forceFirebaseSync() {
  showToast('Connecting to Firebase RTDB…', 'success', 2000);
  fetch('/api/firebase/sync', { method: 'POST' })
    .then(r => r.json())
    .then(res => {
      if (res.success && res.data) {
        _updateTelemetryUI(res.data);
        showToast('✓ Synced with Firebase RTDB live data', 'success');
      } else {
        showToast(res.message || 'Firebase RTDB returned no data', 'warning');
      }
    })
    .catch(() => showToast('Could not reach server to sync Firebase', 'error'));
}

function _handleFirebaseRTDBUpdate(fbRaw) {
  if (!fbRaw) return;

  const limits = fbRaw.limits || {
    temperature: 35,
    humidity: 30,
    gas: 2000,
    soilMoisture: 30
  };

  const temp = parseFloat(fbRaw.temperature != null ? fbRaw.temperature : 28.5);
  const hum  = parseFloat(fbRaw.humidity != null ? fbRaw.humidity : 67.0);
  const gasVal = fbRaw.gas != null ? fbRaw.gas : (fbRaw.gasRaw != null ? fbRaw.gasRaw : 850);
  const gas  = parseInt(gasVal);
  const soilMoisture = parseFloat(fbRaw.soilMoisture != null ? fbRaw.soilMoisture : 67);
  const soilRaw = parseInt(fbRaw.soilRaw != null ? fbRaw.soilRaw : Math.round(4095 - (soilMoisture / 100 * 4095)));

  let isRelayOn = false;
  if (typeof fbRaw.relay === 'string') {
    isRelayOn = ['ON', 'TRUE', 'ACTIVE', '1'].includes(fbRaw.relay.trim().toUpperCase());
  } else {
    isRelayOn = Boolean(fbRaw.relay);
  }

  let ledStr = 'OFF';
  if (typeof fbRaw.led === 'string') {
    ledStr = fbRaw.led.trim().toUpperCase();
  } else {
    ledStr = fbRaw.led ? 'ON' : 'OFF';
  }

  const tempStatus = (fbRaw.temperatureStatus || (temp >= limits.temperature ? 'HIGH' : 'NORMAL')).toUpperCase();
  const humStatus  = (fbRaw.humidityStatus  || (hum <= limits.humidity ? 'LOW' : 'NORMAL')).toUpperCase();
  const gasStatus  = (fbRaw.gasStatus       || (gas >= limits.gas ? 'HIGH' : 'NORMAL')).toUpperCase();
  const soilStatus = (fbRaw.soilStatus      || (soilMoisture < limits.soilMoisture ? 'DRY' : 'WET')).toUpperCase();

  const tempDanger = temp >= limits.temperature || ['HIGH', 'DANGER'].includes(tempStatus);
  const humDanger  = hum <= limits.humidity || ['LOW', 'DANGER'].includes(humStatus);
  const gasDanger  = gas >= limits.gas || ['HIGH', 'DANGER'].includes(gasStatus);
  const soilDry    = soilMoisture < limits.soilMoisture || soilStatus === 'DRY' || Boolean(fbRaw.soilDry);

  const overallStatus = (fbRaw.overallStatus || fbRaw.status || (tempDanger || humDanger || gasDanger ? 'DANGER' : (soilDry ? 'WARNING' : 'NORMAL'))).toUpperCase();

  const normalized = {
    temperature: temp,
    humidity: hum,
    gas: gas,
    gasRaw: gas,
    soilRaw: soilRaw,
    soilMoisture: soilMoisture,
    soilStatus: soilStatus,
    soilDry: soilDry,
    relay: isRelayOn,
    relayMode: 'auto',
    led: ledStr,
    temperatureStatus: tempStatus,
    humidityStatus: humStatus,
    gasStatus: gasStatus,
    overallStatus: overallStatus,
    status: overallStatus,
    temperatureDanger: tempDanger,
    humidityDanger: humDanger,
    gasDanger: gasDanger,
    danger: tempDanger || humDanger || gasDanger,
    limits: limits,
    timestamp: fbRaw.timestamp || new Date().toISOString(),
    source: 'firebase-rtdb'
  };

  _updateTelemetryUI(normalized);
}

function _updateTelemetryUI(data) {
  if (!data) return;

  // 1. Ambient Temperature
  const tempEl   = document.getElementById('val-temp');
  const tempMtr  = document.getElementById('meter-temp');
  const tempTag  = document.getElementById('tag-temp');
  const cardTemp = document.getElementById('card-temp');
  if (tempEl)  tempEl.textContent = data.temperature;
  if (tempMtr) tempMtr.style.setProperty('--meter-pct', Math.min(100, (data.temperature / 50) * 100) + '%');
  if (tempTag) tempTag.textContent = data.temperatureStatus || (data.temperatureDanger ? 'HIGH' : 'NORMAL');
  if (cardTemp) cardTemp.className = `card telemetry-card ${data.temperatureDanger ? 'card-danger' : ''}`;

  // 2. Relative Humidity
  const humEl   = document.getElementById('val-hum');
  const humMtr  = document.getElementById('meter-hum');
  const humTag  = document.getElementById('tag-hum');
  const cardHum = document.getElementById('card-hum');
  if (humEl)   humEl.textContent = data.humidity;
  if (humMtr)  humMtr.style.setProperty('--meter-pct', Math.min(100, data.humidity) + '%');
  if (humTag)  humTag.textContent = data.humidityStatus || (data.humidityDanger ? 'LOW' : 'NORMAL');
  if (cardHum) cardHum.className = `card telemetry-card ${data.humidityDanger ? 'card-danger' : ''}`;

  // 3. Soil Moisture
  const soilEl   = document.getElementById('val-soil');
  const soilMtr  = document.getElementById('meter-soil');
  const soilTag  = document.getElementById('tag-soil');
  const cardSoil = document.getElementById('card-soil');
  const soilRawEl= document.getElementById('val-soil-raw');
  const soilStEl = document.getElementById('tag-soil-status');
  if (soilEl)  soilEl.textContent = data.soilMoisture;
  if (soilMtr) soilMtr.style.setProperty('--meter-pct', Math.min(100, data.soilMoisture) + '%');
  if (soilTag) soilTag.textContent = data.soilStatus || (data.soilDry ? 'DRY' : 'OPTIMAL');
  if (cardSoil) cardSoil.className = `card telemetry-card ${data.soilDry ? 'card-warning' : ''}`;
  if (soilRawEl && data.soilRaw != null) soilRawEl.textContent = `(${data.soilRaw} ADC)`;
  if (soilStEl) soilStEl.textContent = data.soilStatus || (data.soilDry ? 'DRY' : 'WET');

  // 4. Gas Sensor (MQ-2)
  const gasEl   = document.getElementById('val-gas');
  const gasMtr  = document.getElementById('meter-gas');
  const gasTag  = document.getElementById('tag-gas');
  const cardGas = document.getElementById('card-gas');
  const gasVal = data.gas != null ? data.gas : data.gasRaw;
  if (gasEl)   gasEl.textContent = gasVal;
  if (gasMtr)  gasMtr.style.setProperty('--meter-pct', Math.min(100, (gasVal / 3000) * 100) + '%');
  if (gasTag)  gasTag.textContent = data.gasStatus || (data.gasDanger ? 'HIGH' : 'NORMAL');
  if (cardGas) cardGas.className = `card telemetry-card ${data.gasDanger ? 'card-danger' : ''}`;

  // 5. Smart Irrigation Relay
  const relayBadge = document.getElementById('relay-mode-badge');
  const relayInd   = document.getElementById('relay-status-indicator');
  const relaySub   = document.getElementById('irrigation-condition-sub');
  const cardRelay  = document.getElementById('card-relay');
  const quickRelay = document.getElementById('irrigation-quick-badge');
  const btnRelay   = document.getElementById('btn-relay-toggle');

  if (relayBadge) relayBadge.textContent = (data.relayMode || 'AUTO').toUpperCase() + ' MODE';
  if (relayInd) {
    relayInd.textContent = data.relay ? 'IRRIGATION ON' : 'IRRIGATION OFF';
    relayInd.className   = `relay-status-indicator ${data.relay ? 'on' : 'off'}`;
  }
  if (cardRelay) cardRelay.className = `card telemetry-card irrigation-card ${data.relay ? 'relay-active' : ''}`;
  if (quickRelay) quickRelay.className = `irrigation-quick-badge ${data.relay ? 'active' : ''}`;
  if (btnRelay) {
    btnRelay.textContent = data.relay ? 'Turn OFF Valve' : 'Manual Override: Turn ON';
    btnRelay.className   = `btn-relay-toggle ${data.relay ? 'active' : ''}`;
  }
  if (relaySub) {
    relaySub.textContent = data.relay
      ? `Soil moisture low (${data.soilMoisture}%) — Automated water pump is active.`
      : `Soil moisture is adequate (${data.soilMoisture}%) — Valve closed.`;
  }

  // 6. Hardware Actuator Alert LED
  const valLed  = document.getElementById('val-led');
  const tagLed  = document.getElementById('tag-led');
  const unitLed = document.getElementById('unit-led');
  const cardLed = document.getElementById('card-led');
  const meterLed= document.getElementById('meter-led');
  const isLedOn = data.led === 'ON' || data.led === true;
  if (valLed)  valLed.textContent = isLedOn ? 'ON' : 'OFF';
  if (tagLed)  tagLed.textContent = isLedOn ? 'ACTIVE' : 'STANDBY';
  if (unitLed) unitLed.textContent = isLedOn ? 'ALERTING' : 'NORMAL';
  if (cardLed) cardLed.className = `card telemetry-card ${isLedOn ? 'card-warning' : ''}`;
  if (meterLed) meterLed.style.setProperty('--meter-pct', isLedOn ? '100%' : '12%');

  // 7. Dynamic Safety Limits
  if (data.limits) {
    const limTemp = document.getElementById('lim-temp');
    const limHum  = document.getElementById('lim-hum');
    const limGas  = document.getElementById('lim-gas');
    const limSoil = document.getElementById('lim-soil');
    const hintTemp= document.getElementById('hint-temp');
    const hintHum = document.getElementById('hint-hum');
    const hintGas = document.getElementById('hint-gas');
    const hintSoil= document.getElementById('hint-soil');

    if (limTemp && data.limits.temperature) limTemp.textContent = data.limits.temperature;
    if (limHum  && data.limits.humidity)    limHum.textContent  = data.limits.humidity;
    if (limGas  && data.limits.gas)         limGas.textContent  = data.limits.gas;
    if (limSoil && data.limits.soilMoisture)limSoil.textContent = data.limits.soilMoisture;

    if (hintTemp && data.limits.temperature) hintTemp.textContent = data.limits.temperature;
    if (hintHum  && data.limits.humidity)    hintHum.textContent  = data.limits.humidity;
    if (hintGas  && data.limits.gas)         hintGas.textContent  = data.limits.gas;
    if (hintSoil && data.limits.soilMoisture) hintSoil.textContent = data.limits.soilMoisture;
  }

  // 8. Environmental Safety Status Banner
  const banner   = document.getElementById('env-safety-banner');
  const badge    = document.getElementById('env-status-badge');
  const navChip  = document.getElementById('nav-env-status-text');
  const iconWrap = document.getElementById('safety-icon');
  const currentStatus = (data.status || data.overallStatus || 'NORMAL').toUpperCase();

  if (banner) banner.className = `env-safety-banner env-safety-${currentStatus.toLowerCase()}`;
  if (badge)  {
    badge.textContent = currentStatus;
    badge.className   = `safety-badge badge-${currentStatus.toLowerCase()}`;
  }
  if (navChip) navChip.textContent = currentStatus;
  if (iconWrap) {
    iconWrap.textContent = currentStatus === 'DANGER' ? '🚨' : (currentStatus === 'WARNING' ? '⚠️' : '🛡️');
  }

  // 9. Source & Firebase Connection Badge
  const srcTag   = document.getElementById('telemetry-source');
  const fbPulse  = document.getElementById('fb-pulse');
  const fbStatus = document.getElementById('fb-status-val');
  const isFb = data.source && data.source.toLowerCase().includes('firebase');

  if (srcTag) {
    srcTag.textContent = `Source: ${(data.source || 'SIMULATED').toUpperCase()}`;
    srcTag.className = `telemetry-source-tag ${isFb ? 'source-firebase' : ''}`;
  }
  if (fbStatus) {
    fbStatus.textContent = isFb ? 'CONNECTED (LIVE)' : 'SYNC READY';
  }
  if (fbPulse) {
    fbPulse.className = `fb-pulse ${isFb ? 'active' : ''}`;
  }

  // Timestamp
  const envTs = document.getElementById('env-timestamp');
  if (envTs && data.timestamp) {
    envTs.textContent = 'Updated ' + (data.timestamp.length > 8 ? data.timestamp.slice(-8) : data.timestamp);
  }

  // Checklist updates
  const chkTemp = document.getElementById('chk-temp');
  const chkHum  = document.getElementById('chk-hum');
  const chkGas  = document.getElementById('chk-gas');
  const chkSoil = document.getElementById('chk-soil');

  if (chkTemp) {
    chkTemp.className   = `check-item ${data.temperatureDanger ? 'check-danger' : 'check-ok'}`;
    chkTemp.textContent = data.temperatureDanger ? `⚠️ High Temp (${data.temperature}°C)` : `✓ Temperature Normal (${data.temperature}°C)`;
  }
  if (chkHum) {
    chkHum.className   = `check-item ${data.humidityDanger ? 'check-danger' : 'check-ok'}`;
    chkHum.textContent = data.humidityDanger ? `⚠️ Low Humidity (${data.humidity}%)` : `✓ Humidity Safe (${data.humidity}%)`;
  }
  if (chkGas) {
    chkGas.className   = `check-item ${data.gasDanger ? 'check-danger' : 'check-ok'}`;
    chkGas.textContent = data.gasDanger ? `⚠️ Elevated Gas (${gasVal} ADC)` : `✓ Gas Level Safe (${gasVal} ADC)`;
  }
  if (chkSoil) {
    chkSoil.className   = `check-item ${data.soilDry ? 'check-warn' : 'check-ok'}`;
    chkSoil.textContent = data.soilDry ? `⚠️ Soil Moisture Low (${data.soilMoisture}%)` : `✓ Soil Moisture Adequate (${data.soilMoisture}%)`;
  }
  const chkLed = document.getElementById('chk-led');
  if (chkLed) {
    const isLedOn = data.led === 'ON' || data.led === true;
    chkLed.className   = `check-item ${isLedOn ? 'check-warn' : 'check-ok'}`;
    chkLed.textContent = isLedOn ? '⚠️ Alert LED Active' : '✓ Alert LED Standby';
  }
}

/* ─── Irrigation Controls ─────────────────────────────────────────────────── */
function toggleRelay() {
  const btn = document.getElementById('btn-relay-toggle');
  const isCurrentlyActive = btn && btn.classList.contains('active');
  const targetState = !isCurrentlyActive;

  // 1. Sync to Firebase RTDB directly if browser is connected
  if (window._firebaseDB) {
    try {
      window._firebaseDB.ref('agriculture/current').update({
        relay: targetState ? 'ON' : 'OFF'
      });
    } catch (e) {
      console.warn('Firebase RTDB direct relay update note:', e);
    }
  }

  // 2. Call local backend endpoint
  fetch('/api/relay', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ state: targetState, mode: 'manual' })
  })
    .then(r => r.json())
    .then(data => {
      showToast(data.message || 'Relay state updated', 'success');
      refreshSensors();
    })
    .catch(() => showToast('Failed to toggle irrigation valve', 'error'));
}

function setRelayAuto() {
  if (window._firebaseDB) {
    try {
      window._firebaseDB.ref('agriculture/current').update({
        relayMode: 'auto'
      });
    } catch (e) {
      console.warn('Firebase auto mode update note:', e);
    }
  }

  fetch('/api/relay', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ state: false, mode: 'auto' })
  })
    .then(r => r.json())
    .then(data => {
      showToast('✓ Irrigation reset to Automatic Mode', 'success');
      refreshSensors();
    })
    .catch(() => showToast('Failed to reset relay mode', 'error'));
}


/* ─── Mode Switching (Upload / Webcam / Hardware) ─────────────────────────── */
function switchAnalyzeTab(tab) {
  const tabs = ['upload', 'webcam', 'capture'];
  tabs.forEach(t => {
    const btn  = document.getElementById(`tab-btn-${t}`);
    const pane = document.getElementById(`tab-content-${t}`);
    if (btn)  btn.classList.toggle('active', t === tab);
    if (pane) pane.classList.toggle('d-none', t !== tab);
  });

  if (tab === 'webcam') {
    startWebcam();
  } else {
    stopWebcam();
  }
}

/* ─── Image Upload Handlers ───────────────────────────────────────────────── */
function handleFileSelect(event) {
  const file = event.target.files && event.target.files[0];
  if (file) _displaySelectedFile(file);
}

function _displaySelectedFile(file) {
  _selectedFile = file;

  const dropContent = document.getElementById('dropzone-content');
  const prevWrap    = document.getElementById('upload-preview-wrap');
  const prevImg     = document.getElementById('upload-preview-img');
  const fileName    = document.getElementById('upload-file-name');
  const submitBtn   = document.getElementById('btn-upload-submit');

  if (dropContent) dropContent.classList.add('d-none');
  if (prevWrap)    prevWrap.classList.remove('d-none');
  if (fileName)    fileName.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;

  if (prevImg) {
    const reader = new FileReader();
    reader.onload = e => { prevImg.src = e.target.result; };
    reader.readAsDataURL(file);
  }

  if (submitBtn) submitBtn.classList.remove('d-none');
}

function uploadAndAnalyze() {
  if (!_selectedFile) {
    showToast('Please select or drop an image first', 'warning');
    return;
  }
  _performUploadAnalysis(_selectedFile);
}

function _performUploadAnalysis(fileOrBlob) {
  if (_analyzeInProgress) {
    showToast('Analysis already in progress…', 'warning');
    return;
  }

  _analyzeInProgress = true;

  const progress = document.getElementById('analyze-progress');
  const progBar  = document.getElementById('progress-bar-fill');
  const progLbl  = document.getElementById('progress-label');

  if (progress) progress.classList.remove('d-none');

  const stages = [
    { pct: 20,  label: '📤 Uploading high-res crop photo…' },
    { pct: 45,  label: '🔍 Analyzing leaf quality & clarity…' },
    { pct: 70,  label: '🤖 ViT Model identifying pathogen…' },
    { pct: 90,  label: '📋 Generating agronomic prescription…' },
    { pct: 100, label: '✓ Diagnosis complete' },
  ];

  let stageIdx = 0;
  const stageInterval = setInterval(() => {
    if (stageIdx < stages.length) {
      const s = stages[stageIdx++];
      if (progBar) progBar.style.setProperty('--conf-w', s.pct + '%');
      if (progLbl) progLbl.textContent = s.label;
    }
  }, 600);

  const formData = new FormData();
  formData.append('image', fileOrBlob, 'leaf_capture.jpg');

  fetch('/api/upload', {
    method: 'POST',
    body: formData
  })
    .then(r => r.json())
    .then(data => {
      clearInterval(stageInterval);

      if (data.success) {
        if (progBar) progBar.style.setProperty('--conf-w', '100%');
        if (progLbl) progLbl.textContent = '✓ Analysis complete — updating dossier…';
        showToast(
          `✓ ${data.crop || 'Crop'} — ${data.disease || 'Healthy'} (${Math.round((data.confidence || 0) * 100)}%)`,
          'success',
          4000
        );
        setTimeout(() => location.reload(), 1100);
      } else {
        _analyzeError(data.error || 'Upload analysis failed');
        clearInterval(stageInterval);
      }
    })
    .catch(() => {
      clearInterval(stageInterval);
      _analyzeError('Network error — check if local server is running');
    });
}

/* ─── Live WebRTC Device Camera ───────────────────────────────────────────── */
function startWebcam() {
  const video       = document.getElementById('webcam-video');
  const placeholder = document.getElementById('webcam-placeholder');
  const controls    = document.getElementById('webcam-controls');

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    showToast('Webcam not supported on this browser', 'error');
    return;
  }

  navigator.mediaDevices.getUserMedia({
    video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
  })
    .then(stream => {
      _webcamStream = stream;
      if (video) {
        video.srcObject = stream;
        video.playsInline = true;
        video.setAttribute('playsinline', '');
        video.classList.remove('d-none');
      }
      if (placeholder) placeholder.classList.add('d-none');
      if (controls)    controls.classList.remove('d-none');
    })
    .catch(err => {
      showToast('Could not access camera: ' + err.message, 'warning');
    });
}

function stopWebcam() {
  if (_webcamStream) {
    _webcamStream.getTracks().forEach(track => track.stop());
    _webcamStream = null;
  }
  const video       = document.getElementById('webcam-video');
  const placeholder = document.getElementById('webcam-placeholder');
  const controls    = document.getElementById('webcam-controls');

  if (video)       video.classList.add('d-none');
  if (placeholder) placeholder.classList.remove('d-none');
  if (controls)    controls.classList.add('d-none');
}

function captureWebcamSnapshot() {
  const video  = document.getElementById('webcam-video');
  const canvas = document.getElementById('webcam-canvas');
  if (!video || !canvas) return;

  canvas.width  = video.videoWidth || 640;
  canvas.height = video.videoHeight || 480;

  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  canvas.toBlob(blob => {
    if (blob) {
      _performUploadAnalysis(blob);
    }
  }, 'image/jpeg', 0.92);
}

/* ─── Hardware Pi Camera Trigger ─────────────────────────────────────────── */
function triggerAnalysis() {
  if (_analyzeInProgress) {
    showToast('Analysis already in progress…', 'warning');
    return;
  }

  _analyzeInProgress = true;
  const progress = document.getElementById('analyze-progress');
  const progBar  = document.getElementById('progress-bar-fill');
  const progLbl  = document.getElementById('progress-label');

  if (progress) progress.classList.remove('d-none');

  const stages = [
    { pct: 20,  label: '📷 Capturing from Raspberry Pi camera…' },
    { pct: 50,  label: '🔄 Preprocessing tensor…' },
    { pct: 75,  label: '🤖 Running edge inference…' },
    { pct: 90,  label: '💾 Saving diagnostic record…' },
    { pct: 100, label: '✓ Complete' },
  ];

  let stageIdx = 0;
  const stageInterval = setInterval(() => {
    if (stageIdx < stages.length) {
      const s = stages[stageIdx++];
      if (progBar) progBar.style.setProperty('--conf-w', s.pct + '%');
      if (progLbl) progLbl.textContent = s.label;
    }
  }, 700);

  fetch('/api/analyze', { method: 'POST' })
    .then(r => r.json())
    .then(data => {
      clearInterval(stageInterval);
      if (data.success) {
        if (progBar) progBar.style.setProperty('--conf-w', '100%');
        if (progLbl) progLbl.textContent = '✓ Complete — updating…';
        showToast(`✓ ${data.crop || 'Crop'} — ${data.disease || 'Healthy'}`, 'success', 3500);
        setTimeout(() => location.reload(), 1100);
      } else {
        _analyzeError(data.error || 'Capture failed');
      }
    })
    .catch(() => {
      clearInterval(stageInterval);
      _analyzeError('Failed to trigger hardware capture');
    });
}

function _analyzeError(message) {
  _analyzeInProgress = false;
  const progress = document.getElementById('analyze-progress');
  const progBar  = document.getElementById('progress-bar-fill');
  if (progress) progress.classList.add('d-none');
  if (progBar)  progBar.style.setProperty('--conf-w', '0%');
  showToast(`✕ ${message}`, 'error', 5000);
}

/* ─── Drag & Drop Dropzone Setup ─────────────────────────────────────────── */
function initDropzone() {
  const dropzone = document.getElementById('upload-dropzone');
  if (!dropzone) return;

  ['dragenter', 'dragover'].forEach(name => {
    dropzone.addEventListener(name, e => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach(name => {
    dropzone.addEventListener(name, e => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove('dragover');
    });
  });

  dropzone.addEventListener('drop', e => {
    const files = e.dataTransfer && e.dataTransfer.files;
    if (files && files.length > 0) {
      _displaySelectedFile(files[0]);
    }
  });
}

/* ─── Confidence Bar Animations ──────────────────────────────────────────── */
function animateConfidenceBars() {
  document.querySelectorAll('.conf-bar-var').forEach(bar => {
    const val = parseFloat(bar.dataset.confW || '0');
    bar.style.setProperty('--conf-w', '0%');
    setTimeout(() => {
      bar.style.setProperty('--conf-w', val + '%');
    }, 100);
  });
}

/* ─── DOM Initialisation ─────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  animateConfidenceBars();
  initDropzone();
  refreshSensors();

  // Telemetry auto-refresh every 3.5 seconds
  _sensorInterval = setInterval(refreshSensors, 3500);
});
