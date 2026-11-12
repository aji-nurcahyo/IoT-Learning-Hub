// Chapter 04 — Probe Identitas Chip & Uji GPIO Aman pada ESP32-DevKitC V4
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)
// Framework: Arduino-ESP32 (v3.x) atau v2.x
// Catatan: Firmware ini belum dikompilasi/diuji di environment server ini.

#include <Arduino.h>

constexpr uint8_t STATUS_LED_PIN = 25; // GPIO aman untuk output LED (+ resistor 220 ohm)
constexpr uint32_t SERIAL_BAUD = 115200;

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(200);

  pinMode(STATUS_LED_PIN, OUTPUT);
  digitalWrite(STATUS_LED_PIN, LOW);

  Serial.println("=== ESP32 BOARD PROBE (CHAPTER 04) ===");
  Serial.print("Chip Model      : ");
  Serial.println(ESP.getChipModel());
  Serial.print("Chip Revision   : ");
  Serial.println(ESP.getChipRevision());
  Serial.print("CPU Cores       : ");
  Serial.println(ESP.getChipCores());
  Serial.print("CPU Freq (MHz)  : ");
  Serial.println(ESP.getCpuFreqMHz());
  Serial.print("Flash Size (MB) : ");
  Serial.println(ESP.getFlashChipSize() / (1024.0 * 1024.0), 2);
  Serial.print("Free Heap (KiB) : ");
  Serial.println(ESP.getFreeHeap() / 1024.0, 1);
  Serial.println("Status LED Pin  : GPIO 25 (output LOW)");
}

void loop() {
  digitalWrite(STATUS_LED_PIN, HIGH);
  Serial.println("[HEARTBEAT] LED=HIGH");
  delay(1000);

  digitalWrite(STATUS_LED_PIN, LOW);
  Serial.println("[HEARTBEAT] LED=LOW");
  delay(1000);
}

