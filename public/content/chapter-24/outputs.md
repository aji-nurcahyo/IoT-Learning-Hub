# Bukti Pengujian & Hasil Eksekusi — Chapter 24

Pengujian validasi struktur alur deklaratif Node-RED (`flows.json`) dan simulasi eksekusi event runtime dieksekusi menggunakan lingkungan runtime Python 3.

## Perintah Eksekusi

```bash
python public/content/chapter-24/src/nodered_flow_runner.py
```

## Hasil Keluaran Terminal (Standard Output)

```text
=== Node-RED Flow Execution & Integration Verification ===
[SIMULATOR] Validasi skema flows.json SUKSES (12 node terdeteksi).

Case 1: Mengirim Telemetry Normal (27.5 C)
[NORMAL LOG] Temp: 27.5 C < 30.0 C (Kondisi lingkungan normal).

Case 2: Mengirim Telemetry Kritis (31.8 C)
[ALARM DISPATCH] Topic: iot/lab/node-01/event/alarm | Temp: 31.8 C >= 30.0 C | Alarm ID: ALM-1794763103538

Case 3: Menyimulasikan HTTP GET /api/v1/telemetry/latest
HTTP Status : 200
Payload Data: {'dev': 'node-01', 'seq': 102, 'metrics': {'temp_c': 31.8, 'humidity_pct': 65.0}}

Case 4: Mengirim Telemetry Rusak (Tanpa field metrics)
[CATCH NODE] Exception ditangkap: Missing temp_c metric in payload

Semua skenario pengujian alur Node-RED berhasil diverifikasi.
```

## Analisis Hasil

1. **Integritas Alur Deklaratif**: Berkas `flows.json` memenuhi seluruh standar node primitives Node-RED (`tab`, `mqtt in`, `change`, `switch`, `function`, `mqtt out`, `http in`, `http response`, `catch`).
2. **Evaluasi Percabangan**: Paket telemetri dengan suhu $27{,}5\,^\circ\text{C}$ dialirkan ke jalur normal, sedangkan paket dengan suhu $31{,}8\,^\circ\text{C}$ berhasil memicu simpul Function untuk menyusun event alarm lengkap dengan stempel waktu dan menerbitkannya ke topik MQTT darurat.
3. **Penyediaan API REST**: Panggilan tiruan ke endpoint `GET /api/v1/telemetry/latest` sukses mengembalikan status telemetri terakhir yang tersimpan di dalam memori variabel `global`.
4. **Isolasi Pengecualian**: Paket malformed tanpa atribut metrik berhasil dicegat oleh simpul `catch` tanpa menghentikan simulasi runtime.
