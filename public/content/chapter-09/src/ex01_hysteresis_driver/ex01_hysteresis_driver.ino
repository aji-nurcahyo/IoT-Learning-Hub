// Chapter 09 — Kendali Aktuator Histeresis, Safety Interlock & Fail-Safe (Low-Voltage DC)
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)
// Framework: Arduino-ESP32 v3.x
// Wiring (Low-Voltage DC 3.3V / 5V Eksternal + Common GND):
//   - Input Analog (Simulasi suhu / NTC): GPIO 34 (ADC1_CH6)
//   - Interlock Pintu (Active-Low)      : GPIO 27 (INPUT_PULLUP -> Switch -> GND)
//   - Driver Kipas DC / MOSFET Gate     : GPIO 25 -> 220 ohm -> Gate (plus 10k pull-down ke GND)
//   - Indikator Buzzer Aktif 3.3V/Driver: GPIO 26

#include <Arduino.h>
#include <cmath>
#include <cstdint>

constexpr uint8_t TEMP_ADC_PIN   = 34;
constexpr uint8_t INTERLOCK_PIN  = 27; // LOW = pintu tertutup/aman; HIGH = pintu terbuka (interlock aktif)
constexpr uint8_t FAN_DRIVER_PIN = 25;
constexpr uint8_t ALARM_PIN      = 26;

constexpr float TEMP_HIGH_ON_C  = 30.0f;
constexpr float TEMP_LOW_OFF_C  = 28.0f;
constexpr uint32_t CTRL_PERIOD_MS = 500;

bool fanRunning = false;
uint32_t lastCtrlMs = 0;

// Konversi dummy linier 0..3300 mV -> 20..40 C untuk demo Wokwi dengan potensiometer
// serta deteksi fault di ujung ekstrim (< 100 mV atau > 3200 mV)
float readTemperatureC() {
  const uint32_t mv = analogReadMilliVolts(TEMP_ADC_PIN);
  if (mv < 100 || mv > 3200) {
    return NAN; // Indikasi putus kabel atau short sensor
  }
  return 20.0f + ((static_cast<float>(mv) - 100.0f) / 3100.0f) * 20.0f;
}

void setSafeShutdown(const char* reason) {
  fanRunning = false;
  ledcWrite(FAN_DRIVER_PIN, 0);
  digitalWrite(ALARM_PIN, HIGH);
  Serial.printf("[FAIL-SAFE] Kipas OFF, Alarm ON | Alasan: %s\n", reason);
}

void setup() {
  Serial.begin(115200);
  delay(200);

  pinMode(INTERLOCK_PIN, INPUT_PULLUP);
  pinMode(ALARM_PIN, OUTPUT);
  digitalWrite(ALARM_PIN, LOW);

  // PWM 5 kHz, 8-bit (0..255) untuk menggerakkan MOSFET kipas DC
  ledcAttach(FAN_DRIVER_PIN, 5000, 8);
  ledcWrite(FAN_DRIVER_PIN, 0); // Fail-safe default OFF saat boot

  analogReadResolution(12);
  analogSetPinAttenuation(TEMP_ADC_PIN, ADC_11db);

  Serial.println("=== CHAPTER 09: HYSTERESIS CONTROL + INTERLOCK + FAIL-SAFE ===");
}

void loop() {
  const uint32_t now = millis();
  if ((uint32_t)(now - lastCtrlMs) < CTRL_PERIOD_MS) {
    return;
  }
  lastCtrlMs = now;

  // 1. Cek Safety Interlock (misal tutup pelindung kipas terbuka)
  const bool interlockTripped = (digitalRead(INTERLOCK_PIN) == HIGH);
  if (interlockTripped) {
    setSafeShutdown("SAFETY_INTERLOCK_OPEN");
    return;
  }

  // 2. Baca sensor dan cek kondisi Fault (Fail-Safe)
  const float tempC = readTemperatureC();
  if (isnan(tempC)) {
    setSafeShutdown("SENSOR_FAULT_NAN");
    return;
  }

  // 3. Kontrol Histeresis (Deadband 28.0 .. 30.0 C)
  digitalWrite(ALARM_PIN, LOW);
  if (!fanRunning && tempC >= TEMP_HIGH_ON_C) {
    fanRunning = true;
  } else if (fanRunning && tempC <= TEMP_LOW_OFF_C) {
    fanRunning = false;
  }

  // Aktuasi PWM lembut (80% duty saat ON, 0% saat OFF)
  const uint8_t duty = fanRunning ? 204 : 0;
  ledcWrite(FAN_DRIVER_PIN, duty);

  char msg[96];
  snprintf(
      msg,
      sizeof(msg),
      "temp=%.2f C | fan=%s | duty=%u/255 | interlock=OK",
      tempC,
      fanRunning ? "ON" : "OFF",
      duty
  );
  Serial.println(msg);
}

