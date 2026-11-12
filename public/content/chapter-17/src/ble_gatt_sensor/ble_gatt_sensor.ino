// Chapter 17: BLE GATT Server (ESP32 Arduino BLE Library)
// Service: Environmental Sensing (0x181A)
// Characteristics: Temperature (0x2A6E READ | NOTIFY + CCCD) & Interval Control (WRITE | READ)

#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define ENV_SERVICE_UUID        "181A"
#define TEMP_CHAR_UUID          "2A6E"
#define INTERVAL_CHAR_UUID      "7b9d0002-6c3e-4b2a-9a10-112233445566"

BLEServer* pServer = nullptr;
BLECharacteristic* pTempChar = nullptr;
BLECharacteristic* pIntervalChar = nullptr;

volatile bool deviceConnected = false;
bool oldDeviceConnected = false;
uint32_t notifyIntervalMs = 2000;
unsigned long lastNotifyMs = 0;

class ServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* server) override {
    deviceConnected = true;
    Serial.println("[BLE] Central connected");
  }

  void onDisconnect(BLEServer* server) override {
    deviceConnected = false;
    Serial.println("[BLE] Central disconnected -> restarting advertising");
  }
};

class IntervalCallbacks : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic* characteristic) override {
    String val = characteristic->getValue();
    if (val.length() > 0) {
      long parsed = val.toInt();
      if (parsed >= 500 && parsed <= 60000) {
        notifyIntervalMs = static_cast<uint32_t>(parsed);
        Serial.printf("[GATT] Interval updated to %lu ms\n", static_cast<unsigned long>(notifyIntervalMs));
      } else {
        Serial.println("[GATT] Ignored out-of-range interval (valid: 500..60000 ms)");
      }
    }
  }
};

void setup() {
  Serial.begin(115200);
  delay(200);

  BLEDevice::init("ITERA-BLE-EnvNode");
  BLEDevice::setMTU(128);

  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new ServerCallbacks());

  BLEService* pService = pServer->createService(ENV_SERVICE_UUID);

  pTempChar = pService->createCharacteristic(
    TEMP_CHAR_UUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
  );
  pTempChar->addDescriptor(new BLE2902());

  pIntervalChar = pService->createCharacteristic(
    INTERVAL_CHAR_UUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE
  );
  pIntervalChar->setCallbacks(new IntervalCallbacks());
  pIntervalChar->setValue("2000");

  pService->start();

  BLEAdvertising* pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(ENV_SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);
  BLEDevice::startAdvertising();

  Serial.println("[BLE] Advertising as ITERA-BLE-EnvNode (Service 0x181A)");
}

void loop() {
  unsigned long now = millis();

  if (deviceConnected && (now - lastNotifyMs >= notifyIntervalMs)) {
    lastNotifyMs = now;
    // Simulasi suhu 27.50 C + variasi periodik, encoded int16 skala 0.01 C (IEEE/GATT 0x2A6E)
    float tempC = 27.50f + 0.50f * sinf(now / 5000.0f);
    int16_t encoded = static_cast<int16_t>(lroundf(tempC * 100.0f));
    uint8_t payload[2] = {
      static_cast<uint8_t>(encoded & 0xFF),
      static_cast<uint8_t>((encoded >> 8) & 0xFF)
    };
    pTempChar->setValue(payload, sizeof(payload));
    pTempChar->notify();
    Serial.printf("[NOTIFY] temp=%.2f C (raw=%d, bytes=%02X %02X)\n", tempC, encoded, payload[0], payload[1]);
  }

  // Mulai ulang advertising secara aman setelah koneksi terputus
  if (!deviceConnected && oldDeviceConnected) {
    delay(200);
    pServer->startAdvertising();
    oldDeviceConnected = false;
  }
  if (deviceConnected && !oldDeviceConnected) {
    oldDeviceConnected = true;
  }
}

