// Chapter 12 — ESP32 Wi-Fi Station, Device Provisioning (NVS Preferences) & Exponential Backoff
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)
// Keamanan: Kredensial TIDAK ditanam di source code; dimasukkan saat runtime lewat Serial:
//   Format perintah Serial Monitor: PROV:<ssid>,<password>
//   Hapus kredensial / factory reset: WIPE

#include <Arduino.h>
#include <Preferences.h>
#include <WiFi.h>
#include <cstdint>

constexpr uint8_t STATUS_LED_PIN  = 25;
constexpr uint8_t WIPE_BTN_PIN    = 27; // Tekan saat boot / runtime untuk hapus kredensial NVS
constexpr uint32_t CONNECT_TIMEOUT_MS = 10000;
constexpr uint32_t BACKOFF_MIN_MS     = 1000;
constexpr uint32_t BACKOFF_MAX_MS     = 60000;

enum class WifiState : uint8_t {
  PROVISIONING = 0,
  CONNECTING   = 1,
  CONNECTED    = 2,
  BACKOFF_WAIT = 3
};

Preferences prefs;
WifiState wifiState = WifiState::PROVISIONING;
char savedSsid[33] = {0};
char savedPass[65] = {0};

uint32_t stateEnterMs = 0;
uint32_t backoffMs = BACKOFF_MIN_MS;
uint32_t lastDiagMs = 0;
uint32_t lastLedMs = 0;
bool ledOn = false;
char serialBuf[120];
size_t serialLen = 0;

bool loadCredentials() {
  prefs.begin("wifi_cfg", true);
  String s = prefs.getString("ssid", "");
  String p = prefs.getString("pass", "");
  prefs.end();

  if (s.length() == 0 || s.length() > 32 || p.length() > 64) {
    return false;
  }
  snprintf(savedSsid, sizeof(savedSsid), "%s", s.c_str());
  snprintf(savedPass, sizeof(savedPass), "%s", p.c_str());
  return true;
}

void saveCredentials(const char* ssid, const char* pass) {
  prefs.begin("wifi_cfg", false);
  prefs.putString("ssid", ssid);
  prefs.putString("pass", pass);
  prefs.end();
  snprintf(savedSsid, sizeof(savedSsid), "%s", ssid);
  snprintf(savedPass, sizeof(savedPass), "%s", pass);
}

void wipeCredentials() {
  prefs.begin("wifi_cfg", false);
  prefs.clear();
  prefs.end();
  savedSsid[0] = '\0';
  savedPass[0] = '\0';
  WiFi.disconnect(true, true);
  wifiState = WifiState::PROVISIONING;
  Serial.println("[PROV] Kredensial NVS dihapus. Kirim PROV:<ssid>,<password> lewat Serial.");
}

void startConnecting(uint32_t now) {
  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(false); // Kendali backoff ditangani eksplisit oleh FSM
  WiFi.begin(savedSsid, savedPass);
  wifiState = WifiState::CONNECTING;
  stateEnterMs = now;
  Serial.printf("[WIFI] Menghubungkan ke SSID '%s' (timeout=%lu ms)...\n",
                savedSsid, static_cast<unsigned long>(CONNECT_TIMEOUT_MS));
}

void processSerialProvisioning(uint32_t now) {
  while (Serial.available() > 0) {
    char c = static_cast<char>(Serial.read());
    if (c == '\r') continue;
    if (c == '\n') {
      serialBuf[serialLen] = '\0';
      if (strcmp(serialBuf, "WIPE") == 0) {
        wipeCredentials();
      } else if (strncmp(serialBuf, "PROV:", 5) == 0) {
        char* comma = strchr(serialBuf + 5, ',');
        if (comma != nullptr && comma != (serialBuf + 5)) {
          *comma = '\0';
          const char* ssid = serialBuf + 5;
          const char* pass = comma + 1;
          saveCredentials(ssid, pass);
          backoffMs = BACKOFF_MIN_MS;
          Serial.printf("[PROV] Kredensial disimpan ke NVS (SSID=%s, pass=REDACTED).\n", ssid);
          startConnecting(now);
        } else {
          Serial.println("[PROV] Format salah. Gunakan: PROV:<ssid>,<password>");
        }
      }
      serialLen = 0;
    } else if (serialLen < sizeof(serialBuf) - 1) {
      serialBuf[serialLen++] = c;
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(200);

  pinMode(STATUS_LED_PIN, OUTPUT);
  pinMode(WIPE_BTN_PIN, INPUT_PULLUP);
  digitalWrite(STATUS_LED_PIN, LOW);

  Serial.println("=== CHAPTER 12: WI-FI STA + NVS PROVISIONING + BACKOFF ===");
  if (digitalRead(WIPE_BTN_PIN) == LOW) {
    wipeCredentials();
  } else if (loadCredentials()) {
    startConnecting(millis());
  } else {
    wifiState = WifiState::PROVISIONING;
    Serial.println("[PROV] Belum ada kredensial di NVS. Kirim: PROV:<ssid>,<password>");
  }
}

void loop() {
  const uint32_t now = millis();
  processSerialProvisioning(now);

  switch (wifiState) {
    case WifiState::PROVISIONING:
      if ((uint32_t)(now - lastLedMs) >= 150) {
        lastLedMs = now;
        ledOn = !ledOn;
        digitalWrite(STATUS_LED_PIN, ledOn ? HIGH : LOW);
      }
      break;

    case WifiState::CONNECTING:
      if (WiFi.status() == WL_CONNECTED) {
        wifiState = WifiState::CONNECTED;
        backoffMs = BACKOFF_MIN_MS;
        digitalWrite(STATUS_LED_PIN, HIGH);
        Serial.printf("[WIFI] CONNECTED | IP=%s | GW=%s | RSSI=%d dBm\n",
                      WiFi.localIP().toString().c_str(),
                      WiFi.gatewayIP().toString().c_str(),
                      WiFi.RSSI());
      } else if ((uint32_t)(now - stateEnterMs) >= CONNECT_TIMEOUT_MS) {
        WiFi.disconnect(true);
        wifiState = WifiState::BACKOFF_WAIT;
        stateEnterMs = now;
        Serial.printf("[WIFI] Timeout! Menunggu backoff %lu ms sebelum retry.\n",
                      static_cast<unsigned long>(backoffMs));
      }
      break;

    case WifiState::CONNECTED:
      if (WiFi.status() != WL_CONNECTED) {
        wifiState = WifiState::BACKOFF_WAIT;
        stateEnterMs = now;
        digitalWrite(STATUS_LED_PIN, LOW);
        Serial.printf("[WIFI] Koneksi terputus! Menunggu backoff %lu ms.\n",
                      static_cast<unsigned long>(backoffMs));
      } else if ((uint32_t)(now - lastDiagMs) >= 5000) {
        lastDiagMs = now;
        Serial.printf("[DIAG] RSSI=%d dBm | Channel=%d\n", WiFi.RSSI(), WiFi.channel());
      }
      break;

    case WifiState::BACKOFF_WAIT:
      if ((uint32_t)(now - stateEnterMs) >= backoffMs) {
        backoffMs = (backoffMs * 2 <= BACKOFF_MAX_MS) ? (backoffMs * 2) : BACKOFF_MAX_MS;
        startConnecting(now);
      }
      break;
  }
}

