# Hasil Eksekusi dan Bukti Pengujian\n\n\\
=== EMBEDDED AI ROOFLINE HARDWARE MODEL SIMULATION ===
{
  "status": "PASS",
  "conv1d_flash_execution": {
    "operational_intensity_mac_per_byte": 4.5,
    "peak_gmacs": 0.8,
    "memory_bandwidth_gb_s": 0.08,
    "attainable_gmacs": 0.36,
    "bottleneck": "MEMORY_BOUND"
  },
  "conv1d_sram_execution": {
    "operational_intensity_mac_per_byte": 4.5,
    "peak_gmacs": 0.8,
    "memory_bandwidth_gb_s": 1.6,
    "attainable_gmacs": 0.8,
    "bottleneck": "COMPUTE_BOUND"
  },
  "dense_flash_execution": {
    "operational_intensity_mac_per_byte": 0.5,
    "peak_gmacs": 0.8,
    "memory_bandwidth_gb_s": 0.08,
    "attainable_gmacs": 0.04,
    "bottleneck": "MEMORY_BOUND"
  },
  "dense_sram_execution": {
    "operational_intensity_mac_per_byte": 0.5,
    "peak_gmacs": 0.8,
    "memory_bandwidth_gb_s": 1.6,
    "attainable_gmacs": 0.8,
    "bottleneck": "COMPUTE_BOUND"
  }
}

STATUS VERIFIKASI: 100% PASS (Model Kinerja Roofline Terbukti Memvalidasi Bottleneck)\n\\
