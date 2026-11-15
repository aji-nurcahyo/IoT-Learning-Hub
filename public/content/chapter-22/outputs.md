# Bukti Pengujian & Hasil Eksekusi — Chapter 22

Pengujian modul gateway daemon serial-ke-MQTT dieksekusi menggunakan lingkungan runtime Python 3 pada simulator stream serial TTY lokal.

## Perintah Eksekusi

```bash
python public/content/chapter-22/src/serial_mqtt_gateway.py
```

## Hasil Keluaran Terminal (Standard Output)

```text
[GATEWAY DAEMON] Inisialisasi gateway pada /dev/ttyUSB0 @ 115200 bps...
[GATEWAY DAEMON] Status: RUNNING (Mendengarkan stream serial)
[MQTT PUBLISH] Topic: iot/gateway/rpi-gateway-lab01/ESP32-NODE-01/telemetry | Bytes: 135 | Payload: {"dev":"ESP32-NODE-01","seq":101,"temp_c":28.45,"humidity_pct":65.2,"battery_mv":3290,"ts":1794762751,"gateway_id":"rpi-gateway-lab01"}
[GATEWAY WARNING] Frame serial korup diabaikan: $DATA,ESP32-NODE-01,102,28.50,65.10,3288*FF
[MQTT PUBLISH] Topic: iot/gateway/rpi-gateway-lab01/ESP32-NODE-02/telemetry | Bytes: 136 | Payload: {"dev":"ESP32-NODE-02","seq":504,"temp_c":24.12,"humidity_pct":71.05,"battery_mv":3310,"ts":1794762751,"gateway_id":"rpi-gateway-lab01"}
[GATEWAY WARNING] Frame serial korup diabaikan: NOISE_BURST_SERIAL_LINE_GARBAGE
[MQTT PUBLISH] Topic: iot/gateway/rpi-gateway-lab01/ESP32-NODE-01/telemetry | Bytes: 135 | Payload: {"dev":"ESP32-NODE-01","seq":103,"temp_c":28.55,"humidity_pct":65.0,"battery_mv":3285,"ts":1794762751,"gateway_id":"rpi-gateway-lab01"}
[GATEWAY DAEMON] Selesai. Total sukses: 3, Korup: 2
```

## Analisis Hasil

1. **Integritas Framing & Checksum**: Dari lima frame yang diumpankan, tiga frame valid berhasil di-parse dan dipublikasikan ke topik MQTT tujuan. Satu frame dengan checksum tidak cocok (`*FF`) dan satu frame derau mentah (`NOISE_BURST...`) berhasil ditolak dan dicatat pada log peringatan.
2. **Kesesuaian Payload**: Data terbitan menyertakan metadata tambahan dari gateway (`gateway_id`, stempel waktu Unix lokal `ts`), membuktikan fungsi *data enrichment* pada gerbang edge.
3. **Ketahanan Proses**: Program menyelesaikan eksekusi tanpa melempar pengecualian tak tertangani (*unhandled exception*) ketika berhadapan dengan data biner atau teks acak.
