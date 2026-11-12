// Chapter 05 — Header Modular Non-Blocking Timer & LED Controller
#ifndef LED_TIMER_H
#define LED_TIMER_H

#include <Arduino.h>
#include <cstdint>

struct BlinkTask {
  uint8_t pin;
  uint32_t intervalMs;
  uint32_t lastToggleMs;
  bool ledState;
};

inline void initBlinkTask(BlinkTask& task, uint8_t pin, uint32_t intervalMs) {
  task.pin = pin;
  task.intervalMs = intervalMs;
  task.lastToggleMs = millis();
  task.ledState = false;
  pinMode(task.pin, OUTPUT);
  digitalWrite(task.pin, LOW);
}

inline void updateBlinkTask(BlinkTask& task, uint32_t nowMs) {
  // Pengurangan unsigned 32-bit tetap aman saat millis() rollover (~49.7 hari)
  if ((uint32_t)(nowMs - task.lastToggleMs) >= task.intervalMs) {
    task.lastToggleMs = nowMs;
    task.ledState = !task.ledState;
    digitalWrite(task.pin, task.ledState ? HIGH : LOW);
  }
}

#endif // LED_TIMER_H

