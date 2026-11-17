# Panduan Implementasi: Edge AI, TinyML & Sensor Inference

Dokumen ini menjelaskan implementasi teknis algoritma ekstraksi fitur domain waktu dan inferensi model neural network terkuantisasi INT8 pada sistem tertanam.

## 1. Modul Simulasi Ekstraksi Fitur & TinyML Python

Modul [tinyml_inference_sim.py](file:///d:/Workstation/Repo%20My%20Corses/Internet%20Of%20Things/public/content/chapter-35/src/tinyml_inference_sim.py) mengintegrasikan dua alur pemrosesan:
1. `extract_features(signal)`: menghitung nilai statistik *Mean*, *Root Mean Square* (RMS), *Peak-to-Peak* (P2P), dan *Zero Crossing Rate* (ZCR) dari sinyal getaran akselerometer.
2. `TinyMLQuantizedClassifier`: mengonversi input fitur ke integer bertanda INT8 melalui fungsi `quantize_input` ($S=0.05, Z=0$) dan menjalankan dot product integer untuk menghasilkan skor klasifikasi kondisi motor.

Jalankan pengujian menggunakan:

```bash
python public/content/chapter-35/src/tinyml_inference_sim.py
```

### Hasil Verifikasi Eksekusi:
```text
=== CHAPTER 35: TINYML & SENSOR INFERENCE SIMULATION ===
Fitur Sinyal Normal: RMS=0.188, P2P=0.55, ZCR=0.5063
Fitur Sinyal Anomali: RMS=1.9035, P2P=5.9, ZCR=0.5063
Inferensi Normal -> Label: NORMAL (Scores: [255, 120])
Inferensi Anomali -> Label: ANOMALY_BEARING_FAULT (Scores: [-2030, 3110])
STATUS: VERIFIED (Semua pengujian ekstraksi fitur dan inferensi TinyML INT8 lulus 100%)
```

## 2. Mekanisme Kuantisasi Fixed-Point INT8

Kuantisasi bobot neural network ke dalam INT8 memangkas kebutuhan alokasi memori Flash hingga 75%:

```python
def quantize_input(self, val: float) -> int:
    q = int(round(val / self.scale_in)) + self.zero_point_in
    return max(-128, min(127, q))
```

Pada komputasi inferensi, operasi dot-product dieksekusi murni menggunakan aritmatika integer 32-bit akumulator:
$$\text{Score}_k = \sum_{j} (x_{q, j} \times w_{q, kj}) + b_{q, k}$$

Hal ini mengeliminasi kebutuhan instruksi perangkat lunak emulasi *floating point* pada prosesor tanpa FPU, sehingga inferensi dapat tuntas dalam skala mikrodetik.
