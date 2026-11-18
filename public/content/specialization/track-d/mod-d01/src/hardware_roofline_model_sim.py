import json

def calculate_roofline_performance(peak_gmacs, memory_bandwidth_gb_s, operational_intensity):
    # Roofline Model: Attainable Performance = min(Peak Performance, Operational Intensity * Memory Bandwidth)
    memory_bound_perf = operational_intensity * memory_bandwidth_gb_s
    attainable_perf = min(peak_gmacs, memory_bound_perf)
    is_memory_bound = memory_bound_perf < peak_gmacs
    
    return {
        "operational_intensity_mac_per_byte": operational_intensity,
        "peak_gmacs": peak_gmacs,
        "memory_bandwidth_gb_s": memory_bandwidth_gb_s,
        "attainable_gmacs": round(attainable_perf, 3),
        "bottleneck": "MEMORY_BOUND" if is_memory_bound else "COMPUTE_BOUND"
    }

def run_simulation():
    # Profil mikrokontroler Cortex-M55 / ESP32-S3: Peak = 0.8 GMAC/s (400 MHz Dual-MAC), Flash SPI = 0.08 GB/s (80 MB/s)
    peak_gmacs = 0.8
    bw_flash = 0.08 # Eksternal Flash SPI
    bw_sram = 1.6   # Internal SRAM TCM (1600 MB/s)
    
    # Layer 1: Conv1D (Intensitas Aritmatika tinggi karena weight reuse, I = 4.5 MAC/byte)
    conv_flash = calculate_roofline_performance(peak_gmacs, bw_flash, 4.5)
    conv_sram = calculate_roofline_performance(peak_gmacs, bw_sram, 4.5)
    
    # Layer 2: Fully-Connected / Dense (Intensitas Aritmatika rendah, streaming weights, I = 0.5 MAC/byte)
    fc_flash = calculate_roofline_performance(peak_gmacs, bw_flash, 0.5)
    fc_sram = calculate_roofline_performance(peak_gmacs, bw_sram, 0.5)
    
    assert conv_flash["attainable_gmacs"] <= peak_gmacs
    assert fc_flash["bottleneck"] == "MEMORY_BOUND" # Terbukti dibatasi transfer flash!
    assert conv_sram["bottleneck"] == "COMPUTE_BOUND" # Maksimal di SRAM!
    
    return {
        "status": "PASS",
        "conv1d_flash_execution": conv_flash,
        "conv1d_sram_execution": conv_sram,
        "dense_flash_execution": fc_flash,
        "dense_sram_execution": fc_sram
    }

if __name__ == "__main__":
    out = run_simulation()
    print("=== EMBEDDED AI ROOFLINE HARDWARE MODEL SIMULATION ===")
    print(json.dumps(out, indent=2))
    print("\nSTATUS VERIFIKASI: 100% PASS (Model Kinerja Roofline Terbukti Memvalidasi Bottleneck)")
