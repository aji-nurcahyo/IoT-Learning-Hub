# Tugas & Rubrik — Chapter 17: Rancangan GATT Profile & Optimasi Daya BLE Node

## Skenario Tugas

Anda diminta merancang spesifikasi antarmuka BLE untuk **Smart Soil & Greenhouse Beacon (ESP32)** yang dibaca oleh aplikasi teknisi lapangan menggunakan *smartphone* dan juga menyiarkan status berkala ketika tidak ada yang terhubung.

## Instruksi Pengerjaan

1. **Rancangan Tabel GATT Profile**:
   - Definisikan minimal 1 *Service* (`0x181A` atau UUID 128-bit terstruktur) dan 3 *Characteristic*:
     1. Data sensor telemetri ringkas (*Temperature + Soil Moisture*) dengan format biner *little-endian* beserta satuan dan faktor skalanya.
     2. Konfigurasi *sampling/notify interval* (`READ | WRITE`) dengan validasi batas aman.
     3. Status baterai atau pemicu kalibrasi (`READ | INDICATE` beserta CCCD `0x2902`).
2. **Analisis ATT MTU & Fragmentasi**:
   - Bandingkan ukuran paket biner Anda terhadap padanan string JSON-nya pada `ATT_MTU = 23` dan `ATT_MTU = 247`, serta jelaskan risiko jika *Central* menolak negosiasi MTU.
3. **Implementasi Kode & Simulasi**:
   - Kembangkan variasi [`ble_gatt_sensor.ino`](content/chapter-17/src/ble_gatt_sensor/ble_gatt_sensor.ino) atau skrip Python uji [`ble_gatt_sim.py`](content/chapter-17/src/ble_gatt_sim.py) yang memuat pengodean biner lengkap dan pemulihan *advertising* saat *disconnect*.
4. **Analisis Anggaran Daya & Keamanan**:
   - Hitung estimasi umur baterai pilihan Anda (`CR2032 220 mAh` atau `LiPo 500 mAh`) untuk 2 skenario *Advertising Interval*, serta uraikan strategi pengamanan *pairing/bonding* jika karakteristik *Write* mengubah aktuator.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Poin | Indikator Keberhasilan |
| --- | :---: | --- |
| Desain GAP & hierarki GATT Profile | 25 | Service, Characteristic UUID (16-bit SIG vs 128-bit kustom), Properties, dan CCCD `0x2902` tepat. |
| Pengodean payload & analisis ATT MTU | 25 | Encoding *little-endian* akurat, perbandingan MTU `23` vs `247` terhitung benar, hemat byte. |
| Implementasi firmware & simulasi | 30 | Sketsa/skrip valid, ada *restart advertising* pada `onDisconnect()`, validasi input `WRITE`, bebas crash. |
| Anggaran daya, keamanan & kejujuran bukti | 20 | Perhitungan $I_{\text{avg}}$ & umur baterai logis, mitigasi *MITM/Just Works*, serta status uji dicatat jujur. |
| **Total** | **100** | |

