# Panduan Implementasi Kode — Chapter 27

Dokumentasi ini menjelaskan arsitektur skrip [`fleet_manager.py`](content/chapter-27/src/fleet_manager.py).

## Struktur Modul

1. **Enumerasi `DeviceStatus`**:
   Mendefinisikan lima tahapan siklus hidup perangkat: `PROVISIONED`, `ONLINE`, `DEGRADED`, `OFFLINE`, dan `DECOMMISSIONED`.
2. **Kelas `DeviceRecord`**:
   - Menyimpan atribut fisik (`dev_id`, `hw_model`, `mac_addr`, `fw_version`).
   - Menyimpan pasangan *State Twin*: `desired_config` dan `reported_config`.
   - Metode `has_config_drift()` membandingkan kedua kamus konfigurasi untuk mendeteksi ketidaksinkronan status.
3. **Kelas `FleetManager`**:
   - `enroll_device`: Memvalidasi keunikan `dev_id` dan mendaftarkan perangkat ke inventaris.
   - `record_heartbeat`: Memperbarui stempel waktu `last_heartbeat` dan menetapkan status `ONLINE`. Menolak denyut dari perangkat yang berstatus `DECOMMISSIONED`.
   - `set_desired_config`: Menaikkan nomor versi konfigurasi dan memperbarui parameter yang ditargetkan operator.
   - `report_device_config`: Menerima konfirmasi dari mikrokontroler dan menyinkronkan `reported_config` dengan `desired_config`.
   - `evaluate_fleet_health`: Menelusuri seluruh armada dan mengklasifikasikan status perangkat berdasarkan batas ambang `degraded_threshold_sec` ($15\text{s}$) dan `heartbeat_timeout_sec` ($30\text{s}$).
   - `decommission_device`: Menandai perangkat sebagai pensiun dan mencabut hak transmisi data.

## Eksekusi Pengujian

Jalankan pengujian fleet manager langsung dari terminal:

```bash
python public/content/chapter-27/src/fleet_manager.py
```
