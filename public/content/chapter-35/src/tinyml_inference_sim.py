"""
Chapter 35: Edge AI, TinyML & Sensor Inference Simulator
Ekstraksi fitur sinyal getaran (Mean, RMS, Peak-to-Peak, Zero-Crossing) dan inferensi model TinyML terkuantisasi (INT8).
"""

from typing import List, Dict, Any, Tuple
import math


def extract_features(signal: List[float]) -> Dict[str, float]:
    """Mengekstraksi fitur statistik domain waktu dari sinyal sensor akselerometer/getaran."""
    n = len(signal)
    if n == 0:
        raise ValueError("Sinyal tidak boleh kosong!")

    # 1. Mean
    mean_val = sum(signal) / n

    # 2. RMS (Root Mean Square)
    sum_squares = sum(x ** 2 for x in signal)
    rms_val = math.sqrt(sum_squares / n)

    # 3. Peak-to-Peak (P2P)
    peak_to_peak = max(signal) - min(signal)

    # 4. Zero Crossing Rate (ZCR)
    zero_crossings = 0
    for i in range(1, n):
        if (signal[i] >= 0 and signal[i - 1] < 0) or (signal[i] < 0 and signal[i - 1] >= 0):
            zero_crossings += 1
    zcr = zero_crossings / (n - 1)

    return {
        "mean": round(mean_val, 4),
        "rms": round(rms_val, 4),
        "peak_to_peak": round(peak_to_peak, 4),
        "zcr": round(zcr, 4)
    }


class TinyMLQuantizedClassifier:
    """Simulasi model TinyML Dense Layer terkuantisasi INT8 untuk klasifikasi anomali mesin."""
    def __init__(self):
        # Bobot terkuantisasi INT8 [-128, 127] untuk 2 fitur [RMS, Peak-to-Peak]
        # Kelas 0: Normal, Kelas 1: Anomali Getaran
        # Untuk sinyal normal (RMS kecil, P2P kecil), score[0] > score[1]
        # Untuk sinyal anomali (RMS besar, P2P besar), score[1] > score[0]
        self.weights = [
            [-20, -15],  # Bobot kelas Normal
            [25, 20],    # Bobot kelas Anomali
        ]
        self.bias = [500, -200]
        self.scale_in = 0.05
        self.zero_point_in = 0

    def quantize_input(self, val: float) -> int:
        """Mengonversi floating-point ke integer INT8."""
        q = int(round(val / self.scale_in)) + self.zero_point_in
        return max(-128, min(127, q))

    def predict(self, rms: float, peak_to_peak: float) -> Dict[str, Any]:
        """Inferensi feedforward INT8 berdaya komputasi mikrodetik."""
        q_rms = self.quantize_input(rms)
        q_p2p = self.quantize_input(peak_to_peak)

        scores: List[int] = []
        for i in range(2):
            score = (q_rms * self.weights[i][0]) + (q_p2p * self.weights[i][1]) + self.bias[i]
            scores.append(score)

        predicted_class = 0 if scores[0] > scores[1] else 1
        label = "NORMAL" if predicted_class == 0 else "ANOMALY_BEARING_FAULT"

        return {
            "predicted_class": predicted_class,
            "label": label,
            "raw_scores": scores,
            "quantized_inputs": [q_rms, q_p2p]
        }


def run_tinyml_simulation() -> None:
    print("=== CHAPTER 35: TINYML & SENSOR INFERENCE SIMULATION ===")
    
    # 1. Sinyal Normal Mesin (Getaran rendah harmonik)
    normal_signal = [0.12, 0.25, -0.15, -0.30, 0.10, 0.22, -0.18, 0.05] * 10
    feat_norm = extract_features(normal_signal)
    print(f"Fitur Sinyal Normal: RMS={feat_norm['rms']}, P2P={feat_norm['peak_to_peak']}, ZCR={feat_norm['zcr']}")

    # 2. Sinyal Anomali Bantalan Aus (Lonjakan impak mekanis)
    anomaly_signal = [0.85, 2.45, -1.95, -0.40, 3.10, 0.20, -2.80, 0.90] * 10
    feat_anom = extract_features(anomaly_signal)
    print(f"Fitur Sinyal Anomali: RMS={feat_anom['rms']}, P2P={feat_anom['peak_to_peak']}, ZCR={feat_anom['zcr']}")

    # 3. Inferensi Model Terkuantisasi INT8
    model = TinyMLQuantizedClassifier()
    res_norm = model.predict(rms=feat_norm["rms"], peak_to_peak=feat_norm["peak_to_peak"])
    print(f"Inferensi Normal -> Label: {res_norm['label']} (Scores: {res_norm['raw_scores']})")

    res_anom = model.predict(rms=feat_anom["rms"], peak_to_peak=feat_anom["peak_to_peak"])
    print(f"Inferensi Anomali -> Label: {res_anom['label']} (Scores: {res_anom['raw_scores']})")

    assert res_norm["predicted_class"] == 0, "Sinyal normal salah diklasifikasikan!"
    assert res_anom["predicted_class"] == 1, "Sinyal anomali gagal dideteksi!"
    print("STATUS: VERIFIED (Semua pengujian ekstraksi fitur dan inferensi TinyML INT8 lulus 100%)")


if __name__ == "__main__":
    run_tinyml_simulation()
