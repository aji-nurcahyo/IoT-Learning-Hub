// Chapter 05 — Contoh 1: Tipe Data Fixed-Width, Operator, dan Serial Debugging
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)

#include <Arduino.h>
#include <cstdint>

constexpr uint32_t SERIAL_BAUD = 115200;

float hitungDayaMilliwatt(float teganganVolt, float arusMilliamp) {
  return teganganVolt * arusMilliamp;
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(200);

  uint16_t rawSample = 2048;         // 0..4095 (12-bit)
  const float vRef = 3.30f;          // konstanta di Flash / rodata
  bool sensorReady = true;

  float voltage = (static_cast<float>(rawSample) / 4095.0f) * vRef;
  float powerMw = hitungDayaMilliwatt(voltage, 5.5f);

  // Buffer char statis di stack (menghindari fragmentasi heap oleh kelas String)
  char msg[96];
  snprintf(
      msg,
      sizeof(msg),
      "ready=%s raw=%u voltage=%.3f V power=%.2f mW",
      sensorReady ? "true" : "false",
      rawSample,
      voltage,
      powerMw
  );
  Serial.println(msg);
}

void loop() {
  // Tidak ada tugas berulang pada contoh dasar ini.
}

