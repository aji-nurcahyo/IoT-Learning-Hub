# Source Code — Chapter 03: Kalkulator Elektronika & Power Budget

Folder `src/` berisi skrip Python untuk menghitung nilai resistor pembatas arus LED, mengevaluasi keamanan *voltage divider* terhadap batas GPIO 3,3 V, dan mengestimasi umur baterai dari *duty-cycle* aktif vs *sleep*.

## Ringkasan File

- [electronics_calc.py](content/chapter-03/src/electronics_calc.py): Skrip Python 3 standar untuk verifikasi perhitungan Hukum Ohm, daya disipasi, *voltage divider*, dan *power budget*.

## Cara Menjalankan

```sh
python public/content/chapter-03/src/electronics_calc.py
```

## Status Verifikasi

- **Software model (`electronics_calc.py`)**: Dieksekusi langsung pada Python 3.12.10; hasil tercetak pada `outputs.md`.
- **Hardware fisik**: Pengukuran multimeter dan rangkaian breadboard bersifat opsional (Path B) dan belum dijalankan secara fisik pada fase ini.

