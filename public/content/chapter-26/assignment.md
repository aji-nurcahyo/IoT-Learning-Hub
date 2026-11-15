# Tugas Mandiri: Perancangan Dashboard Industri & Alert State Machine

## Deskripsi Tugas

Tugas ini melatih mahasiswa merancang arsitektur visualisasi pemantauan lingkungan IoT berbasis spesifikasi model Grafana, serta mengimplementasikan mesin status peringatan (*Alert State Machine*) yang andal, tahan terhadap derau instan, dan bebas dari fenomena *alert flapping* maupun *alert fatigue*.

## Petunjuk Pengerjaan

1. **Perancangan Model Dashboard Declarative**:
   - Susun berkas konfigurasi deklaratif [`grafana_dashboard_model.json`](content/chapter-26/src/grafana_dashboard_model.json) yang menerapkan prinsip hierarki visual:
     - Panel 1: Stat Panel metrik ketersediaan armada (*Fleet Health Availability*).
     - Panel 2: Stat Panel rasio pengantaran paket (*Packet Delivery Ratio / PDR*).
     - Panel 3: Gauge Panel pembacaan suhu langsung dengan zona warna bertingkat (Hijau, Oranye, Merah).
     - Panel 4: Time-Series Graph pergerakan suhu dan kelembapan 24 jam dari tabel rollup.
2. **Implementasi Alert State Machine**:
   - Bangun kelas `AlertRule` yang mengelola empat status siklus hidup peringatan: `NORMAL`, `PENDING`, `FIRING`, dan `RESOLVED`.
   - Terapkan parameter durasi evaluasi penahanan $T_{\text{for}} = 5\text{ detik}$ untuk meredam lonjakan sementara (*transient spikes*).
3. **Penerapan Histeresis & Throttling**:
   - Terapkan pita histeresis $1{,}0\,^\circ\text{C}$ pada ambang batas pelepasan alarm untuk mencegah osilasi status saat suhu berada di titik kritis.
   - Terapkan mekanisme pembatasan frekuensi pengingat (*notification throttling* dengan interval $15\text{ detik}$) selama kondisi anomali masih berlangsung.
4. **Validasi Simulasi Deterministik**:
   - Uji alur menggunakan skrip [`alert_state_machine.py`](content/chapter-26/src/alert_state_machine.py) melintasi 10 titik waktu evaluasi (termasuk kasus lonjakan sesaat, insiden panas persisten, jeda pengingat, dan pemulihan sistem).
   - Lampirkan log keluaran eksekusi terminal dan analisis grafiknya pada laporan.

## Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :---: | :--- | :---: | :--- |
| 1 | **Hierarki Visual & Model Dashboard** | 35 | Model deklaratif JSON tersusun rapi; pemilihan panel tepat guna dan konfigurasi ambang batas warna mematuhi kaidah fungsional industri. |
| 2 | **Keandalan Alert State Machine** | 35 | Transisi status (Normal -> Pending -> Firing -> Resolved) akurat; lonjakan transien sesaat berhasil diredam oleh durasi $T_{\text{for}}$. |
| 3 | **Pencegahan Flapping & Throttling Notifikasi** | 30 | Logika histeresis dan notification throttling berhasil mencegah alert spam; seluruh skenario simulasi lulus verifikasi otomatis. |
