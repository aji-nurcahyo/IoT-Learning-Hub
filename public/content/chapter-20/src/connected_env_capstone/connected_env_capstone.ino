// Chapter 20 Capstone: Connected Environmental Monitoring System (ESP32)
// Fitur terintegrasi:
// 1. NVS Preferences untuk parameter lokal & fallback offline
// 2. Akuisisi ADC1 + Kontrol Histeresis Lokal (fail-safe tanpa bergantung jaringan)
// 3. Wi-Fi STA FSM + Full-Jitter Exponential Backoff (esp_random)
// 4. HTTP Client GET config dengan timeout & fallback ke NVS
// 5. SNTP UTC time sync + Ring Buffer statis (32 slot) + Batch Replay non-blocking
// 6. MQTT PubSubClient: JSON telemetry, Retained Status + LWT, & remote command

#include <Arduino.h>
#include <HTTPClient.h>
#include <Preferences.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <time.h>

#include "config.h"

struct TelemetryFrame {
  uint32_t seqId;
  uint64_t timestamp;
  bool timeSynced;
  float tempC;
  float tempHighC;
  bool relayOn;
};

struct DeviceConfig {
  char ssid[33];
  char pass[65];
  char brokerHost[64];
  uint16_t brokerPort;
  char configUrl[128];
  uint32_t sampleMs;
  float tempHighC;
  float tempHystC;
};

Preferences prefs;
WiFiClient tcpClient;
PubSubClient mqtt(tcpClient);
DeviceConfig cfg;

TelemetryFrame ringBuf[CAPSTONE_RING_CAPACITY];
size_t ringHead = 0;
size_t ringTail = 0;
size_t ringCount = 0;
uint32_t droppedOldest = 0;
uint32_t seqCounter = 0;

bool relayState = false;
bool httpConfigFetched = false;
unsigned long lastSampleMs = 0;
unsigned long nextWifiRetryMs = 0;
unsigned long nextMqttRetryMs = 0;
uint8_t wifiAttempts = 0;
uint8_t mqttAttempts = 0;

// Topik MQTT terstruktur
char topicTelemetry[64];
char topicStatus[64];
char topicCmd[64];

bool isTimeSynced() {
  time_t now = 0;
  time(&now);
  return now >= VALID_EPOCH_MIN;
}

unsigned long computeFullJitterMs(uint8_t attempt, unsigned long baseMs = 1000, unsigned long capMs = 60000) {
  uint8_t expVal = attempt > 6 ? 6 : attempt;
  unsigned long maxWait = baseMs << expVal;
  if (maxWait > capMs) {
    maxWait = capMs;
  }
  return esp_random() % (maxWait + 1);
}

void loadConfigFromNvs() {
  prefs.begin("capstone", true);
  String s = prefs.getString("ssid", DEFAULT_WIFI_SSID);
  String p = prefs.getString("pass", DEFAULT_WIFI_PASS);
  String b = prefs.getString("broker", DEFAULT_BROKER_HOST);
  String u = prefs.getString("cfgUrl", DEFAULT_HTTP_CONFIG_URL);

  strlcpy(cfg.ssid, s.c_str(), sizeof(cfg.ssid));
  strlcpy(cfg.pass, p.c_str(), sizeof(cfg.pass));
  strlcpy(cfg.brokerHost, b.c_str(), sizeof(cfg.brokerHost));
  strlcpy(cfg.configUrl, u.c_str(), sizeof(cfg.configUrl));

  cfg.brokerPort = prefs.getUShort("bPort", DEFAULT_BROKER_PORT);
  cfg.sampleMs = prefs.getULong("sampleMs", DEFAULT_SAMPLE_MS);
  cfg.tempHighC = prefs.getFloat("tempHigh", DEFAULT_TEMP_HIGH_C);
  cfg.tempHystC = prefs.getFloat("tempHyst", DEFAULT_TEMP_HYST_C);
  prefs.end();

  Serial.printf("[NVS] Loaded broker=%s:%u sampleMs=%lu tempHigh=%.2f C\n",
                cfg.brokerHost, cfg.brokerPort, static_cast<unsigned long>(cfg.sampleMs), cfg.tempHighC);
}

void saveRuntimeThresholdsToNvs() {
  prefs.begin("capstone", false);
  prefs.putULong("sampleMs", cfg.sampleMs);
  prefs.putFloat("tempHigh", cfg.tempHighC);
  prefs.end();
}

void pushRingFrame(const TelemetryFrame& f) {
  if (ringCount == CAPSTONE_RING_CAPACITY) {
    ringHead = (ringHead + 1) % CAPSTONE_RING_CAPACITY;
    ringCount--;
    droppedOldest++;
  }
  ringBuf[ringTail] = f;
  ringTail = (ringTail + 1) % CAPSTONE_RING_CAPACITY;
  ringCount++;
}

float readMappedTempC() {
  // Baca rata-rata 4 sampel ADC1 agar stabil; petakan 0..4095 -> 18.0..42.0 C
  uint32_t sum = 0;
  for (int i = 0; i < 4; i++) {
    sum += analogRead(PIN_TEMP_ADC);
  }
  float avgRaw = sum / 4.0f;
  return 18.0f + (avgRaw / 4095.0f) * 24.0f;
}

void updateLocalHysteresis(float tempC) {
  if (!relayState && tempC >= cfg.tempHighC) {
    relayState = true;
    Serial.printf("[CTRL] Local fail-safe ON (%.2f >= %.2f C)\n", tempC, cfg.tempHighC);
  } else if (relayState && tempC <= (cfg.tempHighC - cfg.tempHystC)) {
    relayState = false;
    Serial.printf("[CTRL] Local fail-safe OFF (%.2f <= %.2f C)\n", tempC, cfg.tempHighC - cfg.tempHystC);
  }
  digitalWrite(PIN_RELAY_FAN, relayState ? HIGH : LOW);
}

void syncHttpConfigOnce() {
  if (httpConfigFetched || WiFi.status() != WL_CONNECTED) {
    return;
  }
  HTTPClient http;
  http.setTimeout(2500);
  if (!http.begin(cfg.configUrl)) {
    Serial.println("[HTTP] http.begin() gagal, pakai config NVS.");
    httpConfigFetched = true;
    return;
  }
  int code = http.GET();
  if (code == HTTP_CODE_OK) {
    String body = http.getString();
    // Parser ringan tanpa alokasi berat untuk "temp_high_c"
    int idx = body.indexOf("\"temp_high_c\"");
    if (idx >= 0) {
      int colon = body.indexOf(':', idx);
      if (colon >= 0) {
        float val = body.substring(colon + 1).toFloat();
        if (val >= 15.0f && val <= 60.0f) {
          cfg.tempHighC = val;
          saveRuntimeThresholdsToNvs();
          Serial.printf("[HTTP] Config updated tempHighC=%.2f C\n", cfg.tempHighC);
        }
      }
    }
  } else {
    Serial.printf("[HTTP] GET %s gagal (code=%d), fallback NVS.\n", cfg.configUrl, code);
  }
  http.end();
  httpConfigFetched = true;
}

void onMqttMessage(char* topic, byte* payload, unsigned int length) {
  char msg[128];
  size_t copyLen = length < sizeof(msg) - 1 ? length : sizeof(msg) - 1;
  memcpy(msg, payload, copyLen);
  msg[copyLen] = '\0';

  Serial.printf("[MQTT RX] %s -> %s\n", topic, msg);
  if (strcmp(topic, topicCmd) == 0) {
    const char* keyPos = strstr(msg, "temp_high_c");
    if (keyPos != nullptr) {
      const char* colon = strchr(keyPos, ':');
      if (colon != nullptr) {
        float newVal = strtof(colon + 1, nullptr);
        if (newVal >= 15.0f && newVal <= 60.0f) {
          cfg.tempHighC = newVal;
          saveRuntimeThresholdsToNvs();
          Serial.printf("[CMD] Updated threshold tempHighC=%.2f C (saved to NVS)\n", cfg.tempHighC);
        } else {
          Serial.println("[CMD] Rejected out-of-range temp_high_c (valid: 15..60 C)");
        }
      }
    }
  }
}

bool publishFrameMqtt(const TelemetryFrame& f) {
  if (!mqtt.connected()) {
    return false;
  }
  char json[220];
  int len = snprintf(
    json,
    sizeof(json),
    "{\"dev\":\"%s\",\"seq\":%lu,\"ts\":%llu,\"synced\":%s,\"temp\":%.2f,\"th\":%.2f,\"relay\":%s,\"q\":%u,\"drop\":%lu}",
    DEVICE_ID,
    static_cast<unsigned long>(f.seqId),
    static_cast<unsigned long long>(f.timestamp),
    f.timeSynced ? "true" : "false",
    f.tempC,
    f.tempHighC,
    f.relayOn ? "true" : "false",
    static_cast<unsigned int>(ringCount),
    static_cast<unsigned long>(droppedOldest)
  );
  if (len <= 0 || len >= static_cast<int>(sizeof(json))) {
    return false;
  }
  return mqtt.publish(topicTelemetry, json);
}

void handleMqttReconnect(unsigned long nowMs) {
  if (mqtt.connected() || WiFi.status() != WL_CONNECTED) {
    return;
  }
  if (static_cast<long>(nowMs - nextMqttRetryMs) < 0) {
    return;
  }

  Serial.printf("[MQTT] Connecting to %s:%u ...\n", cfg.brokerHost, cfg.brokerPort);
  // Hubungkan dengan LWT retained "offline"
  bool ok = mqtt.connect(DEVICE_ID, nullptr, nullptr, topicStatus, 1, true, "offline");
  if (ok) {
    mqttAttempts = 0;
    mqtt.publish(topicStatus, "online", true);
    mqtt.subscribe(topicCmd, 1);
    Serial.println("[MQTT] Connected, retained status=online, subscribed to cmd");
  } else {
    unsigned long waitMs = computeFullJitterMs(mqttAttempts, 1000, 30000);
    if (mqttAttempts < 8) mqttAttempts++;
    nextMqttRetryMs = nowMs + waitMs;
    Serial.printf("[MQTT] Failed rc=%d, retry in %lu ms\n", mqtt.state(), waitMs);
  }
}

void setup() {
  Serial.begin(115200);
  delay(200);

  pinMode(PIN_RELAY_FAN, OUTPUT);
  pinMode(PIN_STATUS_LED, OUTPUT);
  pinMode(PIN_REPROV_BTN, INPUT_PULLUP);
  analogReadResolution(12);

  snprintf(topicTelemetry, sizeof(topicTelemetry), "iot/lab/%s/telemetry", DEVICE_ID);
  snprintf(topicStatus, sizeof(topicStatus), "iot/lab/%s/status", DEVICE_ID);
  snprintf(topicCmd, sizeof(topicCmd), "iot/lab/%s/cmd", DEVICE_ID);

  loadConfigFromNvs();

  WiFi.mode(WIFI_STA);
  WiFi.begin(cfg.ssid, cfg.pass);
  configTime(0, 0, NTP_SERVER_PRIMARY, NTP_SERVER_SECONDARY);

  mqtt.setServer(cfg.brokerHost, cfg.brokerPort);
  mqtt.setBufferSize(512);
  mqtt.setKeepAlive(30);
  mqtt.setCallback(onMqttMessage);
}

void loop() {
  unsigned long nowMs = millis();

  // 1. Akuisisi sensor + kontrol histeresis lokal (selalu berjalan walau jaringan mati!)
  if (static_cast<long>(nowMs - lastSampleMs) >= static_cast<long>(cfg.sampleMs)) {
    lastSampleMs = nowMs;
    float tempC = readMappedTempC();
    updateLocalHysteresis(tempC);

    time_t epochNow = 0;
    time(&epochNow);
    bool synced = isTimeSynced();

    TelemetryFrame frame;
    frame.seqId = ++seqCounter;
    frame.timestamp = synced ? static_cast<uint64_t>(epochNow) : static_cast<uint64_t>(nowMs);
    frame.timeSynced = synced;
    frame.tempC = tempC;
    frame.tempHighC = cfg.tempHighC;
    frame.relayOn = relayState;

    pushRingFrame(frame);
  }

  // 2. Kelola Wi-Fi STA dengan Full-Jitter Backoff
  if (WiFi.status() != WL_CONNECTED) {
    digitalWrite(PIN_STATUS_LED, LOW);
    if (static_cast<long>(nowMs - nextWifiRetryMs) >= 0) {
      unsigned long waitMs = computeFullJitterMs(wifiAttempts, 1000, 60000);
      if (wifiAttempts < 10) wifiAttempts++;
      nextWifiRetryMs = nowMs + waitMs;
      WiFi.reconnect();
    }
    return;
  }

  wifiAttempts = 0;
  digitalWrite(PIN_STATUS_LED, mqtt.connected() ? HIGH : LOW);

  // 3. Sinkronisasi konfigurasi HTTP sekali setelah Wi-Fi aktif
  syncHttpConfigOnce();

  // 4. Kelola koneksi & loop MQTT
  handleMqttReconnect(nowMs);
  mqtt.loop();

  // 5. Kuras ring buffer secara bertahap (non-blocking drain)
  size_t drained = 0;
  while (mqtt.connected() && ringCount > 0 && drained < CAPSTONE_MAX_DRAIN_PER_TICK) {
    if (!publishFrameMqtt(ringBuf[ringHead])) {
      break;
    }
    ringHead = (ringHead + 1) % CAPSTONE_RING_CAPACITY;
    ringCount--;
    drained++;
  }
}

