"""
services/scheduler.py — Lightweight background scheduler.

Uses threading.Timer in a self-rescheduling pattern — no external dependencies.
This is intentionally minimal so it runs on Pi Zero W without extra processes.

The scheduler runs as a daemon thread.
It calls inference_service.run_analysis() at the configured interval.
"""

import logging
import threading
from datetime import datetime

from config import SCHEDULER_DEFAULT_MIN, SCHEDULER_ENABLED
from database import db

logger = logging.getLogger(__name__)


class CropScheduler:
    """Self-rescheduling lightweight scheduler."""

    def __init__(self):
        self._timer:    threading.Timer | None = None
        self._lock      = threading.Lock()
        self._running   = False
        self._interval  = SCHEDULER_DEFAULT_MIN * 60    # seconds
        self._enabled   = SCHEDULER_ENABLED
        self._run_count = 0
        self._last_run:  str | None = None
        self._next_run:  str | None = None

    # ── Public API ────────────────────────────────────────────────────────────

    def start(self):
        """Start the scheduler using the persisted interval from the database."""
        # Load interval from DB settings (may have been changed via settings page)
        saved_min = db.get_setting("scheduler_interval_min", str(SCHEDULER_DEFAULT_MIN))
        saved_en  = db.get_setting("scheduler_enabled", "true")

        self._interval = int(saved_min) * 60
        self._enabled  = saved_en.lower() == "true"

        if not self._enabled:
            logger.info("[scheduler] Scheduler is disabled.")
            return

        logger.info(
            f"[scheduler] Starting — interval={self._interval // 60} min, "
            f"first run in {self._interval // 60} min"
        )
        self._schedule_next()

    def stop(self):
        """Stop the scheduler."""
        with self._lock:
            if self._timer:
                self._timer.cancel()
                self._timer = None
        self._running = False
        logger.info("[scheduler] Stopped.")

    def update_interval(self, minutes: int):
        """Change the interval (takes effect after current timer fires)."""
        self._interval = max(1, minutes) * 60
        db.set_setting("scheduler_interval_min", str(minutes))
        logger.info(f"[scheduler] Interval updated to {minutes} min")
        # Restart timer with new interval
        self.stop()
        self._schedule_next()

    def set_enabled(self, enabled: bool):
        """Enable or disable the scheduler."""
        self._enabled = enabled
        db.set_setting("scheduler_enabled", "true" if enabled else "false")
        if enabled and not self._running:
            self._schedule_next()
        elif not enabled:
            self.stop()

    @property
    def status(self) -> dict:
        return {
            "enabled":          self._enabled,
            "interval_min":     self._interval // 60,
            "run_count":        self._run_count,
            "last_run":         self._last_run,
            "next_run":         self._next_run,
            "running":          self._running,
        }

    # ── Internal ──────────────────────────────────────────────────────────────

    def _schedule_next(self):
        from datetime import datetime, timedelta
        if not self._enabled:
            return
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(self._interval, self._fire)
            self._timer.daemon = True
            self._timer.start()
        next_dt = datetime.now().isoformat(timespec="seconds")
        # Rough next-run estimate
        from datetime import timedelta
        from datetime import datetime as dt
        self._next_run = (dt.now() + timedelta(seconds=self._interval)).isoformat(timespec="seconds")
        logger.debug(f"[scheduler] Next analysis scheduled at {self._next_run}")

    def _fire(self):
        """Called when the timer fires. Runs analysis then reschedules."""
        self._running  = True
        self._last_run = datetime.now().isoformat(timespec="seconds")
        self._run_count += 1

        logger.info(f"[scheduler] Running scheduled analysis #{self._run_count}")

        try:
            from services.inference_service import run_analysis
            result = run_analysis(triggered_by="scheduler")
            if result.get("success"):
                logger.info(
                    f"[scheduler] Analysis #{self._run_count} complete — "
                    f"{result.get('crop')} / {result.get('disease') or 'Healthy'} "
                    f"({result.get('confidence', 0):.0%})"
                )
            else:
                logger.warning(
                    f"[scheduler] Analysis #{self._run_count} failed — "
                    f"{result.get('error')}"
                )
        except Exception as e:
            logger.error(f"[scheduler] Unexpected error during analysis: {e}")

        self._running = False
        # Reschedule
        self._schedule_next()


# Module-level singleton
scheduler = CropScheduler()
