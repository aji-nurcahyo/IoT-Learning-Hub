# Panduan Implementasi Kode — Chapter 26

Dokumentasi ini menjelaskan implementasi teknis model dashboard pada [`grafana_dashboard_model.json`](content/chapter-26/src/grafana_dashboard_model.json) dan mesin status peringatan pada [`alert_state_machine.py`](content/chapter-26/src/alert_state_machine.py).

## Struktur Model Dashboard Grafana

Berkas `grafana_dashboard_model.json` mendefinisikan empat panel visualisasi utama:
1. **Panel 1 (`stat`)**: Menampilkan persentase armada aktif dengan ambang batas warna hijau di atas 95%, oranye di atas 80%, dan merah di bawah 80%.
2. **Panel 2 (`stat`)**: Menampilkan metrik *Packet Delivery Ratio* (PDR) dengan satuan persentase.
3. **Panel 3 (`gauge`)**: Memetakan suhu instan terhadap rentang fisik $15\text{–}45\,^\circ\text{C}$ dengan pembagian zona: Biru (Dingin), Hijau ($20\text{–}28\,^\circ\text{C}$), Oranye ($28\text{–}32\,^\circ\text{C}$), dan Merah ($> 32\,^\circ\text{C}$).
4. **Panel 4 (`timeseries`)**: Memvisualisasikan deret waktu 24 jam yang bersumber dari tabel agregasi rollup basis data.

## Logika Alert State Machine (`alert_state_machine.py`)

Kelas `AlertRule` mengelola transisi siklus hidup alarm:
- `evaluate(current_val, now)`:
  1. Jika status `NORMAL` dan `current_val >= threshold_high`: Berpindah ke status `PENDING` dan mencatat `pending_start_time = now`.
  2. Jika status `PENDING`:
     - Jika nilai turun sebelum `pending_duration`: Kembali ke `NORMAL` (meredam lonjakan palsu).
     - Jika bertahan $\ge \text{pending\_duration}$: Berpindah ke `FIRING` dan mengirimkan notifikasi resmi pertama.
  3. Jika status `FIRING`:
     - Jika nilai turun di bawah `threshold_high - hysteresis`: Berpindah ke `RESOLVED` dan mengirimkan notifikasi pemulihan.
     - Jika masih tinggi: Memeriksa apakah selisih waktu terhadap notifikasi terakhir $\ge \text{throttle\_interval}$ sebelum mengirim pengingat ulang.

## Eksekusi Pengujian

Jalankan pengujian mesin status peringatan langsung dari terminal:

```bash
python public/content/chapter-26/src/alert_state_machine.py
```
