import math
import json

def calculate_resonance(mass_kg: float, stiffness_n_per_m: float) -> float:
    return (1.0 / (2.0 * math.pi)) * math.sqrt(stiffness_n_per_m / mass_kg)

def run_simulation():
    sensor_mass_kg = 0.035 # 35 gram
    # Kekakuan berbagai jenis mounting (N/m)
    mountings = {
        "stud_mount": 1.0e8,      # Baut stud kaku langsung ke bodi mesin
        "adhesive_epoxy": 3.0e7,   # Lem epoksi industri
        "magnetic_base": 1.2e7,    # Dudukan magnet datar
        "probe_handheld": 2.0e5    # Ujung probe ditekan tangan
    }
    
    results = {}
    for name, k in mountings.items():
        fn = calculate_resonance(sensor_mass_kg, k)
        f_usable = 0.20 * fn # Batas linier (+-5% akurasi)
        results[name] = {
            "stiffness_N_m": k,
            "resonance_hz": round(fn, 1),
            "usable_bandwidth_hz": round(f_usable, 1)
        }
    
    # Assertions
    assert results["stud_mount"]["resonance_hz"] > 8000
    assert results["magnetic_base"]["usable_bandwidth_hz"] > 500
    assert results["probe_handheld"]["usable_bandwidth_hz"] < 300 # Sangat buruk untuk frekuensi tinggi!

    return {
        "status": "PASS",
        "sensor_mass_g": sensor_mass_kg * 1000,
        "mountings_evaluation": results
    }

if __name__ == "__main__":
    out = run_simulation()
    print("=== VIBRATION SENSOR MOUNTING PHYSICS SIMULATION ===")
    print(json.dumps(out, indent=2))
    print("\nSTATUS VERIFIKASI: 100% PASS (Resonansi Mekanis Terbukti Membatasi Bandwidth)")
