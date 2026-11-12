// Chapter 05 — Contoh 2: Firmware Non-Blocking dengan Header Modular & State Machine Dasar
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)
// Catatan: Contoh ini mensimulasikan perubahan nilai di firmware untuk fokus ke alur FSM & millis().

#include <Arduino.h>
#include <cstdint>
#include "led_timer.h"

constexpr uint8_t STATUS_LED_PIN = 25;
constexpr uint8_t ALERT_LED_PIN  = 26;
constexpr uint32_t SAMPLE_PERIOD_MS = 1000;
constexpr float ALERT_THRESHOLD_C   = 30.0f;

enum class SystemState : uint8_t {
  IDLE = 0,
  SAMPLE = 1,
  ALERT = 2
};

BlinkTask statusBlink;
BlinkTask alertBlink;
SystemState currentState = SystemState::IDLE;
uint32_t lastSampleMs = 0;
uint32_t sampleSeq = 0;
float simulatedTempC = 27.5f;

const char* stateToName(SystemState st) {
  switch (st) {
    case SystemState::IDLE:   return "IDLE";
    case SystemState::SAMPLE: return "SAMPLE";
    case SystemState::ALERT:  return "ALERT";
    default:                  return "UNKNOWN";
  }
}

void setup() {
  Serial.begin(115200);
  delay(200);
  initBlinkTask(statusBlink, STATUS_LED_PIN, 1000);
  initBlinkTask(alertBlink, ALERT_LED_PIN, 200);
  lastSampleMs = millis();
  Serial.println("=== CHAPTER 05: NON-BLOCKING FSM STARTED ===");
}

void loop() {
  const uint32_t now = millis();

  // Task 1: LED heartbeat selalu responsif setiap 1000 ms
  updateBlinkTask(statusBlink, now);

  // Task 2: Evaluasi State Machine
  switch (currentState) {
    case SystemState::IDLE:
      digitalWrite(ALERT_LED_PIN, LOW);
      if ((uint32_t)(now - lastSampleMs) >= SAMPLE_PERIOD_MS) {
        lastSampleMs = now;
        currentState = SystemState::SAMPLE;
      }
      break;

    case SystemState::SAMPLE: {
      sampleSeq++;
      // Simulasi internal deterministik (bukan bacaan sensor fisik)
      simulatedTempC += 0.9f;
      if (simulatedTempC > 32.5f) {
        simulatedTempC = 27.0f;
      }

      char logBuf[96];
      snprintf(
          logBuf,
          sizeof(logBuf),
          "[SEQ %lu] state=%s sim_temp=%.1f C",
          static_cast<unsigned long>(sampleSeq),
          stateToName(currentState),
          simulatedTempC
      );
      Serial.println(logBuf);

      currentState = (simulatedTempC >= ALERT_THRESHOLD_C)
                         ? SystemState::ALERT
                         : SystemState::IDLE;
      break;
    }

    case SystemState::ALERT:
      updateBlinkTask(alertBlink, now);
      if ((uint32_t)(now - lastSampleMs) >= SAMPLE_PERIOD_MS) {
        lastSampleMs = now;
        currentState = SystemState::SAMPLE;
      }
      break;
  }
}

