# Laporan Review Teknis: Chapter 37

- **Modul**: Chapter 37 — Scalable IoT Architecture & Deployment
- **Reviewer**: Tim Kurikulum & Rekayasa Sistem Tertanam IoT ITERA
- **Tanggal Review**: 2026-11-17
- **Status Evaluasi**: Diterima untuk Publikasi (Verified)

## Hasil Penilaian

1. **Kedalaman Akademik & Akurasi Rekayasa**:
   Materi menguraikan komparasi scaling vertikal vs horizontal, kluster broker MQTT (EMQX/VerneMQ), load balancing layer-4 vs layer-7, formulasi partisi hash deterministik, mitigasi backpressure, dan orkestrasi kontainer Kubernetes.

2. **Kesesuaian Anti-Slop (DURING Mode)**:
   Materi bebas dari klaim abstrak seperti "skalabilitas tak terbatas". Setiap aspek arsitektur dijelaskan melalui batasan fisik konkret (batas soket TCP `ulimit`, throughput paket per detik, dan buffer heap).

3. **Reproduksibilitas Implementasi**:
   Modul `scalability_cluster_sim.py` dapat dieksekusi secara instan dan membuktikan distribusi beban yang merata serta penegakan batas backpressure secara deterministik.
