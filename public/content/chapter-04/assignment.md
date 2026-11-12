# Tugas & Rubrik — Chapter 04

## Skenario Tugas: Dokumen Pemilihan Board & Peta Pin Aman

Anda diminta merancang rencana *hardware bring-up* untuk sebuah **Node Pemantau Ruang Panel** yang membutuhkan:
- 2 output digital (LED Status & Buzzer aktif 3,3 V via driver),
- 2 input digital (Tombol Reset & Saklar Pintu),
- 1 input analog (Sensor suhu analog),
- 1 antarmuka Serial untuk *debugging*.

## Instruksi Pengerjaan

1. **Pemilihan Varian & Framework**: Pilih satu varian (`ESP32-WROOM-32`, `ESP32-S3`, atau `ESP32-C3`) dan *framework* (`Arduino-ESP32` atau `ESP-IDF`), lalu jelaskan alasan teknisnya.
2. **Tabel Alokasi Pin (*Pin Mapping Table*)**: Tetapkan nomor GPIO spesifik untuk ke-5 sinyal di atas (plus `UART0` debug). Buktikan dengan merujuk dokumentasi resmi varian tersebut bahwa tidak ada pin yang melanggar *SPI Flash*, *input-only*, atau mengganggu *boot strapping*.
3. **BOM, Skema Minimum & Prosedur Bring-Up**: Cantumkan BOM *low-voltage DC*, versi toolchain/board package target, serta langkah *compile, flash*, dan verifikasi *Serial Monitor*.
4. **Rencana Troubleshooting & Status Verifikasi**: Tuliskan 3 potensi kegagalan *boot/flashing* dan nyatakan jujur status verifikasi saat ini (*Belum diuji*, *Compile-verified*, *Simulator-verified*, atau *Hardware-verified* sesuai bukti nyata yang Anda jalankan).

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Justifikasi pemilihan varian chip & framework** | **25** | Pemilihan SoC dan framework beralasan teknis serta mempertimbangkan perbedaan keluarga ESP32. |
| **Alokasi pin aman & analisis batasan** | **30** | Seluruh pin valid sesuai datasheet varian; tidak bentrok dengan SPI Flash, input-only, atau boot strapping. |
| **Kelengkapan BOM, wiring & prosedur bring-up** | **25** | BOM lengkap, resistor pengaman dicantumkan, versi toolchain/board package tercatat, dan langkah uji jelas. |
| **Troubleshooting & kejujuran status uji** | **20** | Prosedur diagnosis boot/serial akurat dan klaim status verifikasi sesuai bukti aktual. |

