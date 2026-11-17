// Chapter 32: FreeRTOS Multitasking, Queue & Mutex pada ESP32
// Kompatibel dengan ESP32 Arduino Core dan Wokwi simulator

#include <Arduino.h>

// Definisi handle queue dan mutex
QueueHandle_t sensorQueue;
SemaphoreHandle_t printMutex;

// Struktur data telemetri yang dikirim melalui Queue
struct SensorData {
  float temperature;
  float humidity;
  uint32_t timestamp;
};

// Task 1: Pembacaan sensor berkala (Prioritas 2)
void TaskSensor(void *pvParameters) {
  (void) pvParameters;
  SensorData data;

  for (;;) {
    data.temperature = 25.0 + (random(0, 100) / 10.0);
    data.humidity = 60.0 + (random(0, 200) / 10.0);
    data.timestamp = millis();

    // Kirim data ke queue tanpa memblokir jika penuh
    if (xQueueSend(sensorQueue, &data, (TickType_t) 10) != pdPASS) {
      if (xSemaphoreTake(printMutex, (TickType_t) 5) == pdTRUE) {
        Serial.println("[WARN] Sensor Queue penuh, data dibuang!");
        xSemaphoreGive(printMutex);
      }
    }

    // Delay deterministik berbasis tick RTOS (setiap 500 ms)
    vTaskDelay(pdMS_TO_TICKS(500));
  }
}

// Task 2: Pemrosesan data & transmisi serial (Prioritas 1)
void TaskTelemetry(void *pvParameters) {
  (void) pvParameters;
  SensorData receivedData;

  for (;;) {
    // Menunggu data dari queue (blokir hingga data tersedia)
    if (xQueueReceive(sensorQueue, &receivedData, portMAX_DELAY) == pdPASS) {
      if (xSemaphoreTake(printMutex, portMAX_DELAY) == pdTRUE) {
        Serial.printf("[TELEMETRY @ %lu ms] Temp: %.2f C | Hum: %.2f %%\n",
                      receivedData.timestamp,
                      receivedData.temperature,
                      receivedData.humidity);
        xSemaphoreGive(printMutex);
      }
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(100);

  Serial.println("\n=== FREE_RTOS CONCURRENCY INITIALIZED ===");

  // Buat Mutex untuk sinkronisasi akses Serial
  printMutex = xSemaphoreCreateMutex();

  // Buat Queue untuk menampung maksimal 5 struct SensorData
  sensorQueue = xQueueCreate(5, sizeof(SensorData));

  if (sensorQueue != NULL && printMutex != NULL) {
    // Buat TaskSensor pada Core 1
    xTaskCreatePinnedToCore(
      TaskSensor,       // Fungsi task
      "TaskSensor",     // Nama task
      2048,             // Alokasi stack (word)
      NULL,             // Parameter
      2,                // Prioritas (lebih tinggi)
      NULL,             // Task handle
      1                 // Pinned core
    );

    // Buat TaskTelemetry pada Core 1
    xTaskCreatePinnedToCore(
      TaskTelemetry,
      "TaskTelemetry",
      2048,
      NULL,
      1,                // Prioritas (lebih rendah)
      NULL,
      1
    );

    Serial.println("[SYSTEM] TaskSensor (Pri 2) & TaskTelemetry (Pri 1) berjalan.");
  } else {
    Serial.println("[ERROR] Gagal mengalokasikan memori Queue/Mutex!");
  }
}

void loop() {
  // Dalam FreeRTOS ESP32, loop() berjalan sebagai task prioritas 1 pada Core 1
  vTaskDelay(pdMS_TO_TICKS(1000));
}
