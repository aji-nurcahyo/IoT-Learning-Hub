// Chapter 06 — Contoh 2: External Interrupt (ISR) dengan IRAM_ATTR & Debounce Aman di loop()
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)
// Aturan penting ISR ESP32:
//   1. Pasang IRAM_ATTR agar handler selalu berada di RAM cepat.
//   2. Jangan memanggil Serial.print() atau delay() di dalam ISR!
//   3. Gunakan variabel volatile untuk flag komunikasi dari ISR ke loop().

#include <Arduino.h>
#include <cstdint>

constexpr uint8_t BUTTON_PIN = 27;
constexpr uint8_t LED_PIN    = 25;
constexpr uint32_t DEBOUNCE_MS = 50;

volatile bool irqTriggered = false;
volatile uint32_t irqTimeMs = 0;

bool ledState = false;
uint32_t lastHandledMs = 0;

void IRAM_ATTR onButtonFalling() {
  irqTimeMs = millis();
  irqTriggered = true;
}

void setup() {
  Serial.begin(115200);
  delay(200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), onButtonFalling, FALLING);
  Serial.println("=== CHAPTER 06: INTERRUPT FLAG + LOOP DEBOUNCE ===");
}

void loop() {
  if (irqTriggered) {
    noInterrupts();
    const uint32_t t = irqTimeMs;
    irqTriggered = false;
    interrupts();

    // Saring pantulan lanjutan dalam jendela lockout 50 ms
    if ((uint32_t)(t - lastHandledMs) >= DEBOUNCE_MS && digitalRead(BUTTON_PIN) == LOW) {
      lastHandledMs = t;
      ledState = !ledState;
      digitalWrite(LED_PIN, ledState ? HIGH : LOW);
      Serial.printf("[IRQ VALID] t=%lu ms -> LED=%s\n",
                    static_cast<unsigned long>(t),
                    ledState ? "HIGH" : "LOW");
    }
  }
}

