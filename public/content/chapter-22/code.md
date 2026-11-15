# Panduan Implementasi Kode — Chapter 22

Dokumentasi ini menjelaskan implementasi teknis gateway pada [`serial_mqtt_gateway.py`](content/chapter-22/src/serial_mqtt_gateway.py) dan konfigurasi supervisor pada [`iot-gateway.service`](content/chapter-22/src/iot-gateway.service).

## Struktur Program

1. **Kelas `MockSerialPort`**:
   Menyediakan abstraksi aliran byte serial tiruan agar pengujian unit dan otomatisasi dapat berjalan deterministik pada sistem pengujian continuous integration (CI) tanpa membutuhkan modul hardware fisik.
2. **Fungsi `calculate_lrc_checksum`**:
   Mengimplementasikan algoritma Longitudinal Redundancy Check (LRC) 8-bit hex standar industri:
   ```python
   def calculate_lrc_checksum(data_str: str) -> str:
       lrc = 0
       for ch in data_str.encode('ascii'):
           lrc = (lrc + ch) & 0xFF
       return f"{((lrc ^ 0xFF) + 1) & 0xFF:02X}"
   ```
3. **Kelas `SerialMqttGateway`**:
   - `parse_serial_frame`: Memvalidasi keberadaan start delimiter `$DATA,`, pemisah token koma, dan karakter asteris `*`, kemudian mengomparasi nilai checksum yang diterima dengan hasil kalkulasi lokal.
   - `publish_to_mqtt`: Mengonversi struktur data dictionary ke string JSON kompak dan mempublikasikannya ke hierarki topik `iot/gateway/{gateway_id}/{dev}/telemetry`.
   - `_handle_signal`: Mengubah flag `self.running = False` secara aman ketika sistem operasi mengirimkan sinyal `SIGINT` atau `SIGTERM`.

## Konfigurasi systemd

File unit [`iot-gateway.service`](content/chapter-22/src/iot-gateway.service) ditempatkan pada `/etc/systemd/system/` dengan perintah instalasi:

```bash
sudo cp content/chapter-22/src/iot-gateway.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable iot-gateway.service
sudo systemctl start iot-gateway.service
```

Untuk memantau log secara real-time:

```bash
journalctl -u iot-gateway.service -f
```

## Eksekusi Pengujian Lokal

```bash
python public/content/chapter-22/src/serial_mqtt_gateway.py
```
