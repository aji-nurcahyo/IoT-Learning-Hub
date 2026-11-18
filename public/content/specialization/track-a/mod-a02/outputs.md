# Hasil Eksekusi dan Bukti Pengujian\n\n\\
=== OCCUPANCY SENSING & DCV VENTILATION SIMULATION ===
{
  "status": "PASS",
  "beer_lambert_calibration": {
    "path_length_cm": 5.0,
    "absorption_coef": 0.00045,
    "reference_i0": 5000.0
  },
  "target_evaluation": {
    "measured_intensity": 3850.0,
    "computed_co2_ppm": 116.2,
    "occupancy_type": "STATIC_SEATED",
    "damper_command_pct": 30.0
  },
  "time_series_simulation": [
    {
      "scenario": "Ruangan Kosong Awal",
      "co2_ppm": 37.1,
      "occupancy_type": "UNOCCUPIED",
      "damper_position_pct": 20.0
    },
    {
      "scenario": "Peserta Masuk Bergerak",
      "co2_ppm": 56.8,
      "occupancy_type": "DYNAMIC_WALKING",
      "damper_position_pct": 30.0
    },
    {
      "scenario": "Rapat Berjalan Duduk Diam",
      "co2_ppm": 116.2,
      "occupancy_type": "STATIC_SEATED",
      "damper_position_pct": 30.0
    },
    {
      "scenario": "Konsentrasi CO2 Melonjak",
      "co2_ppm": 198.3,
      "occupancy_type": "STATIC_SEATED",
      "damper_position_pct": 30.0
    },
    {
      "scenario": "Peserta Keluar Ruangan",
      "co2_ppm": 77.5,
      "occupancy_type": "UNOCCUPIED",
      "damper_position_pct": 20.0
    }
  ]
}

STATUS VERIFIKASI: 100% PASS (Model NDIR & Logika DCV Tervalidasi)\n\\
