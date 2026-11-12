"""Simulasi State Machine Provisioning Wi-Fi & Exponential Backoff (Chapter 12).

Memverifikasi:
1. Perilaku awal saat NVS kosong -> masuk state PROVISIONING (tanpa kredensial hardcoded).
2. Penyimpanan kredensial ke NVS simulasi (dengan redaksi password di log!).
3. Urutan backoff eksponensial (1s -> 2s -> 4s -> 8s -> 16s -> 32s -> 60s cap) saat AP tidak tersedia.
4. Reset backoff ke 1s ketika koneksi berhasil (CONNECTED).
"""

from __future__ import annotations

BACKOFF_MIN_MS = 1000
BACKOFF_MAX_MS = 60000


def main() -> None:
    nvs: dict[str, str] = {}
    state = "PROVISIONING" if "ssid" not in nvs else "CONNECTING"
    backoff_ms = BACKOFF_MIN_MS

    print("=== SIMULASI WI-FI PROVISIONING & BACKOFF FSM (CHAPTER 12) ===")
    print(f"[BOOT ] NVS kosong -> state={state}")

    # Simulasi perintah provisioning dari pengguna (data uji dummy, bukan password asli)
    nvs["ssid"] = "Lab-IoT-24G"
    nvs["pass"] = "dummy-test-pass"
    print(f"[PROV ] Disimpan ke NVS: ssid={nvs['ssid']}, pass=REDACTED")
    state = "CONNECTING"

    # Simulasi 7 kegagalan koneksi beruntun untuk memeriksa batas atas backoff 60s
    backoff_seq: list[int] = []
    for attempt in range(1, 8):
        print(f"[RETRY #{attempt}] state={state} -> timeout 10000 ms -> BACKOFF_WAIT {backoff_ms} ms")
        backoff_seq.append(backoff_ms)
        backoff_ms = min(backoff_ms * 2, BACKOFF_MAX_MS)

    assert backoff_seq == [1000, 2000, 4000, 8000, 16000, 32000, 60000]

    # Simulasi koneksi berhasil pada percobaan berikutnya
    state = "CONNECTED"
    backoff_ms = BACKOFF_MIN_MS
    print(f"[CONN ] state={state}, IP=192.168.10.42, RSSI=-58 dBm, backoff_reset={backoff_ms} ms")


if __name__ == "__main__":
    main()

