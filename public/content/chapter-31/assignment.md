# Tugas Terbimbing: Analisis Profil Daya dan Estimasi Masa Pakai Baterai IoT

## Deskripsi Tugas

Dalam tugas ini, Anda diminta merancang model analisis konsumsi energi perangkat IoT pemantau lingkungan luar ruangan (*outdoor*) dan memvalidasi estimasi masa pakai baterai melalui eksekusi skrip pemodelan Python serta penulisan kode firmware ESP32 hemat daya.

Proyek ini harus mengimplementasikan:
1. Pemodelan matematis konsumsi muatan listrik berkala ($Q = \int I\,dt$) dengan mempertimbangkan variasi waktu aktif dan durasi *deep sleep*.
2. Estimasi usia operasional baterai nyata dengan memasukkan faktor *derating* kapasitas nominal serta laju *self-discharge* tahunan.
3. Struktur firmware ESP32 berbasis Arduino Core yang memanfaatkan RTC Timer Wake-up dan variabel persisten pada `RTC_DATA_ATTR`.

## Petunjuk Pengumpulan

1. Kode sumber simulasi Python: `public/content/chapter-31/src/power_model_sim.py`.
2. Kode firmware contoh: `public/content/chapter-31/src/esp32_low_power_firmware.ino`.
3. Laporan teknis ringkas yang menyajikan tabel perbandingan skenario konsumsi daya serta grafik/tinjauan trade-off latensi data versus masa pakai baterai.

## Rubrik Penilaian (Total: 100 Poin)

| Kriteria | Bobot | Deskripsi |
|---|:---:|---|
| **Akurasi Model Matematis Konsumsi Muatan** | 35 Poin | Perhitungan arus rata-rata ($I_{avg}$), muatan per siklus ($Q_{cycle}$), dan estimasi masa pakai baterai berbasis derating kapasitas serta *self-discharge* terbukti akurat dan konsisten secara teoritis. |
| **Implementasi Firmware ESP32 & Wake-up Source** | 35 Poin | Kode firmware menerapkan konfigurasi *deep sleep* yang tepat, pembersihan buffer UART sebelum tidur, pemeliharaan status pada RTC slow memory, dan penanganan sumber bangun secara benar. |
| **Analisis Rekayasa & Trade-off Latensi vs Daya** | 30 Poin | Analisis menyajikan pemahaman mendalam mengenai dampak interval transmisi, strategi power gating sensor, serta kompromi antara latensi telemetri dengan masa hidup operasional sistem. |
