# Hasil Eksekusi dan Bukti Pengujian\n\n\\
=== LIFE-SAFETY INTERLOCK & EMERGENCY EVACUATION SIMULATION ===
{
  "status": "PASS",
  "supervised_loop_tests": {
    "normal_condition": {
      "v_sense": 4.21,
      "status": "SUPERVISED_NORMAL",
      "alarm": false
    },
    "fire_alarm_condition": {
      "v_sense": 22.86,
      "status": "FIRE_ALARM_ACTIVE",
      "alarm": true
    },
    "open_fault_condition": {
      "v_sense": 0.02,
      "status": "OPEN_CIRCUIT_TROUBLE",
      "alarm": false
    }
  },
  "evacuation_routing": {
    "origin_node": "Room_302",
    "blocked_nodes_hazard": [
      "Stair_East"
    ],
    "optimal_safe_evacuation": {
      "destination_exit": "Exit_West",
      "evacuation_path": [
        "Room_302",
        "Hallway_Mid",
        "Stair_West",
        "Exit_West"
      ],
      "total_effective_cost": 87.0,
      "path_safe": true
    }
  },
  "life_safety_interlock": {
    "doors_fail_safe_unlocked": true,
    "air_handling_unit_fans_off": true,
    "response_time_ms": 45.0
  }
}

STATUS VERIFIKASI: 100% PASS (Model EOL & Rute Evakuasi Bebas Asap Tervalidasi)\n\\
