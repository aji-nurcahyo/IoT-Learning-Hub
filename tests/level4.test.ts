import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execSync } from 'node:child_process';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');

test('Level 4: Low-power profiling & battery lifetime model (Ch 31)', () => {
  const stdout = execSync('python public/content/chapter-31/src/power_model_sim.py', { cwd: root, encoding: 'utf8' });
  assert.ok(stdout.includes('CHAPTER 31: LOW-POWER & BATTERY LIFETIME VERIFICATION'));
  assert.ok(stdout.includes('I_avg: 3.0097 mA'));
  assert.ok(stdout.includes('Lifetime: 3252.7 hari'));
  assert.ok(stdout.includes('STATUS: VERIFIED'));
});

test('Level 4: FreeRTOS priority preemption & queue concurrency (Ch 32)', () => {
  const stdout = execSync('python public/content/chapter-32/src/rtos_scheduler_sim.py', { cwd: root, encoding: 'utf8' });
  assert.ok(stdout.includes('CHAPTER 32: RTOS SCHEDULER & QUEUE SIMULATION'));
  assert.ok(stdout.includes('T3:SafetyWatchdog'));
  assert.ok(stdout.includes('Queue verified: Dropped=1, Remaining Items=2'));
  assert.ok(stdout.includes('STATUS: VERIFIED'));
});

test('Level 4: Industrial Modbus RTU CRC-16 & OPC UA information tree (Ch 33)', () => {
  const stdout = execSync('python public/content/chapter-33/src/industrial_protocol_sim.py', { cwd: root, encoding: 'utf8' });
  assert.ok(stdout.includes('CHAPTER 33: INDUSTRIAL IOT & PROTOCOLS SIMULATION'));
  assert.ok(stdout.includes('Modbus RTU Response Frame: 01030400FF028CCAC6'));
  assert.ok(stdout.includes('OPC UA Read Temp: 25.5 degC'));
  assert.ok(stdout.includes('STATUS: VERIFIED'));
});

test('Level 4: Thread mesh multihop routing & Matter commissioning (Ch 34)', () => {
  const stdout = execSync('python public/content/chapter-34/src/matter_thread_sim.py', { cwd: root, encoding: 'utf8' });
  assert.ok(stdout.includes('CHAPTER 34: MATTER & THREAD SIMULATION'));
  assert.ok(stdout.includes('DoorLock -> Router1 -> Leader -> BorderRouter -> LightSensor'));
  assert.ok(stdout.includes('Session=CASE_READY'));
  assert.ok(stdout.includes('STATUS: VERIFIED'));
});

test('Level 4: Edge AI TinyML feature extraction & INT8 quantized inference (Ch 35)', () => {
  const stdout = execSync('python public/content/chapter-35/src/tinyml_inference_sim.py', { cwd: root, encoding: 'utf8' });
  assert.ok(stdout.includes('CHAPTER 35: TINYML & SENSOR INFERENCE SIMULATION'));
  assert.ok(stdout.includes('Inferensi Normal -> Label: NORMAL'));
  assert.ok(stdout.includes('Inferensi Anomali -> Label: ANOMALY_BEARING_FAULT'));
  assert.ok(stdout.includes('STATUS: VERIFIED'));
});

test('Level 4: Digital Twin thermal dynamic sync & What-If projection (Ch 36)', () => {
  const stdout = execSync('python public/content/chapter-36/src/digital_twin_sim.py', { cwd: root, encoding: 'utf8' });
  assert.ok(stdout.includes('CHAPTER 36: DIGITAL TWIN & SYSTEM MODELING SIMULATION'));
  assert.ok(stdout.includes('Status: SYNCHRONIZED'));
  assert.ok(stdout.includes('Prediksi Suhu 60s ke Depan pada 250W -> 47.11 C'));
  assert.ok(stdout.includes('STATUS: VERIFIED'));
});

test('Level 4: Scalable broker sharding, device hash & backpressure limit (Ch 37)', () => {
  const stdout = execSync('python public/content/chapter-37/src/scalability_cluster_sim.py', { cwd: root, encoding: 'utf8' });
  assert.ok(stdout.includes('CHAPTER 37: SCALABLE IOT ARCHITECTURE SIMULATION'));
  assert.ok(stdout.includes('Distribusi Pesan pada Partisi [0, 1, 2, 3]: [25, 24, 23, 28]'));
  assert.ok(stdout.includes('Total Dropped (Backpressure): 5'));
  assert.ok(stdout.includes('STATUS: VERIFIED'));
});

test('Level 4: Fault injection chaos testing, brownout & MTBF metrics (Ch 38)', () => {
  const stdout = execSync('python public/content/chapter-38/src/fault_injection_harness.py', { cwd: root, encoding: 'utf8' });
  assert.ok(stdout.includes('CHAPTER 38: FAULT INJECTION & RELIABILITY SIMULATION'));
  assert.ok(stdout.includes('Total pesan sukses terkirim ke backend: 5'));
  assert.ok(stdout.includes('Availability: 99.863%'));
  assert.ok(stdout.includes('STATUS: VERIFIED'));
});

test('Level 4: STRIDE threat model, DREAD scoring & PII data minimization (Ch 39)', () => {
  const stdout = execSync('python public/content/chapter-39/src/threat_model_governance_sim.py', { cwd: root, encoding: 'utf8' });
  assert.ok(stdout.includes('CHAPTER 39: STRIDE THREAT MODEL & PRIVACY SIMULATION'));
  assert.ok(stdout.includes('THREAT-01 [Spoofing] -> Skor DREAD: 8.0 (CRITICAL)'));
  assert.ok(stdout.includes("Payload Higienis Privasi: {'device_id': 'sensor-room-101', 'temperature': 24.5, 'humidity': 55.0}"));
  assert.ok(stdout.includes('STATUS: VERIFIED'));
});

test('Level 4: Advanced Capstone platform SATC-01 to SATC-06 acceptance suite (Ch 40)', () => {
  const stdout = execSync('python public/content/chapter-40/src/advanced_capstone_platform.py', { cwd: root, encoding: 'utf8' });
  assert.ok(stdout.includes('CHAPTER 40: ADVANCED IOT SYSTEMS CAPSTONE PLATFORM'));
  assert.ok(stdout.includes('[SATC-01] Power Budget & Battery Lifetime: PASS'));
  assert.ok(stdout.includes('[SATC-02] FreeRTOS Preemption Timeline: PASS'));
  assert.ok(stdout.includes('[SATC-03] Industrial Modbus RTU Framing: PASS'));
  assert.ok(stdout.includes('[SATC-04] Edge AI TinyML Anomaly Inference: PASS'));
  assert.ok(stdout.includes('[SATC-05] Digital Twin Thermal & What-If: PASS'));
  assert.ok(stdout.includes('[SATC-06] Resilience & Privacy Governance: PASS'));
  assert.ok(stdout.includes('ALL 6 SYSTEM ACCEPTANCE TEST CASES (SATC) VERIFIED 100%!'));
});
