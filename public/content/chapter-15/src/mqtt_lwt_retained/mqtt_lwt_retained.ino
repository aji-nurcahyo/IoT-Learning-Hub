// Chapter 15 — MQTT Last Will (LWT), Retained Status, Keepalive & Deduplikasi Seq
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)
// Library Dependency: PubSubClient (v2.8+)
// Catatan: PubSubClient mendukung LWT (willTopic/QoS/Retain), subscribe QoS 0/1,
//          dan publish retain=true (QoS 0). Untuk publish QoS 1/2 & MQTT 5.0 penuh,
//          gunakan ESP-IDF esp-mqtt.

#include <Arduino.h>
#include <Preferences.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <cstdint>

constexpr uint16_t MQTT_PORT         = 1883;
constexpr uint16_t MQTT_KEEPALIVE_S  = 30; // LWT terpicu jika senyap > 45 s (1.5x)
constexpr uint32_t TELEMETRY_MS      = 5000;
constexpr uint32_t RECONNECT_MS      = 4000;

const char* CLIENT_ID      = "esp32-gh01-node01";
const char* TOPIC_STATUS   = "lab/gh01/node-01/status";
const char* TOPIC_DATA     = "lab/gh01/node-01/telemetry";
const char* TOPIC_CMD      = "lab/gh01/node-01/cmd";

Preferences prefs;
WiFiClient tcpClient;
PubSubClient mqtt(tcpClient);

char cfgSsid[33] = {0};
char cfgPass[65] = {0};
char cfgBroker[64] = {0};
bool configured = false;

uint32_t lastRetryMs = 0;
uint32_t lastPubMs = 0;
uint32_t seqNum = 0;
uint32_t lastHandledCmdSeq = 0;

void onMqttMessage(char* topic, byte* payload, unsigned int length) {
  char buf[96];
  const size_t n = (length < sizeof(buf) - 1) ? length : (sizeof(buf) - 1);
  memcpy(buf, payload, n);
  buf[n] = '\0';

  // Contoh idempotensi sederhana: abaikan perintah jika format "cmd_seq:<n>:..." berulang
  unsigned long cmdSeq = 0;
  if (sscanf(buf, "cmd_seq:%lu", &cmdSeq) == 1) {
    if (cmdSeq <= lastHandledCmdSeq) {
      Serial.printf("[MQTT RX] Duplikat perintah seq=%lu diabaikan (idempoten).\n", cmdSeq);
      return;
    }
    lastHandledCmdSeq = static_cast<uint32_t>(cmdSeq);
  }
  Serial.printf("[MQTT RX] topic=%s msg=%s\n", topic, buf);
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
  Serial.println("=== CHAPTER 15: MQTT LWT, RETAINED & KEEPALIVE ===");

  configured = loadConfig();
  if (configured) {
    WiFi.mode(WIFI_STA);
    WiFi.begin(cfgSsid, cfgPass);
    mqtt.setServer(cfgBroker, MQTT_PORT);
    mqtt.setKeepAlive(MQTT_KEEPALIVE_S);
    mqtt.setCallback(onMqttMessage);
    mqtt.setBufferSize(256);
  }
}

void loop() {
  const uint32_t now = millis();
  if (!configured || WiFi.status() != WL_CONNECTED) return;

  if (!mqtt.connected()) {
    if ((uint32_t)(now - lastRetryMs) >= RECONNECT_MS) {
      lastRetryMs = now;
      // Parameter connect: (id, user, pass, willTopic, willQoS, willRetain, willMessage, cleanSession)
      const bool ok = mqtt.connect(
          CLIENT_ID,
          nullptr,
          nullptr,
          TOPIC_STATUS,
          1,      // willQoS = 1
          true,   // willRetain = true
          "{\"state\":\"offline\",\"reason\":\"lwt\"}",
          true    // cleanSession = true (harus re-subscribe setelah konek)
      );
      if (ok) {
        Serial.println("[MQTT] Terhubung dengan LWT aktif.");
        // Publikasikan status online sebagai retained message agar dashboard baru langsung tahu
        mqtt.publish(TOPIC_STATUS, "{\"state\":\"online\"}", true);
        // Subscribe perintah pada QoS 1
        mqtt.subscribe(TOPIC_CMD, 1);
      } else {
        Serial.printf("[MQTT] Connect gagal rc=%d\n", mqtt.state());
      }
    }
    return;
  }

  mqtt.loop();

  if ((uint32_t)(now - lastPubMs) >= TELEMETRY_MS) {
    lastPubMs = now;
    seqNum++;
    char jsonBuf[144];
    snprintf(
        jsonBuf,
        sizeof(jsonBuf),
        "{\"device_id\":\"%s\",\"seq\":%lu,\"temp_c\":29.10,\"source\":\"synthetic\"}",
        CLIENT_ID,
        static_cast<unsigned long>(seqNum)
    );
    mqtt.publish(TOPIC_DATA, jsonBuf, false);
  }
}

