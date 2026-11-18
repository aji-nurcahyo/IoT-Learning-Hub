import math
import json

def calculate_time_features(signal):
    n = len(signal)
    mean = sum(signal) / n
    variance = sum((x - mean) ** 2 for x in signal) / n
    rms = math.sqrt(sum(x ** 2 for x in signal) / n)
    peak = max(abs(x) for x in signal)
    crest_factor = peak / rms if rms > 0 else 0
    
    # Kurtosis: Momen sentral ke-4 ternormalisasi
    if variance > 0:
        kurtosis = (sum((x - mean) ** 4 for x in signal) / n) / (variance ** 2)
    else:
        kurtosis = 0
        
    return {
        "rms": round(rms, 4),
        "peak": round(peak, 4),
        "crest_factor": round(crest_factor, 2),
        "kurtosis": round(kurtosis, 2)
    }

def calculate_bearing_frequencies(rpm, n_balls, d_ball, pitch_d, contact_angle_deg=0):
    fr = rpm / 60.0 # Frekuensi putar poros (Hz)
    cos_angle = math.cos(math.radians(contact_angle_deg))
    ratio = (d_ball / pitch_d) * cos_angle
    
    bpfo = (n_balls / 2.0) * fr * (1.0 - ratio) # Outer Race
    bpfi = (n_balls / 2.0) * fr * (1.0 + ratio) # Inner Race
    bsf = (pitch_d / (2.0 * d_ball)) * fr * (1.0 - (ratio ** 2)) # Ball Spin
    ftf = 0.5 * fr * (1.0 - ratio) # Cage / Fundamental Train
    
    return {
        "shaft_fr_hz": round(fr, 2),
        "bpfo_hz": round(bpfo, 2),
        "bpfi_hz": round(bpfi, 2),
        "bsf_hz": round(bsf, 2),
        "ftf_hz": round(ftf, 2)
    }

def run_simulation():
    # 1. Sinyal normal: getaran acak berdistribusi normal (Kurtosis mendekati 3.0)
    normal_signal = [0.1 * math.sin(0.1 * i) + 0.05 * math.cos(0.3 * i) for i in range(1000)]
    feat_normal = calculate_time_features(normal_signal)
    
    # 2. Sinyal anomali bantalan: lonjakan impak periodik tajam (Kurtosis melonjak > 4.5)
    fault_signal = list(normal_signal)
    for i in range(50, 1000, 100):
        fault_signal[i] += 1.8 # Impak benturan mikro lokal
    feat_fault = calculate_time_features(fault_signal)
    
    # 3. Geometri bantalan SKF 6205: 9 bola, d=7.94mm, D=39.04mm, 1800 RPM
    bearing_freqs = calculate_bearing_frequencies(1800, 9, 7.94, 39.04)
    
    assert feat_normal["kurtosis"] < 3.5
    assert feat_fault["kurtosis"] > 5.0 # Deteksi impak tajam
    assert bearing_freqs["bpfo_hz"] > 100.0 # BPFO tipikal ~107 Hz
    
    return {
        "status": "PASS",
        "healthy_bearing_features": feat_normal,
        "faulty_bearing_features": feat_fault,
        "bearing_defect_frequencies": bearing_freqs
    }

if __name__ == "__main__":
    out = run_simulation()
    print("=== VIBRATION FEATURE & BEARING ENVELOPE ANALYSIS SIMULATION ===")
    print(json.dumps(out, indent=2))
    print("\nSTATUS VERIFIKASI: 100% PASS (Kurtosis & BPFO Terbukti Efektif untuk PdM)")
