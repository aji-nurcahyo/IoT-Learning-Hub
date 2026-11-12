// Chapter 13 — ESP32 HTTP REST Client, JSON Serialization, Timeout & Status-Aware Retry
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)
// Menggunakan pustaka bawaan Arduino-ESP32: WiFi.h, HTTPClient.h, Preferences.h (tanpa library pihak ke-3)
// Konfigurasi runtime via Serial:
//   PROV:<ssid>,<pass>,<api_base_url>  contoh: PROV:LabWiFi,pass123,http://192.168.10.50:8000

#include <Arduino.h>
#include <HTTPClient.h>
#include <Preferences.h>
#include <WiFi.h>
#include <cstdint>

constexpr uint32_t HTTP_TIMEOUT_MS = 3000;
constexpr uint32_t SEND_PERIOD_MS  = 10000;
constexpr uint8_t  MAX_RETRY_5XX   = 2;

Preferences prefs;
char cfgSsid[33] = {0};
char cfgPass[65] = {0};
char cfgBaseUrl[128] = {0};
bool provisioned = false;

uint32_t lastSendMs = 0;
uint32_t seqNum = 0;

bool loadConfig() {
  prefs.begin("http_cfg", true);
  String s = prefs.getString("ssid", "");
  String p = prefs.getString("pass", "");
  String u = prefs.getString("url", "");
  prefs.end();
  if (s.length() == 0 || u.length() == 0) return false;
  snprintf(cfgSsid, sizeof(cfgSsid), "%s", s.c_str());
  snprintf(cfgPass, sizeof(cfgPass), "%s", p.c_str());
  snprintf(cfgBaseUrl, sizeof(cfgBaseUrl), "%s", u.c_str());
  return true;
}

bool shouldRetryHttp(int code) {
  // Timeout/transport error (< 0) atau 5xx server error layak di-retry terbatas;
  // 4xx (400 Bad Request, 401 Unauthorized, 404 Not Found) TIDAK boleh di-retry otomatis.
  return (code < 0) || (code >= 500 && code <= 599) || (code == 429);
}

bool postTelemetryWithRetry(const char* jsonBody) {
  char endpoint[160];
  snprintf(endpoint, sizeof(endpoint), "%s/api/v1/telemetry", cfgBaseUrl);

  for (uint8_t attempt = 0; attempt <= MAX_RETRY_5XX; ++attempt) {
    HTTPClient http;
    http.setTimeout(HTTP_TIMEOUT_MS);

    if (!http.begin(endpoint)) {
      Serial.println("[HTTP] Gagal inisialisasi URL endpoint.");
      return false;
    }
    http.addHeader("Content-Type", "application/json");
    http.addHeader("X-Device-Id", "esp32-node-01");

    const int code = http.POST(reinterpret_cast<uint8_t*>(const_cast<char*>(jsonBody)), strlen(jsonBody));
    if (code > 0) {
      const String resp = http.getString();
      Serial.printf("[HTTP] Attempt %u -> Status=%d Body=%s\n", attempt + 1, code, resp.c_str());
    } else {
      Serial.printf("[HTTP] Attempt %u -> Transport error=%d (%s)\n",
                    attempt + 1, code, HTTPClient::errorToString(code).c_str());
    }
    http.end();

    if (code >= 200 && code < 300) {
      return true;
    }
    if (!shouldRetryHttp(code)) {
      Serial.println("[HTTP] Client error 4xx — hentikan retry, perbaiki payload/endpoint.");
      return false;
    }
  }
  return false;
}

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("=== CHAPTER 13: HTTP REST CLIENT & JSON SERIALIZATION ===");

  provisioned = loadConfig();
  if (provisioned) {
    WiFi.mode(WIFI_STA);
    WiFi.begin(cfgSsid, cfgPass);
    Serial.printf("[WIFI] Menghubungkan ke '%s'...\n", cfgSsid);
  } else {
    Serial.println("[CFG] Belum ada konfigurasi. Simpan via NVS atau Serial PROV:<ssid>,<pass>,<url>");
  }
}

void loop() {
  const uint32_t now = millis();
  if (!provisioned || WiFi.status() != WL_CONNECTED) {
    return;
  }

  if ((uint32_t)(now - lastSendMs) >= SEND_PERIOD_MS) {
    lastSendMs = now;
    seqNum++;

    char payload[160];
    snprintf(
        payload,
        sizeof(payload),
        "{\"device_id\":\"esp32-node-01\",\"seq\":%lu,\"uptime_ms\":%lu,\"temp_c\":28.40,\"source\":\"synthetic\"}",
        static_cast<unsigned long>(seqNum),
        static_cast<unsigned long>(now)
    );
    postTelemetryWithRetry(payload);
  }
}

