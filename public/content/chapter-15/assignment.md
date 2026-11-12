# Tugas & Rubrik — Chapter 15

## Skenario Tugas: Rancangan Keandalan MQTT (QoS, LWT, Retained & Deduplikasi)

Anda merancang lapisan pesan MQTT untuk **Sistem Monitoring & Kontrol Ruang Server Kampus** yang memiliki 4 aliran pesan:
1. `campus/server-room/node-01/telemetry` (suhu & kelembaban tiap 5 detik),
2. `campus/server-room/node-01/alarm` (peringatan overheat $> 32\,^\circ\text{C}$),
3. `campus/server-room/node-01/status` (status online/offline perangkat),
4. `campus/server-room/node-01/cmd/buzzer` (perintah reset alarm dari operator NOC).

## Instruksi Pengerjaan

1. **Matriks Kebijakan QoS & Retained**: Tentukan QoS (0/1/2) dan flag `retain` (`true`/`false`) untuk keempat topic di atas beserta justifikasi teknisnya (termasuk catatan apakah pustaka `PubSubClient` atau `esp-mqtt` yang dibutuhkan).
2. **Konfigurasi LWT & Keepalive**: Rancang parameter `CONNECT` (LWT topic, payload, QoS, retain, keepalive, dan `cleanSession`) beserta diagram alur dari normal $\rightarrow$ putus mendadak $\rightarrow$ LWT terpicu $\rightarrow$ reconnect & re-subscribe.
3. **Mekanisme Deduplikasi & Simulasi**: Implementasikan atau perluas skrip simulasi/kode ESP32 untuk menangani duplikat QoS 1 berbasis `seq`/`cmd_seq`, dan lampirkan log hasil pengujian jujur.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Pemilihan tingkat QoS per jenis topic** | **25** | Justifikasi QoS 0/1/2 tepat untuk telemetry, alarm, status, dan command serta sadar batas library. |
| **Desain Retained, LWT & Keepalive** | **25** | Penggunaan `retain=true` hanya pada status (tidak pada command!), LWT dan keepalive tepat. |
| **Deduplikasi & manajemen Session/Reconnect** | **30** | Mekanisme idempoten `seq`, alur re-subscribe pada `cleanSession`, serta perbandingan MQTT 5.0. |
| **Simulasi pengujian & kejujuran bukti** | **20** | Output uji terdokumentasi asli dengan pemisahan jelas antara simulasi software dan uji hardware. |

