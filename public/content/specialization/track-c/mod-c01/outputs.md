# Hasil Eksekusi dan Bukti Pengujian\n\n\\
=== AGRO-ECOLOGICAL SOIL DIELECTRIC & VWC SIMULATION ===
{
  "status": "PASS",
  "soil_constants": {
    "wilting_point_vwc": 0.12,
    "field_capacity_vwc": 0.28
  },
  "target_evaluation": {
    "eps_r": 18.4,
    "computed_vwc": 0.3249,
    "status": "FIELD_CAPACITY_OPTIMAL",
    "is_above_field_capacity": true
  },
  "simulation_series": [
    {
      "dielectric_eps_r": 4.2,
      "volumetric_water_content": 0.0603,
      "vwc_percentage": 6.03,
      "status": "PERMANENT_WILTING_POINT_STRESS",
      "sensitivity_dtheta_deps": 0.024808
    },
    {
      "dielectric_eps_r": 10.5,
      "volumetric_water_content": 0.1979,
      "vwc_percentage": 19.79,
      "status": "READILY_AVAILABLE_WATER",
      "sensitivity_dtheta_deps": 0.019072
    },
    {
      "dielectric_eps_r": 18.4,
      "volumetric_water_content": 0.3249,
      "vwc_percentage": 32.49,
      "status": "FIELD_CAPACITY_OPTIMAL",
      "sensitivity_dtheta_deps": 0.013327
    },
    {
      "dielectric_eps_r": 26.0,
      "volumetric_water_content": 0.41,
      "vwc_percentage": 41.0,
      "status": "FIELD_CAPACITY_OPTIMAL",
      "sensitivity_dtheta_deps": 0.00932
    },
    {
      "dielectric_eps_r": 35.2,
      "volumetric_water_content": 0.4809,
      "vwc_percentage": 48.09,
      "status": "SATURATED_ANOXIC_RISK",
      "sensitivity_dtheta_deps": 0.006464
    }
  ]
}

STATUS VERIFIKASI: 100% PASS (Model Topp & Sensitivitas Dielektrik Tervalidasi)\n\\
