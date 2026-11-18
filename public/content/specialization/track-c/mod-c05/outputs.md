# Hasil Eksekusi dan Bukti Pengujian\n\n\\
=== FAO-56 PENMAN-MONTEITH EVAPOTRANSPIRATION SIMULATION ===
{
  "status": "PASS",
  "meteorological_inputs": {
    "temperature_c": 28.0,
    "net_radiation_mj_m2": 16.5,
    "wind_speed_2m_m_s": 1.8,
    "relative_humidity_pct": 70.0,
    "vapor_pressure_deficit_kpa": 1.134
  },
  "evapotranspiration_results": {
    "reference_et0_mm_day": 5.78,
    "crop_coefficient_kc": 1.15,
    "crop_etc_mm_day": 6.65
  },
  "soil_water_balance": {
    "total_available_water_taw_mm": 80.0,
    "readily_available_water_raw_mm": 40.0,
    "irrigation_triggered": true,
    "target_irrigation_depth_mm": 6.65,
    "valve_open_duration_minutes": 99.8
  }
}

STATUS VERIFIKASI: 100% PASS (Model FAO-56 & Neraca Air Tervalidasi)\n\\
