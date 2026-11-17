# Tugas Terbimbing: Perancangan Arsitektur Konkurensi & Penjadwalan Preemptive FreeRTOS

## Deskripsi Tugas

Dalam tugas ini, Anda diminta merancang dan memverifikasi arsitektur penjadwalan sistem tertanam *real-time* berbasis FreeRTOS pada ESP32 serta memvalidasi perilaku penanganan konkurensi melalui eksekusi modul simulasi Python mandiri.

Tugas ini mewajibkan:
1. Pemodelan logika penjadwalan *preemptive fixed-priority* yang membuktikan bahwa task berprioritas lebih tinggi merebut CPU tanpa penundaan.
2. Implementasi antrean *thread-safe* (*FreeRTOS Queue*) dengan pembuktian penanganan luapan memori (*buffer overflow mitigation*).
3. Kode firmware C++ ESP32 yang mendemonstrasikan pola *Producer-Consumer* menggunakan Queue, sinkronisasi periferal serial menggunakan Mutex, dan penetapan task ke core prosesor tertentu (*core pinning*).

## Petunjuk Pengumpulan

1. Kode sumber simulasi Python: `public/content/chapter-32/src/rtos_scheduler_sim.py`.
2. Kode firmware FreeRTOS ESP32: `public/content/chapter-32/src/esp32_freertos_tasks.ino`.
3. Laporan teknis yang menyajikan analisis *timeline* eksekusi (diagram Gantt) serta evaluasi mitigasi *priority inversion*.

## Rubrik Penilaian (Total: 100 Poin)

| Kriteria | Bobot | Deskripsi |
|---|:---:|---|
| **Akurasi Model Penjadwal & Mekanisme Preemption** | 35 Poin | Simulasi penjadwalan preemptive berbasis prioritas membuktikan preemption seketika, perhitungan *turnaround time*, dan *waiting time* yang tepat dan terverifikasi otomatis. |
| **Penerapan Primitif Sinkronisasi FreeRTOS** | 35 Poin | Kode C++ mengimplementasikan Queue dan Mutex secara disiplin, memisahkan domain produsen dan konsumen secara elegan, serta mencegah *race condition* pada UART Serial. |
| **Analisis Keandalan Konkurensi & Mitigasi Bahaya** | 30 Poin | Pembahasan mendalam mengenai penanganan *overflow queue*, monitoring sisa stack task (*watermark*), dan analisis teoritis pencegahan *deadlock* serta *priority inversion*. |
