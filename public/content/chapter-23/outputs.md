# Bukti Pengujian & Hasil Eksekusi — Chapter 23

Pengujian mesin pemrosesan edge, algoritma pemfilteran statistik, aturan histeresis lokal, dan sinkronisasi buffer dieksekusi menggunakan lingkungan runtime Python 3.

## Perintah Eksekusi

```bash
python public/content/chapter-23/src/edge_engine.py
```

## Hasil Keluaran Terminal (Standard Output)

```text
=== Edge Processing & Local Automation Verification Suite ===
Test 1 - IQR Filter: Dari 8 sampel mentah -> 6 sampel bersih.
   Raw: [26.1, 26.3, 26.2, 99.9, 26.4, 26.2, -45.0, 26.5]
   Cleaned: [26.1, 26.3, 26.2, 26.4, 26.2, 26.5]

Test 2 - Deadband Filter (threshold 0.5 C):
   Input stream : [25.0, 25.1, 25.2, 25.6, 25.7, 26.3]
   Published    : [25.0, 25.6, 26.3] (Meredam 3 fluktuasi kecil)

Test 3 - Sliding Window Aggregation (5 samples):
   Metrik agregat: {'count': 5, 'mean': 26.0, 'min': 25.5, 'max': 26.5, 'std_dev': 0.34}

Test 4 - Hysteresis Control (High: 30.0 C, Hysteresis: 1.5 C):
   Temp: 28.0 C | Relay: OFF | Action: NO_CHANGE
   Temp: 29.8 C | Relay: OFF | Action: NO_CHANGE
   Temp: 30.2 C | Relay: ON  | Action: RELAY_TURNED_ON
   Temp: 29.9 C | Relay: ON  | Action: NO_CHANGE
   Temp: 29.0 C | Relay: ON  | Action: NO_CHANGE
   Temp: 28.6 C | Relay: ON  | Action: NO_CHANGE
   Temp: 28.4 C | Relay: OFF | Action: RELAY_TURNED_OFF
   Temp: 28.0 C | Relay: OFF | Action: NO_CHANGE

Test 5 - Edge Spooling & Cloud Sync:
   Total buffer setelah 12 push (kapasitas 10): 10 entri
   Drain batch 1 (5 entri): id 2 hingga 6
   Sisa buffer dalam antrean: 5 entri

All edge processing test cases passed successfully.
```

## Analisis Hasil

1. **Efektivitas Filter IQR**: Dua lonjakan derau ekstrem (`99.9` dan `-45.0`) berhasil disaring dan dibuang tanpa merusak distribusi nilai normal di sekitar $26\,^\circ\text{C}$.
2. **Reduksi Deadband**: Sebanyak $50\%$ paket transmisi yang hanya berfluktuasi kecil di bawah ambang $0{,}5\,^\circ\text{C}$ berhasil diredam.
3. **Stabilitas Histeresis**: Ketika suhu naik ke $30{,}2\,^\circ\text{C}$, relay aktif. Saat suhu berosilasi turun ke $29{,}9\,^\circ\text{C}$, $29{,}0\,^\circ\text{C}$, dan $28{,}6\,^\circ\text{C}$, relay tetap bertahan dalam status aktif. Relay baru mati saat suhu menyentuh $28{,}4\,^\circ\text{C}$ ($< 28{,}5\,^\circ\text{C}$), membuktikan efektivitas kontrol anti-chattering.
4. **Keandalan Spool Buffer**: Mekanisme pembatasan kapasitas (kapasitas 10 dengan 12 masukan) mempertahankan 10 data terbaru dan membuang 2 data terlama (*drop-oldest*), serta berhasil menguras batch 5 item pertama saat koneksi diaktifkan kembali.
