# Bukti & Output Eksekusi — Chapter 03

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (perhitungan analitis rangkaian DC dan *power budget*)
- **Tanggal**: 2026-11-10
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-03/src/electronics_calc.py`
- **Hardware fisik**: Tidak digunakan (rangkaian breadboard & pengukuran multimeter fisik belum dijalankan)

## 2. Output Aktual (Verbatim)

```text
=== KALKULATOR ELEKTRONIKA & POWER BUDGET (CHAPTER 03) ===

1. LED Current-Limiting Resistor (V_CC=3.3V, V_F=2.0V, Target<=6mA)
   R eksak        : 216.7 ohm
   R standar pilih: 220 ohm
   Arus aktual    : 5.91 mA
   Disipasi R     : 7.68 mW (aman untuk resistor 0.25 W = 250 mW)

2. Level Shifting Sensor 5 V ke GPIO 3.3 V via Voltage Divider
   R1=10k, R2=15k -> V_out = 3.00 V | Aman <=3.3V: True
   R1=4.7k, R2=10k -> V_out = 3.40 V | Aman <=3.3V: False (BAHAYA OVERVOLTAGE!)

3. Power Budget Node Sensor (Baterai 2000 mAh, 80% usable, siklus 300 s)
   Arus rata-rata : 0.949 mA
   Kapasitas guna : 1600 mAh
   Estimasi umur  : 1686.9 jam (~70.3 hari)
```

## 3. Catatan Keterbatasan

Hasil di atas adalah verifikasi matematis ideal. Nilai resistor fisik memiliki toleransi (misalnya $\pm 1\%$ atau $\pm 5\%$), tegangan maju LED ($V_F$) bergantung pada warna/datasheet, dan kapasitas baterai aktual dipengaruhi oleh suhu serta *cutoff voltage* regulator.

