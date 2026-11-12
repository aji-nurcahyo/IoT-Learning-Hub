# Bukti & Output — Chapter 19: Connectivity Reliability, Time Synchronization & Offline Buffering

- **Status Verifikasi Saat Ini**: Software Simulation **Terverifikasi (`software`)**; kompilasi `.ino` (`compile`), simulasi Wokwi (`simulator`), serta uji ketahanan jaringan dan SNTP pada papan ESP32 fisik (`hardware`) belum dijalankan (**Not Tested**) pada tahap penulisan modul ini.
- **Catatan Lingkungan**: Skrip `offline_buffer_sync.py` dijalankan pada Python `3.12.10` Windows 11 secara deterministik (seed RNG tetap).

## Output Aktual `offline_buffer_sync.py`

Command:

```text
python public/content/chapter-19/src/offline_buffer_sync.py
```

Exit code: `0`

```text
=== CHAPTER 19: RELIABILITY, TIME SYNC & OFFLINE BUFFERING ===
[JITTER] attempt=3, 50 nodes without jitter -> unique_delays=1 (all at 16.0 s!)
[JITTER] attempt=3, 50 nodes full-jitter    -> unique_delays=50, min=0.40 s, max=15.99 s
[LIVE] seq=1 epoch=1762819210 -> STORED_ACK
[LIVE] seq=2 epoch=1762819220 -> STORED_ACK
[OFFLINE] pushed 6 items into capacity=4 ring -> buffered=4, dropped_oldest=2
[IDEMPOTENCY] replay seq=5 try1=STORED_ACK, retry_after_lost_ack=DUPLICATE_ACK
[DRAIN] seq=6 -> STORED_ACK
[DRAIN] seq=7 -> STORED_ACK
[DRAIN] seq=8 -> STORED_ACK
[LIVE] seq=9 -> STORED_ACK
[SUMMARY] server_stored=7, duplicates_ignored=1, ring_dropped_oldest=2
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `offline_queue_ntp`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-19/src/offline_queue_ntp
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 901794 bytes (68%) of program storage space. Maximum is 1310720 bytes.
Global variables use 48060 bytes (14%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```
