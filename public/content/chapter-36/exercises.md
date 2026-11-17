# Latihan Chapter 36: Digital Twins & System Modeling

## Latihan Konseptual

1. **Perbedaan Dashboard Telemetri vs Digital Twin**:
   Jelaskan tiga perbedaan fundamental antara *dashboard monitoring telemetri biasa* (seperti Grafana) dengan implementasi *Digital Twin* yang sesungguhnya. Fokuskan penjelasan pada keberadaan model persamaan fisika, kemampuan proyeksi prediktif (*What-If*), dan interaksi kendali dua arah.

2. **Dinamika Termal Hukum Pendinginan Newton**:
   Dalam pemodelan termal 1-orde:
   $$\frac{dT}{dt} = \frac{1}{C_{th}} \left( Q_{in} - \frac{T - T_{amb}}{R_{th}} \right)$$
   Jelaskan arti fisis dari parameter $C_{th}$ (Kapasitas Termal) dan $R_{th}$ (Resistansi Termal). Apa yang terjadi pada respon dinamika pemanasan sistem jika nilai $C_{th}$ diperbesar dua kali lipat?

3. **Mekanisme Deteksi Kebocoran Residu**:
   Bagaimana kembaran digital dapat membedakan antara *gangguan transien sensor* (derau acak ADC) dengan *degradasi fisik permanen aset* (seperti penurunan efisiensi insulasi pendingin)? Jelaskan penggunaan batas ambang galat residu (*residual threshold*) dan durasi persistensi waktu.

## Latihan Praktik & Perhitungan

1. **Kalkulasi Suhu Tunak (Steady-State)**:
   Sebuah lemari instrumen IoT luar ruangan memiliki:
   - Suhu udara lingkungan sekitar ($T_{amb}$) = $28.0^\circ\text{C}$
   - Daya disipasi internal total ($Q_{in}$) = $45.0\text{ Watt}$
   - Resistansi termal dinding konveksi ($R_{th}$) = $0.25\text{ K/Watt}$
   
   *Instruksi*:
   - Hitung suhu tunak ($T_{ss}$) yang akan dicapai di dalam lemari instrumen saat laju akumulasi panas $\frac{dT}{dt} = 0$.
   - Jika batas suhu operasi maksimum komponen elektronik di dalam lemari adalah $45.0^\circ\text{C}$, apakah sistem memerlukan kipas ventilasi pendingin tambahan?

2. **Simulasi Integrasi Diskrit Euler**:
   Tuliskan algoritma iterasi numerik Python sederhana yang menghitung estimasi suhu $T_{k+1}$ dari kondisi awal $T_0 = 25^\circ\text{C}$ selama 3 langkah waktu dengan $\Delta t = 2\text{ detik}$, $Q_{in} = 100\text{ W}$, $C_{th} = 300\text{ J/K}$, $R_{th} = 0.1\text{ K/W}$, dan $T_{amb} = 25^\circ\text{C}$.
