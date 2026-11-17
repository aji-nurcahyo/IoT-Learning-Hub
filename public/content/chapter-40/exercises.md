# Latihan Chapter 40: Advanced IoT Systems Capstone

## Latihan Konseptual

1. **Sintesis Arsitektur End-to-End**:
   Jelaskan bagaimana keenam subsistem utama (Low-Power, FreeRTOS, Modbus RTU, TinyML INT8, Digital Twin, dan Resilience/Privacy) saling berinteraksi di dalam satu node pemantau industri cerdas. Gambarkan diagram alir data (*data pipeline flow*) dari saat sensor membaca getaran fisik hingga status anomali tercermin pada kembaran digital.

2. **Dinamika Integrasi RTOS & TinyML**:
   Ketika model inferensi TinyML dijalankan pada sebuah task FreeRTOS, jelaskan pertimbangan penentuan alokasi ukuran *Stack Memory* (`usStackDepth`) dan tingkat prioritas eksekusi task agar inferensi tidak mengorbankan ketepatan waktu (*timing jitter*) task penjaga keselamatan (*Safety Watchdog*).

3. **Peran Matriks Penerimaan Sistem (SATC)**:
   Mengapa dalam metodologi rekayasa sistem profesional, pengujian fungsional selalu dikelompokkan ke dalam kasus uji penerimaan terstruktur (*System Acceptance Test Cases / SATC*) dengan ambang batas lulus/gagal (*pass/fail criteria*) yang tegas? Sebutkan manfaat pendekatan ini bagi proses audit kepatuhan industri.

## Latihan Praktik & Perhitungan

1. **Analisis Kuantifikasi Matriks SATC**:
   Berdasarkan hasil eksekusi suite pengujian capstone pada modul `advanced_capstone_platform.py`:
   - Uraikan hasil kuantitatif kasus uji **SATC-01** (arus rata-rata $I_{avg}$ dan masa pakai baterai).
   - Uraikan hasil kasus uji **SATC-04** (fitur RMS, P2P, dan label prediksi yang dihasilkan model TinyML).
   - Uraikan hasil kasus uji **SATC-05** (suhu terestimasi real-time vs proyeksi skenario *What-If* saat daya dinaikkan ke 250 Watt).

2. **Perancangan Modul Uji Ketahanan Tambahan (SATC-07)**:
   Rancanglah satu kasus uji penerimaan sistem tambahan (**SATC-07: Cryptographic OTA Rollback Test**) yang memverifikasi bahwa jika file biner pembaruan firmware memiliki tanda tangan digital yang rusak, sistem bootloader akan membatalkan proses flashing dan melakukan *automatic rollback* ke partisi firmware sebelumnya tanpa membuat perangkat macet (*unbricked*).
