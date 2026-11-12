// Chapter 08 — Akuisisi Sensor NTC 10k, Kalibrasi Dua Titik & Statistik Sampel
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)
// Wiring (Divider 3.3V -> R_fixed 10k -> GPIO 34 -> NTC 10k -> GND):
//   - R_fixed = 10,000 ohm (toleransi 1%), NTC = 10,000 ohm @ 25 C (Beta = 3950 K)
//   - Pin ADC1_CH6 = GPIO 34 (aman dipakai bersamaan dengan Wi-Fi)

#include <Arduino.h>
#include <cmath>
#include <cstdint>

constexpr uint8_t NTC_ADC_PIN = 34;
constexpr float V_SUPPLY_MV   = 3300.0f;
constexpr float R_FIXED_OHM   = 10000.0f;
constexpr float NTC_R25_OHM   = 10000.0f;
constexpr float NTC_BETA_K    = 3950.0f;
constexpr float T25_KELVIN    = 298.15f;

// Parameter kalibrasi dua titik hasil pencocokan terhadap termometer referensi (contoh)
constexpr float CAL_SLOPE  = 1.0381f;
constexpr float CAL_OFFSET = -1.474f;

constexpr uint8_t NUM_SAMPLES = 10;

float readRawNtcCelsius() {
  const float vMv = static_cast<float>(analogReadMilliVolts(NTC_ADC_PIN));
  if (vMv <= 50.0f || vMv >= (V_SUPPLY_MV - 50.0f)) {
    // Deteksi kemungkinan open-circuit atau short-circuit pada rangkaian divider
    return NAN;
  }
  // R_ntc = R_fixed * V_ntc / (V_supply - V_ntc)
  const float rNtc = R_FIXED_OHM * (vMv / (V_SUPPLY_MV - vMv));
  const float invT = (1.0f / T25_KELVIN) + (1.0f / NTC_BETA_K) * logf(rNtc / NTC_R25_OHM);
  return (1.0f / invT) - 273.15f;
}

void setup() {
  Serial.begin(115200);
  delay(200);
  analogReadResolution(12);
  analogSetPinAttenuation(NTC_ADC_PIN, ADC_11db);
  Serial.println("=== CHAPTER 08: NTC SENSOR ACQUISITION & TWO-POINT CALIBRATION ===");
}

void loop() {
  float samples[NUM_SAMPLES];
  uint8_t valid = 0;

  for (uint8_t i = 0; i < NUM_SAMPLES; ++i) {
    const float t = readRawNtcCelsius();
    if (!isnan(t)) {
      samples[valid++] = t;
    }
    delay(20); // jeda singkat antar-konversi sampel burst
  }

  if (valid < 2) {
    Serial.println("[FAULT] Sensor NTC open/short circuit terdeteksi!");
    delay(1000);
    return;
  }

  float sum = 0.0f;
  for (uint8_t i = 0; i < valid; ++i) sum += samples[i];
  const float meanRaw = sum / valid;

  float sqDiff = 0.0f;
  for (uint8_t i = 0; i < valid; ++i) {
    const float d = samples[i] - meanRaw;
    sqDiff += d * d;
  }
  const float stdDev = sqrtf(sqDiff / (valid - 1));
  const float uA = stdDev / sqrtf(static_cast<float>(valid));
  const float tempCal = (CAL_SLOPE * meanRaw) + CAL_OFFSET;

  char msg[112];
  snprintf(
      msg,
      sizeof(msg),
      "n=%u raw_mean=%.2f C cal_temp=%.2f C s=%.3f C uA=%.3f C",
      valid,
      meanRaw,
      tempCal,
      stdDev,
      uA
  );
  Serial.println(msg);
  delay(1000);
}

