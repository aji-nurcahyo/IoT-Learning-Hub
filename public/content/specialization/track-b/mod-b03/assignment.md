# Tugas Rekayasa & Rubrik: Modul B03

## Perancangan Arsitektur Polling Bus & Pemetaan Data Modbus ke Server OPC UA

Rancang arsitektur akuisisi data pabrik yang mengintegrasikan 8 power meter Modbus RTU ke server SCADA OPC UA:
1. Hitung waktu siklus polling pada variasi baud rate 9600, 19200, dan 38400 bps.
2. Buat skrip simulasi pemetaan holding register Modbus ke variabel OPC UA terstruktur.
3. Analisis mekanisme penanganan timeout jika salah satu slave mengalami kegagalan daya.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Pemodelan Waktu Polling Bus Serial RS-485** | 30 | Ketepatan perhitungan frame timing, waktu turnaround, dan refresh rate sistem. |
| **Desain Pohon Ruang Alamat OPC UA NodeSet** | 35 | Kualitas pengorganisasian hierarki objek industri dan pemetaan tipe data. |
| **Evaluasi Throughput, Timeout & Laporan Rekayasa** | 35 | Analisis kegagalan jaringan, penanganan timeout, dan kejelasan dokumentasi. |
