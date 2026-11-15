# Tugas Mandiri: Proyek Capstone Level 3 — Platform Pemantauan IoT Terintegrasi

## Deskripsi Tugas

Tugas akhir Level 3 ini merupakan proyek integratif berskala penuh: **Scalable IoT Environmental Monitoring & Management Platform**. Anda diminta untuk mengintegrasikan seluruh konsep data models, gateway edge, penyimpanan deret waktu teroptimasi, dashboarding & alerting anti-fatigue, manajemen armada berbasis digital twin, dan pembaruan OTA aman ke dalam sebuah sistem terpadu yang dapat diuji secara mandiri (*local-first & simulator-first*).

## Petunjuk Pengerjaan

1. **Arsitektur Multi-Subsistem Terpadu**:
   - Susun dan integrasikan seluruh modul inti pada skrip [`capstone_platform.py`](content/chapter-30/src/capstone_platform.py):
     - `DeviceTwinRegistry`: Registri inventaris perangkat dan pelacak status kembar konfigurasi (*Desired vs Reported*).
     - `TopicAclAuthorizer`: Penegak matriks otorisasi topik MQTT berdasarkan pola identitas klien.
     - `EdgeGatewayProcessor`: Mesin validasi skema, penyaring duplikasi pesan (*Idempotency Dedup*), dan kompresi *Deadband*.
     - `CapstoneTimeSeriesStorage`: Basis data SQLite deret waktu dengan pipeline *1-minute rollup* dan pembersihan retensi berkala.
     - `CapstoneAlertEngine`: Mesin status peringatan 4-tahap (`NORMAL` $\rightarrow$ `PENDING` $\rightarrow$ `FIRING` $\rightarrow$ `RESOLVED`) dengan kontrol histeresis anti-flapping.
     - `CapstoneOtaManager`: Simulator distribusi firmware bertahap dengan verifikasi tanda tangan kriptografis dan pemulihan mandiri (*Automatic Rollback*).
2. **Eksekusi 6 Kasus Uji Penerimaan Sistem (SATC)**:
   - Jalankan fungsi `run_capstone_acceptance_tests()` dan buktikan bahwa seluruh 6 skenario penerimaan sistem berhasil dieksekusi dengan status lulus (*PASS*).
3. **Penyusunan Laporan Uji & Analisis Teknis**:
   - Catat log hasil eksekusi terminal pada berkas [`outputs.md`](content/chapter-30/outputs.md).
   - Susun analisis komparasi teknis yang mengevaluasi trade-off arsitektur, efisiensi komputasi edge, dan ketahanan sistem terhadap skenario kegagalan jaringan atau firmware.

## Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :--- | :---: | :--- |
| **Arsitektur Integrasi & Kebersihan Kode** | 35 | Seluruh 6 subsistem terintegrasi harmonis; kode modular, bebas ketergantungan cloud berbayar, dan mematuhi prinsip anti-slop. |
| **Kebenaran Fungsional Matriks SATC** | 35 | Seluruh 6 kasus uji penerimaan sistem (SATC-01 sampai SATC-06) dieksekusi tuntas dan lulus verifikasi tanpa galat logika. |
| **Analisis Keandalan & Kelengkapan Bukti** | 30 | Log bukti uji terdokumentasi lengkap dan deterministik; analisis teknis membedah ketahanan sistem secara mendalam dan terukur. |
