// Chapter 16 — Demonstrasi Antarmuka UART2, I2C Scanner & Konfigurasi SPI pada ESP32
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32)
// Pin Default:
//   - I2C  : SDA = GPIO 21, SCL = GPIO 22 (wajib pull-up 4.7 kOhm ke 3.3V bila modul belum punya)
//   - UART2: RX2 = GPIO 16, TX2 = GPIO 17 (catatan: hindari 16/17 pada modul WROVER ber-PSRAM!)
//   - VSPI : SCLK = GPIO 18, MISO = GPIO 19, MOSI = GPIO 23, CS = GPIO 5

#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <cstdint>

constexpr uint8_t I2C_SDA_PIN  = 21;
constexpr uint8_t I2C_SCL_PIN  = 22;
constexpr uint8_t UART2_RX_PIN = 16;
constexpr uint8_t UART2_TX_PIN = 17;
constexpr uint8_t SPI_CS_PIN   = 5;

constexpr uint32_t SCAN_INTERVAL_MS = 5000;
uint32_t lastScanMs = 0;

void scanI2cBus() {
  uint8_t found = 0;
  Serial.println("[I2C] Memindai alamat 7-bit (0x08..0x77)...");
  for (uint8_t addr = 0x08; addr <= 0x77; ++addr) {
    Wire.beginTransmission(addr);
    const uint8_t err = Wire.endTransmission();
    if (err == 0) {
      Serial.printf("  -> Perangkat ditemukan di 0x%02X\n", addr);
      found++;
    } else if (err == 4) {
      Serial.printf("  -> Error bus tidak dikenal pada 0x%02X (cek pull-up SDA/SCL!)\n", addr);
    }
  }
  if (found == 0) {
    Serial.println("  -> Tidak ada slave I2C merespons (normal jika bus kosong).");
  }
}

void probeSpiTransfer() {
  // Contoh transaksi SPI Mode 0 (CPOL=0, CPHA=0), MSB first, 1 MHz
  SPISettings settings(1000000, MSBFIRST, SPI_MODE0);
  SPI.beginTransaction(settings);
  digitalWrite(SPI_CS_PIN, LOW);
  const uint8_t rx = SPI.transfer(0x9F); // Contoh perintah baca ID (JEDEC/register)
  digitalWrite(SPI_CS_PIN, HIGH);
  SPI.endTransaction();
  Serial.printf("[SPI] Transaksi uji Mode 0 selesai (MISO rx=0x%02X)\n", rx);
}

void setup() {
  Serial.begin(115200); // UART0 untuk Serial Monitor USB
  delay(200);

  // Inisialisasi UART2 dengan format 8N1 pada 9600 baud
  Serial2.begin(9600, SERIAL_8N1, UART2_RX_PIN, UART2_TX_PIN);

  // Inisialisasi I2C @ 100 kHz Standard Mode
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
  Wire.setClock(100000);
  Wire.setTimeOut(50);

  // Inisialisasi VSPI & pin Chip Select
  pinMode(SPI_CS_PIN, OUTPUT);
  digitalWrite(SPI_CS_PIN, HIGH); // CS idle HIGH (active-low)
  SPI.begin();

  Serial.println("=== CHAPTER 16: UART2, I2C SCANNER & SPI PROBE ===");
}

void loop() {
  // Teruskan data masuk dari UART2 ke Serial Monitor USB (non-blocking)
  while (Serial2.available() > 0) {
    const int ch = Serial2.read();
    Serial.printf("[UART2 RX] byte=0x%02X ('%c')\n", ch, (ch >= 32 && ch <= 126) ? ch : '.');
  }

  const uint32_t now = millis();
  if ((uint32_t)(now - lastScanMs) >= SCAN_INTERVAL_MS) {
    lastScanMs = now;
    scanI2cBus();
    probeSpiTransfer();
    Serial2.println("PING_UART2");
  }
}

