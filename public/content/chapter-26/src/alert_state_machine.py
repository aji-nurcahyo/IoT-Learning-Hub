#!/usr/bin/env python3
"""
IoT Alert State Machine & Anti-Fatigue Engine
Chapter 26 — Internet of Things Learning Hub

Mengimplementasikan siklus hidup peringatan (NORMAL -> PENDING -> FIRING -> RESOLVED),
histeresis ambang batas untuk mencegah alert flapping, serta pembatasan frekuensi notifikasi.
"""

import time
from enum import Enum
from typing import Dict, Any, List, Optional


class AlertState(str, Enum):
    NORMAL = "NORMAL"
    PENDING = "PENDING"
    FIRING = "FIRING"
    RESOLVED = "RESOLVED"


class AlertRule:
    def __init__(
        self,
        rule_name: str,
        threshold_high: float = 30.0,
        hysteresis: float = 1.0,
        pending_duration_sec: float = 10.0,
        throttle_interval_sec: float = 30.0
    ):
        self.rule_name = rule_name
        self.threshold_high = threshold_high
        self.hysteresis = hysteresis
        self.pending_duration = pending_duration_sec
        self.throttle_interval = throttle_interval_sec

        self.state = AlertState.NORMAL
        self.pending_start_time: Optional[float] = None
        self.last_notification_time: float = 0.0
        self.notifications_sent = 0
        self.history: List[str] = []

    def evaluate(self, current_val: float, now: float) -> Dict[str, Any]:
        """
        Logika state machine:
        1. NORMAL: Jika val >= threshold_high -> transisi ke PENDING (catat start_time).
        2. PENDING:
           - Jika val < threshold_high -> kembali ke NORMAL (false alarm / spike sesaat diredam).
           - Jika (now - pending_start) >= pending_duration -> transisi ke FIRING (kirim notifikasi).
        3. FIRING:
           - Jika val < (threshold_high - hysteresis) -> transisi ke RESOLVED (lalu kembali ke NORMAL).
           - Jika masih tinggi -> periksa throttling sebelum mengirim pengingat notifikasi ulang.
        """
        initial_state = self.state
        notification_dispatched = False
        message = ""

        if self.state == AlertState.NORMAL or self.state == AlertState.RESOLVED:
            if current_val >= self.threshold_high:
                self.state = AlertState.PENDING
                self.pending_start_time = now
                message = f"Nilai {current_val} C melampaui ambang batas {self.threshold_high} C. Status: PENDING (Evaluasi {self.pending_duration}s)."

        elif self.state == AlertState.PENDING:
            if current_val < self.threshold_high:
                self.state = AlertState.NORMAL
                self.pending_start_time = None
                message = f"Nilai {current_val} C kembali normal sebelum durasi tuntas. Status: NORMAL (False alarm diredam)."
            elif (now - (self.pending_start_time or now)) >= self.pending_duration:
                self.state = AlertState.FIRING
                notification_dispatched = True
                self.last_notification_time = now
                self.notifications_sent += 1
                message = f"[CRITICAL ALERT] Nilai {current_val} C bertahan > {self.pending_duration}s! Notifikasi #{self.notifications_sent} dikirim ke operator."

        elif self.state == AlertState.FIRING:
            # Ambang pelepasan histeresis
            clear_threshold = self.threshold_high - self.hysteresis
            if current_val < clear_threshold:
                self.state = AlertState.RESOLVED
                self.pending_start_time = None
                notification_dispatched = True
                self.notifications_sent += 1
                message = f"[RESOLVED] Suhu {current_val} C telah turun di bawah batas aman {clear_threshold} C. Notifikasi pemulihan dikirim."
            else:
                # Periksa apakah perlu pengingat ulang dengan pembatasan throttling
                if (now - self.last_notification_time) >= self.throttle_interval:
                    notification_dispatched = True
                    self.last_notification_time = now
                    self.notifications_sent += 1
                    message = f"[REMINDER] Peringatan masih aktif ({current_val} C). Notifikasi #{self.notifications_sent} terkirim."
                else:
                    message = f"Kondisi masih FIRING ({current_val} C), notifikasi diredam oleh throttle interval."

        status_record = f"t={now:.1f}s | Val={current_val:4.1f} C | State={self.state.value} | {message}"
        self.history.append(status_record)

        return {
            "time": now,
            "value": current_val,
            "state": self.state.value,
            "state_changed": (initial_state != self.state),
            "notification_sent": notification_dispatched,
            "message": message
        }


def main():
    print("=== IoT Alert State Machine & Anti-Fatigue Verification Suite ===")

    # Aturan: High = 30.0 C, Histeresis = 1.0 C (Clear saat < 29.0 C), Pending Duration = 5.0s, Throttle = 15.0s
    rule = AlertRule(
        rule_name="Server_Room_Overheat",
        threshold_high=30.0,
        hysteresis=1.0,
        pending_duration_sec=5.0,
        throttle_interval_sec=15.0
    )

    timeline = [
        # (detik, nilai_suhu, skenario)
        (0.0, 27.5, "Kondisi awal normal"),
        (2.0, 31.0, "Spike sesaat mulai muncul (PENDING)"),
        (4.0, 28.0, "Spike hilang cepat sebelum 5s -> harus kembali ke NORMAL tanpa alert spam!"),
        (10.0, 30.5, "Kondisi panas persisten dimulai (PENDING)"),
        (12.0, 31.2, "Masih panas dalam jendela PENDING"),
        (16.0, 31.5, "Telah melewati 5 detik PENDING -> Harus FIRING!"),
        (20.0, 31.0, "Masih panas, tapi dalam jeda throttle -> Notifikasi diredam"),
        (32.0, 30.8, "Masih panas melewati 15s throttle -> Notifikasi pengingat dikirim"),
        (35.0, 29.5, "Suhu turun ke 29.5 C, tapi di atas 29.0 C (histeresis) -> Tetap FIRING, anti-flapping!"),
        (40.0, 28.5, "Suhu turun di bawah 29.0 C -> Transisi RESOLVED!")
    ]

    for t, val, note in timeline:
        res = rule.evaluate(val, t)
        notif_flag = " [NOTIF DIKIRIM]" if res["notification_sent"] else ""
        print(f"t={t:4.1f}s | Temp: {val:4.1f} C | State: {res['state']:8s}{notif_flag}")
        print(f"         Catatan: {note}")

    print(f"\nTotal Notifikasi Terkirim Sepanjang Simulasi: {rule.notifications_sent}")
    assert rule.notifications_sent == 3, f"Harus tepat 3 notifikasi (1 firing, 1 reminder, 1 resolved), diperoleh {rule.notifications_sent}!"
    print("Verifikasi Alert State Machine & Hysteresis SUKSES.")


if __name__ == "__main__":
    main()
