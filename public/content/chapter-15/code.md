# Source Code — Chapter 15: MQTT QoS, Retained Messages & Last Will

Folder `src/` berisi:

1. [mqtt_lwt_retained.ino](content/chapter-15/src/mqtt_lwt_retained/mqtt_lwt_retained.ino): Firmware ESP32 dengan `PubSubClient` yang mendaftarkan **Last Will (`offline`, retained)** saat `CONNECT`, menerbitkan status **`online` (retained)** saat berhasil terhubung, mengatur `keepAlive = 30 s`, melakukan `subscribe` QoS 1, dan menerapkan deduplikasi perintah via `cmd_seq`.
2. [mqtt_qos_lwt_sim.py](content/chapter-15/src/mqtt_qos_lwt_sim.py): Simulasi Python untuk memverifikasi *packet handshake* QoS 0/1/2, deduplikasi pesan ganda pada QoS 1, penyimpanan *Retained Message*, dan pemicuan LWT saat *keepalive* terlampaui.

## Cara Menjalankan

**Simulasi Python:**
```sh
python public/content/chapter-15/src/mqtt_qos_lwt_sim.py
```

**Firmware ESP32:**
- Memerlukan library `PubSubClient` (`v2.8+`).
- Untuk menguji LWT pada Mosquitto lokal: jalankan `mosquitto_sub -t "lab/gh01/node-01/status" -v`, hubungkan node, lalu cabut daya/putuskan jaringan node secara mendadak dan tunggu $\sim 45\text{ detik}$ ($1{,}5 \times 30\text{ s}$).

