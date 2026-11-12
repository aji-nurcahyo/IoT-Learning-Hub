// Chapter 10 Capstone — Smart Environmental Monitoring & Local Control System
// Target board: ESP32-DevKitC V4 (ESP32-WROOM-32), Arduino-ESP32 v3.x
// Catatan: Tidak memerlukan Wi-Fi/MQTT/Cloud; fokus integrasi fondasi Level 1.

#include <Arduino.h>
#include <cmath>
#include <cstdint>
#include "env_config.h"

// State & Buffer
ControlMode activeMode = ControlMode::AUTO_NORMAL;
ControlMode modeBeforeFault = ControlMode::AUTO_NORMAL;
bool fanActive = false;
bool alarmActive = false;

uint32_t mvWindow[MOVING_AVG_N] = {0};
uint8_t windowIdx = 0;
uint8_t windowCount = 0;
uint32_t windowSum = 0;

bool lastRawBtn = HIGH;
bool stableBtn = HIGH;
uint32_t lastBounceMs = 0;

uint32_t lastSampleMs = 0;
uint32_t lastTelemetryMs = 0;
uint32_t lastLedMs = 0;
bool statusLedState = false;
uint32_t seqNum = 0;
float latestTempC = NAN;
const char* faultReason = "NONE";

const char* modeToStr(ControlMode m) {
  switch (m) {
    case ControlMode::AUTO_NORMAL: return "AUTO_NORMAL";
    case ControlMode::AUTO_STRICT: return "AUTO_STRICT";
    case ControlMode::MANUAL_ON:   return "MANUAL_ON";
    case ControlMode::FAULT_SAFE:  return "FAULT_SAFE";
    default:                       return "UNKNOWN";
  }
}

float convertMvToCalibratedC(float mv) {
  if (mv < ADC_MIN_MV || mv > ADC_MAX_MV) {
    return NAN;
  }
  const float rNtc = R_FIXED_OHM * (mv / (V_SUPPLY_MV - mv));
  const float invT = (1.0f / T25_KELVIN) + (1.0f / NTC_BETA_K) * logf(rNtc / NTC_R25_OHM);
  const float rawC = (1.0f / invT) - 273.15f;
  return (CAL_SLOPE * rawC) + CAL_OFFSET;
}

void handleModeButton(uint32_t now) {
  const bool raw = digitalRead(PIN_MODE_BUTTON);
  if (raw != lastRawBtn) {
    lastBounceMs = now;
    lastRawBtn = raw;
  }
  if ((uint32_t)(now - lastBounceMs) >= DEBOUNCE_MS && raw != stableBtn) {
    stableBtn = raw;
    if (stableBtn == LOW && activeMode != ControlMode::FAULT_SAFE) {
      if (activeMode == ControlMode::AUTO_NORMAL) {
        activeMode = ControlMode::AUTO_STRICT;
      } else if (activeMode == ControlMode::AUTO_STRICT) {
        activeMode = ControlMode::MANUAL_ON;
      } else {
        activeMode = ControlMode::AUTO_NORMAL;
      }
      modeBeforeFault = activeMode;
    }
  }
}

void updateStatusLed(uint32_t now) {
  if (activeMode == ControlMode::FAULT_SAFE) {
    digitalWrite(PIN_STATUS_LED, LOW);
    return;
  }
  if (activeMode == ControlMode::MANUAL_ON) {
    digitalWrite(PIN_STATUS_LED, HIGH);
    return;
  }
  const uint32_t period = (activeMode == ControlMode::AUTO_STRICT) ? 250 : 1000;
  if ((uint32_t)(now - lastLedMs) >= period) {
    lastLedMs = now;
    statusLedState = !statusLedState;
    digitalWrite(PIN_STATUS_LED, statusLedState ? HIGH : LOW);
  }
}

void evaluateControl(bool interlockOpen) {
  if (interlockOpen) {
    activeMode = ControlMode::FAULT_SAFE;
    faultReason = "INTERLOCK_OPEN";
    fanActive = false;
    alarmActive = true;
  } else if (isnan(latestTempC)) {
    activeMode = ControlMode::FAULT_SAFE;
    faultReason = "SENSOR_FAULT_NAN";
    fanActive = false;
    alarmActive = true;
  } else {
    if (activeMode == ControlMode::FAULT_SAFE) {
      activeMode = modeBeforeFault;
      faultReason = "NONE";
    }
    alarmActive = (latestTempC >= EMERGENCY_T_C);

    if (activeMode == ControlMode::MANUAL_ON) {
      fanActive = true;
    } else {
      const float tHigh = (activeMode == ControlMode::AUTO_STRICT) ? STRICT_T_HIGH_C : NORMAL_T_HIGH_C;
      const float tLow  = (activeMode == ControlMode::AUTO_STRICT) ? STRICT_T_LOW_C  : NORMAL_T_LOW_C;
      if (!fanActive && latestTempC >= tHigh) {
        fanActive = true;
      } else if (fanActive && latestTempC <= tLow) {
        fanActive = false;
      }
    }
  }

  ledcWrite(PIN_FAN_PWM, fanActive ? FAN_DUTY_ON : 0);
  digitalWrite(PIN_ALARM_BUZZER, alarmActive ? HIGH : LOW);
}

void setup() {
  Serial.begin(115200);
  delay(200);

  pinMode(PIN_MODE_BUTTON, INPUT_PULLUP);
  pinMode(PIN_INTERLOCK, INPUT_PULLUP);
  pinMode(PIN_STATUS_LED, OUTPUT);
  pinMode(PIN_ALARM_BUZZER, OUTPUT);
  digitalWrite(PIN_STATUS_LED, LOW);
  digitalWrite(PIN_ALARM_BUZZER, LOW);

  ledcAttach(PIN_FAN_PWM, FAN_PWM_FREQ_HZ, FAN_PWM_RES);
  ledcWrite(PIN_FAN_PWM, 0);

  analogReadResolution(12);
  analogSetPinAttenuation(PIN_NTC_ADC, ADC_11db);

  Serial.println("=== CAPSTONE LEVEL 1: SMART ENV MONITOR & LOCAL CONTROL ===");
}

void loop() {
  const uint32_t now = millis();

  handleModeButton(now);
  const bool interlockOpen = (digitalRead(PIN_INTERLOCK) == HIGH);

  if ((uint32_t)(now - lastSampleMs) >= SAMPLE_INTERVAL_MS) {
    lastSampleMs = now;
    const uint32_t mv = analogReadMilliVolts(PIN_NTC_ADC);

    if (mv < ADC_MIN_MV || mv > ADC_MAX_MV) {
      latestTempC = NAN;
    } else {
      windowSum -= mvWindow[windowIdx];
      mvWindow[windowIdx] = mv;
      windowSum += mv;
      windowIdx = (windowIdx + 1) % MOVING_AVG_N;
      if (windowCount < MOVING_AVG_N) windowCount++;

      const float avgMv = static_cast<float>(windowSum) / windowCount;
      latestTempC = convertMvToCalibratedC(avgMv);
    }
    evaluateControl(interlockOpen);
  }

  updateStatusLed(now);

  if ((uint32_t)(now - lastTelemetryMs) >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryMs = now;
    seqNum++;
    char jsonBuf[192];
    if (isnan(latestTempC)) {
      snprintf(
          jsonBuf, sizeof(jsonBuf),
          "{\"seq\":%lu,\"uptime_ms\":%lu,\"temp_c\":null,\"mode\":\"%s\",\"fan\":\"%s\",\"alarm\":%s,\"fault\":\"%s\"}",
          static_cast<unsigned long>(seqNum), static_cast<unsigned long>(now),
          modeToStr(activeMode), fanActive ? "ON" : "OFF",
          alarmActive ? "true" : "false", faultReason
      );
    } else {
      snprintf(
          jsonBuf, sizeof(jsonBuf),
          "{\"seq\":%lu,\"uptime_ms\":%lu,\"temp_c\":%.2f,\"mode\":\"%s\",\"fan\":\"%s\",\"alarm\":%s,\"fault\":\"%s\"}",
          static_cast<unsigned long>(seqNum), static_cast<unsigned long>(now),
          latestTempC, modeToStr(activeMode), fanActive ? "ON" : "OFF",
          alarmActive ? "true" : "false", faultReason
      );
    }
    Serial.println(jsonBuf);
  }
}

