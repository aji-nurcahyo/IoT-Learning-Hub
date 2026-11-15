# Panduan Implementasi Kode — Chapter 23

Dokumentasi ini menjelaskan arsitektur dan algoritma yang diimplementasikan pada skrip [`edge_engine.py`](content/chapter-23/src/edge_engine.py).

## Struktur Modul

1. **`filter_outliers_iqr`**:
   - Menghitung kuartil $Q_1$ (persentil 25) dan $Q_3$ (persentil 75) dari larik data yang diurutkan.
   - Mengeliminasi nilai di luar rentang $[Q_1 - 1{,}5 \cdot \text{IQR}, Q_3 + 1{,}5 \cdot \text{IQR}]$.
2. **`DeadbandFilter`**:
   - Membandingkan nilai pengukuran saat ini dengan nilai terakhir yang berhasil dipublikasikan.
   - Mengembalikan `True` jika $|x_{\text{baru}} - x_{\text{terakhir}}| \ge \text{threshold}$, mereduksi banjir paket ketika kondisi lingkungan tidak berubah.
3. **`SlidingWindowAggregator`**:
   - Memelihara buffer geser ukuran tetap $N = 5$.
   - Membersihkan sampel menggunakan filter IQR sebelum menghitung metrik statistik (`mean`, `min`, `max`, `std_dev`).
4. **`LocalAutomationEngine`**:
   - Logika kendali dua ambang batas (*two-threshold hysteresis*):
     - Menyalakan pendingin jika $T \ge T_{\text{high}}$ ($30{,}0\,^\circ\text{C}$).
     - Mematikan pendingin hanya jika $T < T_{\text{high}} - \text{hysteresis}$ ($28{,}5\,^\circ\text{C}$).
   - Mencegah osilasi relay (*chattering*) pada titik kritis.
5. **`EdgeSpoolBuffer`**:
   - Antrean FIFO berkapasitas batas (kapasitas $50$ slot) dengan kebijakan *Drop-Oldest*.
   - Menyediakan metode `drain(batch_size)` untuk mentransfer data bertahap ke cloud saat jaringan pulih.

## Cara Menjalankan

Eksekusi skrip pengujian mandiri dari direktori proyek:

```bash
python public/content/chapter-23/src/edge_engine.py
```
