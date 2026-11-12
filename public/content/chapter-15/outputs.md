# Bukti & Output Eksekusi — Chapter 15

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (simulasi jaminan pengiriman QoS 0/1/2, deduplikasi QoS 1, *Retained Message*, dan LWT pada Python 3.12.10)
- **Tanggal**: 2026-11-11
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-15/src/mqtt_qos_lwt_sim.py`
- **Firmware ESP32 (`mqtt_lwt_retained.ino`)**: **Belum diuji** (toolchain `esp32:esp32` masih dalam tahap instalasi; Mosquitto eksternal belum terpasang)

## 2. Output Aktual (Verbatim — Software Verification)

```text
=== SIMULASI MQTT QoS, SESSIONS, RETAINED & LWT (CHAPTER 15) ===
QoS 0: 1 paket/pesan -> PUBLISH
QoS 1: 2 paket/pesan -> PUBLISH -> PUBACK
QoS 2: 4 paket/pesan -> PUBLISH -> PUBREC -> PUBREL -> PUBCOMP

--- Uji Duplikasi QoS 1 (PUBACK hilang di jaringan) ---
  [DB INSERT ] seq=10 dup=False temp_c=29.1 C
  [DB INSERT ] seq=11 dup=False temp_c=29.3 C
  [DEDUP DROP] seq=11 dup=True sudah pernah diproses!
  [DB INSERT ] seq=12 dup=False temp_c=29.4 C

--- Uji Retained Message, Keepalive & LWT ---
1) Node konek -> retained['status'] = {"state":"online"}
2) Dashboard baru subscribe -> langsung terima retained: {"state":"online"}
3) Diam 46s (> 45s) -> Broker picu LWT: lab/gh01/node-01/status = {"state":"offline","reason":"lwt"}
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `mqtt_lwt_retained`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-15/src/mqtt_lwt_retained
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 914608 bytes (69%) of program storage space. Maximum is 1310720 bytes.
Global variables use 47280 bytes (14%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```
