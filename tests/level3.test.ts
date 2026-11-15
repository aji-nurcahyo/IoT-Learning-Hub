import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');

test('Level 3: Telemetry schema validation & duplicate detection (Ch 21)', () => {
  const script = resolve(root, 'public/content/chapter-21/src/data_models_validator.py');
  const stdout = execFileSync('python', [script], { encoding: 'utf8' });
  assert.ok(stdout.includes('Valid Telemetry Validation: PASSED'));
  assert.ok(stdout.includes('Malformed Telemetry Rejection: PASSED'));
  assert.ok(stdout.includes('Message 101 Resend in TTL: Duplicate? True'));
  assert.ok(stdout.includes('Savings vs Raw'));
});

test('Level 3: Gateway data processing & framing checksum (Ch 22)', () => {
  const script = resolve(root, 'public/content/chapter-22/src/serial_mqtt_gateway.py');
  const stdout = execFileSync('python', [script], { encoding: 'utf8' });
  assert.ok(stdout.includes('Total sukses: 3, Korup: 2'));
  assert.ok(stdout.includes('Frame serial korup diabaikan'));
  assert.ok(stdout.includes('[MQTT PUBLISH]'));
});

test('Level 3: Edge processing, deadband & hysteresis rules (Ch 23)', () => {
  const script = resolve(root, 'public/content/chapter-23/src/edge_engine.py');
  const stdout = execFileSync('python', [script], { encoding: 'utf8' });
  assert.ok(stdout.includes('IQR Filter: Dari 8 sampel mentah -> 6 sampel bersih'));
  assert.ok(stdout.includes('Meredam 3 fluktuasi kecil'));
  assert.ok(stdout.includes('Hysteresis Control'));
  assert.ok(stdout.includes('All edge processing test cases passed successfully'));
});

test('Level 3: Node-RED event-driven flow & context routing (Ch 24)', () => {
  const script = resolve(root, 'public/content/chapter-24/src/nodered_flow_runner.py');
  const stdout = execFileSync('python', [script], { encoding: 'utf8' });
  assert.ok(stdout.includes('Validasi skema flows.json SUKSES'));
  assert.ok(stdout.includes('[ALARM DISPATCH]'));
  assert.ok(stdout.includes('HTTP Status : 200'));
  assert.ok(stdout.includes('[CATCH NODE] Exception ditangkap'));
});

test('Level 3: Time-series database ingestion, rollup & retention purge (Ch 25)', () => {
  const script = resolve(root, 'public/content/chapter-25/src/timeseries_retention_engine.py');
  const stdout = execFileSync('python', [script], { encoding: 'utf8' });
  assert.ok(stdout.includes('Bulk Ingestion: Berhasil memasukkan 30 baris'));
  assert.ok(stdout.includes('Jumlah jendela agregasi terbuat: 2'));
  assert.ok(stdout.includes('Data mentah terhapus'));
  assert.ok(stdout.includes('Data rollup agregasi tetap utuh'));
  assert.ok(stdout.includes('Total Kebutuhan Disk'));
});

test('Level 3: Alert triggering, pending duration & anti-flapping (Ch 26)', () => {
  const script = resolve(root, 'public/content/chapter-26/src/alert_state_machine.py');
  const stdout = execFileSync('python', [script], { encoding: 'utf8' });
  assert.ok(stdout.includes('State: NORMAL'));
  assert.ok(stdout.includes('Kondisi awal normal'));
  assert.ok(stdout.includes('State: PENDING'));
  assert.ok(stdout.includes('Spike sesaat'));
  assert.ok(stdout.includes('State: FIRING'));
  assert.ok(stdout.includes('[NOTIF DIKIRIM]'));
  assert.ok(stdout.includes('anti-flapping!'));
  assert.ok(stdout.includes('State: RESOLVED'));
  assert.ok(stdout.includes('Total Notifikasi Terkirim Sepanjang Simulasi: 3'));
});

test('Level 3: Device registry, heartbeat monitor & digital twin drift (Ch 27)', () => {
  const script = resolve(root, 'public/content/chapter-27/src/fleet_manager.py');
  const stdout = execFileSync('python', [script], { encoding: 'utf8' });
  assert.ok(stdout.includes('Enrollment: Berhasil mendaftarkan 2 node'));
  assert.ok(stdout.includes('Node 2 Status: DEGRADED'));
  assert.ok(stdout.includes('Node 2 Status: OFFLINE'));
  assert.ok(stdout.includes('Konfigurasi Drift Terdeteksi? True'));
  assert.ok(stdout.includes('Heartbeat ditolak untuk perangkat pensiun? Ya'));
});

test('Level 3: Cryptographic TLS X.509 certs & MQTT topic ACL matrix (Ch 28)', () => {
  const script = resolve(root, 'public/content/chapter-28/src/iot_security_evaluator.py');
  const stdout = execFileSync('python', [script], { encoding: 'utf8' });
  assert.ok(stdout.includes('Valid ECC P-256 Certificate: PASSED'));
  assert.ok(stdout.includes('Expired Certificate Rejection: PASSED'));
  assert.ok(stdout.includes('Self Telemetry Publish: Allowed? True'));
  assert.ok(stdout.includes('Cross-Device Telemetry Read: Allowed? False'));
  assert.ok(stdout.includes('Cross-Device Command Hijack: Allowed? False'));
  assert.ok(stdout.includes('STRIDE Threat Modeling Evaluation'));
});

test('Level 3: Dual-bank A/B OTA update, code signature & auto rollback (Ch 29)', () => {
  const script = resolve(root, 'public/content/chapter-29/src/ota_lifecycle_simulator.py');
  const stdout = execFileSync('python', [script], { encoding: 'utf8' });
  assert.ok(stdout.includes('Penolakan Firmware Korup / Palsu'));
  assert.ok(stdout.includes('Ditolak'));
  assert.ok(stdout.includes('ROLLBACK_TRIGGERED!'));
  assert.ok(stdout.includes('Kembali ke Bank: app0'));
  assert.ok(stdout.includes('Health-Check: Firmware v1.2.0-stable'));
  assert.ok(stdout.includes('dikonfirmasi VALID permanen'));
});

test('Level 3: Capstone end-to-end environmental platform workflow (Ch 30)', () => {
  const script = resolve(root, 'public/content/chapter-30/src/capstone_platform.py');
  const stdout = execFileSync('python', [script], { encoding: 'utf8' });
  assert.ok(stdout.includes('[SATC-01] Device Enrollment & Topic ACL Authorization:'));
  assert.ok(stdout.includes('[SATC-02] Telemetry Validation, Deduplication & Deadband Filtering:'));
  assert.ok(stdout.includes('[SATC-03] Time-Series Ingestion, 1-Minute Rollup & Retention Aging:'));
  assert.ok(stdout.includes('[SATC-04] Alert State Machine'));
  assert.ok(stdout.includes('[SATC-05] Digital Twin Configuration Drift & Reconciliation:'));
  assert.ok(stdout.includes('[SATC-06] Secure OTA Verification & Automatic Rollback:'));
  assert.ok(stdout.includes('ALL 6 SYSTEM ACCEPTANCE TEST CASES (SATC) PASSED SUCCESSFULLY!'));
});
