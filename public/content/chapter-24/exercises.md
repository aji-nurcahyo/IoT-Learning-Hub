# Latihan Soal & Praktik — Chapter 24

## Bagian A — Soal Konseptual

1. **Perbandingan Paradigma Pemrograman**:
   Bandingkan kelebihan dan kekurangan antara membangun integrasi pipeline telemetri menggunakan Node-RED berbasis aliran visual (*flow-based low-code*) versus menulis layanan backend mandiri menggunakan Python Flask/FastAPI dari nol.
2. **Cakupan Variabel Konteks**:
   Sebuah sistem Node-RED memiliki 3 tab terpisah: `Ingestion`, `Alerting`, dan `Reporting`. Jika variabel ambang batas alarm disimpan pada cakupan `flow.set('threshold', 30.0)` di tab `Ingestion`, dapatkah simpul di tab `Alerting` membaca nilai tersebut secara langsung? Jelaskan cakupan konteks yang tepat untuk kebutuhan tersebut.
3. **Mekanisme Simpul Catch**:
   Apa yang membedakan penanganan kesalahan menggunakan blok `try { ... } catch (e) { ... }` lokal di dalam simpul Function dengan memasang simpul `catch` khusus pada lembar kerja Node-RED?

## Bagian B — Soal Praktik Komputasi

1. **Eksplorasi Format Aliran Deklaratif**:
   Buka file [`flows.json`](content/chapter-24/src/flows.json). Identifikasi simpul yang bertanggung jawab menerbitkan pesan ke broker MQTT. Sebutkan atribut `id`, `type`, dan daftar simpul masukan (`wires`) yang terhubung dengannya.
2. **Modifikasi Ambang Batas Logika**:
   Menggunakan skrip [`nodered_flow_runner.py`](content/chapter-24/src/nodered_flow_runner.py), ubah kondisi pengujian agar ambang batas peringatan suhu dinaikkan menjadi $32{,}0\,^\circ\text{C}$. Jalankan simulasi kembali dan amati apakah payload dengan suhu $31{,}8\,^\circ\text{C}$ kini masuk ke kategori log normal.
