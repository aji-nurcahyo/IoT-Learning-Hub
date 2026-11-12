// Chapter 07 — Pembacaan ADC1 dengan Moving Average & Pengaturan Kecerahan LED via PWM (LEDC)
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)
// Framework: Arduino-ESP32 v3.x (API ledcAttach(pin, freq, resolution))
// Wiring:
//   - Potensiometer 10 kOhm : ujung ke 3V3 dan GND, wiper tengah ke GPIO 34 (ADC1_CH6)
//   - LED                   : GPIO 25 -> Resistor 220 ohm -> Anoda LED -> Katoda -> GND

#include <Arduino.h>
#include <cstdint>

constexpr uint8_t ADC_POT_PIN   = 34; // ADC1_CH6 (aman dipakai bersamaan dengan Wi-Fi)
constexpr uint8_t PWM_LED_PIN   = 25;
constexpr uint32_t PWM_FREQ_HZ  = 5000;
constexpr uint8_t PWM_RES_BITS  = 10;   // Rentang 0..1023
constexpr uint16_t PWM_MAX_DUTY = (1u << PWM_RES_BITS) - 1u;

constexpr uint8_t AVG_WINDOW = 8;
constexpr uint32_t SAMPLE_MS = 50;

uint32_t mvBuffer[AVG_WINDOW] = {0};
uint8_t bufIdx = 0;
uint32_t bufSum = 0;
uint8_t sampleCount = 0;
uint32_t lastSampleMs = 0;
uint32_t lastPrintMs = 0;

void setup() {
  Serial.begin(115200);
  delay(200);

  // Set atenuasi ADC ke 11 dB (rentang efektif ~150 mV..3100 mV pada ESP32)
  analogReadResolution(12);
  analogSetPinAttenuation(ADC_POT_PIN, ADC_11db);

  // Konfigurasi PWM hardware LEDC (API Arduino-ESP32 v3.x)
  ledcAttach(PWM_LED_PIN, PWM_FREQ_HZ, PWM_RES_BITS);
  ledcWrite(PWM_LED_PIN, 0);

  Serial.println("=== CHAPTER 07: ADC1 MOVING AVERAGE + LEDC PWM ===");
}

void loop() {
  const uint32_t now = millis();

  if ((uint32_t)(now - lastSampleMs) >= SAMPLE_MS) {
    lastSampleMs = now;

    // analogReadMilliVolts() menggunakan kurva kalibrasi eFuse pabrik bila tersedia
    const uint32_t mv = analogReadMilliVolts(ADC_POT_PIN);

    bufSum -= mvBuffer[bufIdx];
    mvBuffer[bufIdx] = mv;
    bufSum += mv;
    bufIdx = (bufIdx + 1) % AVG_WINDOW;
    if (sampleCount < AVG_WINDOW) {
      sampleCount++;
    }

    const uint32_t avgMv = bufSum / sampleCount;
    // Peta 0..3300 mV ke 0..1023 duty cycle
    uint32_t clampedMv = (avgMv > 3300u) ? 3300u : avgMv;
    uint16_t duty = static_cast<uint16_t>((clampedMv * PWM_MAX_DUTY) / 3300u);
    ledcWrite(PWM_LED_PIN, duty);

    if ((uint32_t)(now - lastPrintMs) >= 250) {
      lastPrintMs = now;
      const float dutyPct = (static_cast<float>(duty) / PWM_MAX_DUTY) * 100.0f;
      char msg[96];
      snprintf(
          msg,
          sizeof(msg),
          "raw_mv=%lu avg_mv=%lu duty=%u/%u (%.1f%%)",
          static_cast<unsigned long>(mv),
          static_cast<unsigned long>(avgMv),
          duty,
          PWM_MAX_DUTY,
          dutyPct
      );
      Serial.println(msg);
    }
  }
}

