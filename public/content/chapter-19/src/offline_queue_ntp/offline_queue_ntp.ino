// Chapter 19: SNTP Time Sync, Offline Ring Buffer & Jittered Exponential Backoff
// Catatan: Simulasi antrean telemetri di RAM (struct fixed-size tanpa String heap).

#include <Arduino.h>
#include <WiFi.h>
#include <time.h>

static const char* WIFI_SSID = "ITERA-IoT-Lab";
static const char* WIFI_PASS = "iot-lab-pass";
static const char* NTP_SERVER_1 = "pool.ntp.org";
static const char* NTP_SERVER_2 = "time.google.com";

struct TelemetryRecord {
  uint32_t seqId;
  uint64_t timestamp;
  bool timeSynced;
  float tempC;
};

constexpr size_t RING_CAPACITY = 32;
constexpr size_t MAX_DRAIN_PER_TICK = 4;

TelemetryRecord ringBuf[RING_CAPACITY];
size_t ringHead = 0;
size_t ringTail = 0;
size_t ringCount = 0;
uint32_t droppedOldest = 0;
uint32_t globalSeq = 0;

unsigned long lastSampleMs = 0;
unsigned long nextReconnectMs = 0;
uint8_t reconnectAttempt = 0;

bool isTimeSynced() {
  time_t now = 0;
  time(&now);
  // Valid epoch setelah 2024-01-01 (1704067200)
  return now >= 1704067200;
}

void pushRecord(const TelemetryRecord& rec) {
  if (ringCount == RING_CAPACITY) {
    ringHead = (ringHead + 1) % RING_CAPACITY;
    ringCount--;
    droppedOldest++;
  }
  ringBuf[ringTail] = rec;
  ringTail = (ringTail + 1) % RING_CAPACITY;
  ringCount++;
}

bool mockTransportSend(const TelemetryRecord& rec) {
  // Pengiriman hanya dianggap berhasil jika Wi-Fi terhubung
  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }
  Serial.printf(
    "{\"seq\":%lu,\"ts\":%llu,\"synced\":%s,\"temp\":%.2f}\n",
    static_cast<unsigned long>(rec.seqId),
    static_cast<unsigned long long>(rec.timestamp),
    rec.timeSynced ? "true" : "false",
    rec.tempC
  );
  return true;
}

unsigned long computeJitteredBackoffMs(uint8_t attempt) {
  uint8_t cappedExp = attempt > 5 ? 5 : attempt;
  uint32_t maxDelayMs = 1000UL << cappedExp; // 1s, 2s, 4s, 8s, 16s, 32s
  if (maxDelayMs > 60000UL) {
    maxDelayMs = 60000UL;
  }
  return esp_random() % (maxDelayMs + 1);
}

void setup() {
  Serial.begin(115200);
  delay(200);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  configTime(0, 0, NTP_SERVER_1, NTP_SERVER_2); // UTC (offset 0) untuk telemetry log
  Serial.println("[INIT] SNTP & Offline Ring Buffer ready (capacity=32)");
}

void loop() {
  unsigned long nowMs = millis();

  // 1. Akuisisi periodik tiap 5 detik (selalu masuk ring buffer dulu agar urutan terjaga)
  if (nowMs - lastSampleMs >= 5000) {
    lastSampleMs = nowMs;
    time_t nowEpoch = 0;
    time(&nowEpoch);
    bool synced = isTimeSynced();

    TelemetryRecord rec;
    rec.seqId = ++globalSeq;
    rec.timestamp = synced ? static_cast<uint64_t>(nowEpoch) : static_cast<uint64_t>(nowMs);
    rec.timeSynced = synced;
    rec.tempC = 26.80f + 0.40f * sinf(nowMs / 4000.0f);

    pushRecord(rec);
    Serial.printf("[BUF] queued seq=%lu depth=%u dropped=%lu\n",
                  static_cast<unsigned long>(rec.seqId),
                  static_cast<unsigned int>(ringCount),
                  static_cast<unsigned long>(droppedOldest));
  }

  // 2. Kelola reconnect non-blocking dengan full-jitter exponential backoff
  if (WiFi.status() != WL_CONNECTED) {
    if (nowMs >= nextReconnectMs) {
      unsigned long waitMs = computeJitteredBackoffMs(reconnectAttempt);
      if (reconnectAttempt < 10) {
        reconnectAttempt++;
      }
      nextReconnectMs = nowMs + waitMs;
      Serial.printf("[NET] disconnected -> retry scheduled in %lu ms\n", waitMs);
      WiFi.reconnect();
    }
    return;
  }

  reconnectAttempt = 0;

  // 3. Batch drain maksimal MAX_DRAIN_PER_TICK item per iterasi loop
  size_t drained = 0;
  while (ringCount > 0 && drained < MAX_DRAIN_PER_TICK) {
    if (!mockTransportSend(ringBuf[ringHead])) {
      break;
    }
    ringHead = (ringHead + 1) % RING_CAPACITY;
    ringCount--;
    drained++;
  }
}

