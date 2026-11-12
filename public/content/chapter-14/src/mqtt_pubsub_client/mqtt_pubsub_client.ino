// Chapter 14 — ESP32 MQTT Client (Publish/Subscribe) Non-Blocking dengan PubSubClient
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)
// Library Dependency: PubSubClient (by Nick O'Leary, v2.8+)
// Kredensial Wi-Fi & alamat Broker disimpan di NVS (Preferences) — tanpa password hardcoded!
// Perintah Serial: PROV:<ssid>,<pass>,<broker_ip>

#include <Arduino.h>
#include <Preferences.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <cstdint>

constexpr uint16_t MQTT_PORT       = 1883;
constexpr uint32_t TELEMETRY_MS    = 5000;
constexpr uint32_t RECONNECT_MS    = 3000;
constexpr uint8_t  ACTUATOR_LED    = 25;

const char* TOPIC_TELEMETRY = "lab/gh01/node-01/telemetry";
const char* TOPIC_CMD_WILD  = "lab/gh01/node-01/cmd/#";

Preferences prefs;
WiFiClient tcpClient;
PubSubClient mqtt(tcpClient);

char cfgSsid[33] = {0};
char cfgPass[65] = {0};
char cfgBroker[64] = {0};
bool configured = false;

uint32_t lastMqttRetryMs = 0;
uint32_t lastPublishMs = 0;
uint32_t seqNum = 0;

void onMqttMessage(char* topic, byte* payload, unsigned int length) {
  char msg[64];
  const size_t copyLen = (length < sizeof(msg) - 1) ? length : (sizeof(msg) - 1);
  memcpy(msg, payload, copyLen);
  msg[copyLen] = '\0';

  Serial.printf("[MQTT RX] topic=%s payload=%s\n", topic, msg);
  if (strcmp(topic, "lab/gh01/node-01/cmd/led") == 0) {
    if (strcmp(msg, "ON") == 0) {
      digitalWrite(ACTUATOR_LED, HIGH);
    } else if (strcmp(msg, "OFF") == 0) {
      digitalWrite(ACTUATOR_LED, LOW);
    }
  }
}

bool loadConfig() {
  prefs.begin("mqtt_cfg", true);
  String s = prefs.getString("ssid", "");
  String p = prefs.getString("pass", "");
  String b = prefs.getString("broker", "");
  prefs.end();
  if (s.length() == 0 || b.length() == 0) return false;
  snprintf(cfgSsid, sizeof(cfgSsid), "%s", s.c_str());
  snprintf(cfgPass, sizeof(cfgPass), "%s", p.c_str());
  snprintf(cfgBroker, sizeof(cfgBroker), "%s", b.c_str());
  return true;
}

void setup() {
  Serial.begin(115200);
  delay(200);
  pinMode(ACTUATOR_LED, OUTPUT);
  digitalWrite(ACTUATOR_LED, LOW);

  Serial.println("=== CHAPTER 14: MQTT PUBLISH/SUBSCRIBE CLIENT ===");
  configured = loadConfig();
  if (configured) {
    WiFi.mode(WIFI_STA);
    WiFi.begin(cfgSsid, cfgPass);
    mqtt.setServer(cfgBroker, MQTT_PORT);
    mqtt.setCallback(onMqttMessage);
    mqtt.setBufferSize(256);
    Serial.printf("[CFG] Target WiFi=%s Broker=%s:%u\n", cfgSsid, cfgBroker, MQTT_PORT);
  } else {
    Serial.println("[CFG] NVS kosong. Provisioning via NVS sebelum menjalankan di lapangan.");
  }
}

void loop() {
  const uint32_t now = millis();
  if (!configured || WiFi.status() != WL_CONNECTED) {
    return;
  }

  if (!mqtt.connected()) {
    if ((uint32_t)(now - lastMqttRetryMs) >= RECONNECT_MS) {
      lastMqttRetryMs = now;
      const char* clientId = "esp32-gh01-node01";
      if (mqtt.connect(clientId)) {
        Serial.println("[MQTT] Terhubung ke Broker.");
        mqtt.subscribe(TOPIC_CMD_WILD);
        Serial.printf("[MQTT] Subscribe: %s\n", TOPIC_CMD_WILD);
      } else {
        Serial.printf("[MQTT] Gagal konek (rc=%d), retry %lu ms.\n",
                      mqtt.state(), static_cast<unsigned long>(RECONNECT_MS));
      }
    }
    return;
  }

  // Wajib dipanggil rutin di loop() untuk memproses ping/keepalive & pesan masuk
  mqtt.loop();

  if ((uint32_t)(now - lastPublishMs) >= TELEMETRY_MS) {
    lastPublishMs = now;
    seqNum++;

    char jsonBuf[160];
    snprintf(
        jsonBuf,
        sizeof(jsonBuf),
        "{\"device_id\":\"esp32-gh01-node01\",\"seq\":%lu,\"temp_c\":28.75,\"source\":\"synthetic\"}",
        static_cast<unsigned long>(seqNum)
    );
    const bool ok = mqtt.publish(TOPIC_TELEMETRY, jsonBuf);
    Serial.printf("[MQTT TX] %s -> %s (%s)\n", TOPIC_TELEMETRY, jsonBuf, ok ? "OK" : "FAIL");
  }
}

