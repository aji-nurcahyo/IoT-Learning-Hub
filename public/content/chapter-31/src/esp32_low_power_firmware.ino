// Chapter 31: ESP32 Low-Power Deep Sleep & Wake-up Source
// Kompatibel dengan ESP32 Arduino Core dan Wokwi simulator

#include <Arduino.h>
#include "esp_sleep.h"

#define uS_TO_S_FACTOR 1000000ULL  // Konversi mikrodetik ke detik
#define TIME_TO_SLEEP  10          // Durasi deep sleep (10 detik)
#define WAKEUP_PIN     GPIO_NUM_33 // Pin eksternal wake-up RTC

RTC_DATA_ATTR int bootCount = 0;

void print_wakeup_reason() {
  esp_sleep_wakeup_cause_t wakeup_reason = esp_sleep_get_wakeup_cause();

  switch (wakeup_reason) {
    case ESP_SLEEP_WAKEUP_EXT0:
      Serial.println("[WAKEUP] Dipicu sinyal RTC_IO eksternal (EXT0)");
      break;
    case ESP_SLEEP_WAKEUP_TIMER:
      Serial.println("[WAKEUP] Dipicu timer internal RTC");
      break;
    default:
      Serial.printf("[WAKEUP] Boot normal atau penyebab lain: %d\n", wakeup_reason);
      break;
  }
}

void setup() {
  Serial.begin(115200);
  delay(100);

  ++bootCount;
  Serial.printf("\n--- SIKLUS BOOT KE-%d ---\n", bootCount);
  print_wakeup_reason();

  // Simulasi tugas aktif (pembacaan sensor dan transmisi)
  Serial.println("[ACTIVE] Menyalakan peripheral sensor...");
  delay(200); // Simulasi waktu akuisisi 200 ms
  Serial.println("[ACTIVE] Transmisi data telemetri selesai.");

  // Konfigurasi wake-up timer
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  Serial.printf("[SLEEP] ESP32 memasuki deep sleep selama %d detik...\n", TIME_TO_SLEEP);
  Serial.flush();

  // Masuk deep sleep
  esp_deep_sleep_start();
}

void loop() {
  // Loop tidak akan pernah dieksekusi dalam mode deep sleep
}
