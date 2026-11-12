#pragma once

#include <Arduino.h>

// Pemetaan Pin ESP32 (aman terhadap Wi-Fi & strapping pins)
constexpr int PIN_TEMP_ADC = 34;     // ADC1_CH6 (input only, aman saat Wi-Fi aktif)
constexpr int PIN_RELAY_FAN = 26;    // Aktuator kipas / indikator relay lokal
constexpr int PIN_STATUS_LED = 2;    // LED status konektivitas
constexpr int PIN_REPROV_BTN = 27;   // Tombol reset/re-sync konfigurasi lokal (INPUT_PULLUP)

// Konfigurasi default NVS & Fallback Lokal
constexpr const char* DEFAULT_WIFI_SSID = "Wokwi-GUEST";
constexpr const char* DEFAULT_WIFI_PASS = "";
constexpr const char* DEFAULT_BROKER_HOST = "192.168.1.10";
constexpr uint16_t DEFAULT_BROKER_PORT = 1883;
constexpr const char* DEFAULT_HTTP_CONFIG_URL = "http://192.168.1.10:8080/api/v1/config/node-01";
constexpr const char* DEVICE_ID = "node-01";

constexpr uint32_t DEFAULT_SAMPLE_MS = 5000;
constexpr float DEFAULT_TEMP_HIGH_C = 30.0f;
constexpr float DEFAULT_TEMP_HYST_C = 1.5f;

// Kapasitas Offline Ring Buffer & Batas Drain
constexpr size_t CAPSTONE_RING_CAPACITY = 32;
constexpr size_t CAPSTONE_MAX_DRAIN_PER_TICK = 4;

// Parameter SNTP
constexpr const char* NTP_SERVER_PRIMARY = "pool.ntp.org";
constexpr const char* NTP_SERVER_SECONDARY = "time.google.com";
constexpr time_t VALID_EPOCH_MIN = 1704067200; // 2024-01-01T00:00:00Z

