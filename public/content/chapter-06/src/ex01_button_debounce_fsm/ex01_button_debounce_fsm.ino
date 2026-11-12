// Chapter 06 — Button-Controlled LED dengan Software Debouncing, Edge Detection & FSM
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)
// Wiring:
//   - Tombol: GPIO 27 <-> Push Button <-> GND (pakai internal INPUT_PULLUP, active-low)
//   - LED   : GPIO 25 -> Resistor 220 ohm -> Anoda LED -> Katoda -> GND

#include <Arduino.h>
#include <cstdint>

constexpr uint8_t BUTTON_PIN = 27; // Mendukung internal INPUT_PULLUP (bukan GPIO 34..39!)
constexpr uint8_t LED_PIN    = 25;
constexpr uint32_t DEBOUNCE_MS = 50;
constexpr uint32_t BLINK_MS    = 250;

enum class LedMode : uint8_t {
  OFF = 0,
  ON = 1,
  BLINK = 2
};

LedMode currentMode = LedMode::OFF;
bool lastRawReading = HIGH;
bool stableButtonState = HIGH;
uint32_t lastBounceMs = 0;

uint32_t lastBlinkMs = 0;
bool blinkOutput = false;
uint32_t pressCount = 0;

const char* modeName(LedMode m) {
  switch (m) {
    case LedMode::OFF:   return "OFF";
    case LedMode::ON:    return "ON";
    case LedMode::BLINK: return "BLINK";
    default:             return "OFF";
  }
}

void applyLedMode(uint32_t nowMs) {
  switch (currentMode) {
    case LedMode::OFF:
      digitalWrite(LED_PIN, LOW);
      break;
    case LedMode::ON:
      digitalWrite(LED_PIN, HIGH);
      break;
    case LedMode::BLINK:
      if ((uint32_t)(nowMs - lastBlinkMs) >= BLINK_MS) {
        lastBlinkMs = nowMs;
        blinkOutput = !blinkOutput;
        digitalWrite(LED_PIN, blinkOutput ? HIGH : LOW);
      }
      break;
  }
}

void setup() {
  Serial.begin(115200);
  delay(200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.println("=== CHAPTER 06: DEBOUNCE + EDGE DETECT + LED FSM ===");
  Serial.println("Mode awal: OFF (tekan tombol di GPIO 27 untuk beralih mode)");
}

void loop() {
  const uint32_t now = millis();
  const bool raw = digitalRead(BUTTON_PIN);

  // Reset timer stabilitas setiap kali sinyal mentah berubah (pantulan / bounce)
  if (raw != lastRawReading) {
    lastBounceMs = now;
    lastRawReading = raw;
  }

  // Terima transisi hanya jika sinyal bertahan konstan >= DEBOUNCE_MS
  if ((uint32_t)(now - lastBounceMs) >= DEBOUNCE_MS && raw != stableButtonState) {
    stableButtonState = raw;

    // Falling-edge detection: HIGH -> LOW (active-low button pressed)
    if (stableButtonState == LOW) {
      pressCount++;
      if (currentMode == LedMode::OFF) {
        currentMode = LedMode::ON;
      } else if (currentMode == LedMode::ON) {
        currentMode = LedMode::BLINK;
        lastBlinkMs = now;
        blinkOutput = true;
      } else {
        currentMode = LedMode::OFF;
      }

      char msg[80];
      snprintf(
          msg,
          sizeof(msg),
          "[PRESS #%lu] t=%lu ms -> LED Mode = %s",
          static_cast<unsigned long>(pressCount),
          static_cast<unsigned long>(now),
          modeName(currentMode)
      );
      Serial.println(msg);
    }
  }

  applyLedMode(now);
}

