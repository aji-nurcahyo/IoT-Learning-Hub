# Panduan Implementasi: Digital Twins & System Modeling

Dokumen ini menjelaskan implementasi teknis pemodelan matematika sistem fisik berbasis persamaan diferensial dinamika termal dan modul sinkronisasi kembaran digital Python.

## 1. Modul Simulasi Kembaran Digital Python

Modul [digital_twin_sim.py](file:///d:/Workstation/Repo%20My%20Corses/Internet%20Of%20Things/public/content/chapter-36/src/digital_twin_sim.py) mengintegrasikan dua komponen inti:
1. `ThermalSystemModel`: mengimplementasikan model dinamika termal 1-orde berbasis Hukum Pendinginan Newton dan pemanasan Joule:
   $$\frac{dT}{dt} = \frac{1}{C_{th}} \left( Q_{in} - \frac{T - T_{amb}}{R_{th}} \right)$$
2. `DigitalTwinSynchronizer`: membandingkan suhu terukur riil ($T_{measured}$) dengan estimasi model virtual ($T_{estimated}$), menghitung besaran galat residu, dan menyediakan fungsi `simulate_what_if_scenario` untuk proyeksi prediktif bebas risiko.

Jalankan pengujian menggunakan:

```bash
python public/content/chapter-36/src/digital_twin_sim.py
```

### Hasil Verifikasi Eksekusi:
```text
=== CHAPTER 36: DIGITAL TWIN & SYSTEM MODELING SIMULATION ===
Siklus Sinkronisasi Real-Time (Daya = 100W, dt = 2s):
Step 1 | Fisik: 25.5 C | Digital: 25.667 C | Residual: 0.167 C | Status: SYNCHRONIZED
Step 2 | Fisik: 26.1 C | Digital: 26.289 C | Residual: 0.189 C | Status: SYNCHRONIZED
Step 3 | Fisik: 26.8 C | Digital: 26.87 C | Residual: 0.07 C | Status: SYNCHRONIZED
Step 4 | Fisik: 27.4 C | Digital: 27.412 C | Residual: 0.012 C | Status: SYNCHRONIZED
Step 5 | Fisik: 28.0 C | Digital: 27.918 C | Residual: 0.082 C | Status: SYNCHRONIZED

Simulasi What-If: Prediksi Suhu 60s ke Depan pada 250W -> 47.11 C
STATUS: VERIFIED (Semua pengujian sinkronisasi Digital Twin dan skenario What-If lulus 100%)
```

## 2. Keuntungan Analisis Skenario What-If

Fungsi `simulate_what_if_scenario(future_power_watts=250.0, duration_seconds=60.0)` memproyeksikan lintasan pemanasan jauh lebih cepat daripada waktu nyata:
- Proyeksi menunjukkan suhu akan melonjak tajam ke angka $47.11^\circ\text{C}$.
- Jika batas keselamatan modul adalah $45.0^\circ\text{C}$, sistem kontrol dapat menolak perintah peningkatan daya tersebut secara otomatis di level digital sebelum terjadi kerusakan termal pada perangkat keras nyata.
