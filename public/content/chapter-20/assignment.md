# Tugas & Rubrik — Chapter 20: Connected Environmental Monitoring Capstone

## Deskripsi Proyek Akhir Level 2

Bangun dan uji sistem **ESP32 Connected Environmental Monitoring Node** yang menyatukan seluruh lapisan konektivitas Level 2 menggunakan infrastruktur **lokal (*Simulator-First* / *Mosquitto LAN* / *HTTP Server Lokal*)** tanpa ketergantungan layanan cloud berbayar.

## Persyaratan Teknis Sistem

1. **Provisioning & Fallback Konfigurasi**:
   - Memuat kredensial Wi-Fi, alamat broker lokal, `sample_ms`, dan `temp_high_c` dari NVS (`Preferences`), menyinkronkan via **HTTP `GET`** saat online, dan jatuh kembali secara aman ke NVS bila server HTTP tidak tersedia.
2. **Kontrol Lokal Fail-Safe**:
   - Membaca sensor pada pin ADC1 (`GPIO34`) dan mengendalikan aktuator kipas/relay (`GPIO26`) dengan pita histeresis ($T_{\text{high}}$ dan $\Delta T$) secara mandiri meskipun jaringan terputus.
3. **Konektivitas MQTT Lengkap**:
   - Publikasi payload JSON terstruktur (`dev`, `seq`, `ts`, `synced`, `temp`, `th`, `relay`, `q`, `drop`).
   - Implementasi **Retained status (`"online"`)** dan **LWT (`"offline"`)** pada topik status.
   - Berlangganan topik `cmd` untuk pembaruan ambang jarak jauh disertai validasi batas aman dan penyimpanan persisten ke NVS.
4. **Ketahanan Offline & Sinkronisasi Waktu**:
   - Menggunakan SNTP UTC (`time_synced`), *Circular Ring Buffer* berukuran tetap bebas `String` *heap* dinamis, **Full-Jitter Exponential Backoff**, *batch drain* non-blocking, serta deduplikasi idempoten `(dev, seq)` di sisi *subscriber/ingest*.
5. **Pengujian Konektivitas & Pelaporan Kejujuran Bukti**:
   - Jalankan dan dokumentasikan **6 skenario uji wajib** (`TC-01` HTTP fallback, `TC-02` Retained/LWT, `TC-03` Live JSON, `TC-04` Outage buffering + fail-safe, `TC-05` Batch replay + idempotensi, `TC-06` Remote command + LWT drop test).
   - Catat status verifikasi secara jujur (*Software Simulation*, *Compile*, *Simulator Wokwi*, atau *Hardware*).

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Poin | Indikator Keberhasilan |
| --- | :---: | --- |
| Arsitektur firmware terintegrasi & NVS/HTTP fallback | 25 | NVS, ADC1, histeresis lokal *fail-safe*, HTTP GET timeout/fallback, dan FSM non-blocking tersusun modular. |
| Implementasi protokol MQTT, JSON, LWT & validasi `cmd` | 25 | Payload JSON akurat, *Retained* `"online"` + LWT `"offline"` bekerja, serta perintah `cmd` tersanitasi sebelum ubah NVS. |
| Ketahanan jaringan (SNTP, Ring Buffer, Jitter & Idempotency) | 30 | Ring buffer statis, `time_synced` jujur, *Full-Jitter* aktif, *batch drain* aman WDT, dan *replay* bebas duplikat. |
| Eksekusi 6 skenario uji konektivitas & kejujuran bukti | 20 | Seluruh 6 *test case* (`TC-01..TC-06`) terdokumentasi dengan log output aktual dan pemisahan jujur *software/compile/sim/hardware*. |
| **Total** | **100** | |

