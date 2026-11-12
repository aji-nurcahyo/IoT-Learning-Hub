// Chapter 10 Capstone — Header Konfigurasi & Parameter Sistem
#ifndef ENV_CONFIG_H
#define ENV_CONFIG_H

#include <cstdint>

// Pin Mapping untuk ESP32-DevKitC V4 (WROOM-32)
constexpr uint8_t PIN_NTC_ADC      = 34; // ADC1_CH6 (input-only, aman Wi-Fi)
constexpr uint8_t PIN_MODE_BUTTON  = 27; // INPUT_PULLUP, active-low
constexpr uint8_t PIN_INTERLOCK    = 14; // INPUT_PULLUP, LOW=aman, HIGH=terbuka
constexpr uint8_t PIN_FAN_PWM      = 25; // LEDC PWM ke MOSFET gate / LED beban
constexpr uint8_t PIN_STATUS_LED   = 26; // LED status sistem
constexpr uint8_t PIN_ALARM_BUZZER = 18; // Buzzer aktif / indikator fault

// Parameter Akuisisi & Kalibrasi NTC (10k @ 25C, Beta 3950)
constexpr float V_SUPPLY_MV   = 3300.0f;
constexpr float R_FIXED_OHM   = 10000.0f;
constexpr float NTC_R25_OHM   = 10000.0f;
constexpr float NTC_BETA_K    = 3950.0f;
constexpr float T25_KELVIN    = 298.15f;
constexpr float CAL_SLOPE     = 1.0381f;
constexpr float CAL_OFFSET    = -1.4740f;
constexpr uint16_t ADC_MIN_MV = 100;
constexpr uint16_t ADC_MAX_MV = 3200;

// Konfigurasi Timing Non-Blocking (ms)
constexpr uint32_t SAMPLE_INTERVAL_MS    = 100;
constexpr uint32_t DEBOUNCE_MS           = 50;
constexpr uint32_t TELEMETRY_INTERVAL_MS = 1000;
constexpr uint8_t  MOVING_AVG_N          = 8;

// Parameter Kontrol Histeresis (C)
constexpr float NORMAL_T_HIGH_C = 30.0f;
constexpr float NORMAL_T_LOW_C  = 28.0f;
constexpr float STRICT_T_HIGH_C = 27.0f;
constexpr float STRICT_T_LOW_C  = 25.0f;
constexpr float EMERGENCY_T_C   = 45.0f;

// PWM LEDC
constexpr uint32_t FAN_PWM_FREQ_HZ = 5000;
constexpr uint8_t  FAN_PWM_RES     = 8;
constexpr uint8_t  FAN_DUTY_ON     = 204; // ~80%

enum class ControlMode : uint8_t {
  AUTO_NORMAL = 0,
  AUTO_STRICT = 1,
  MANUAL_ON   = 2,
  FAULT_SAFE  = 3
};

#endif // ENV_CONFIG_H

