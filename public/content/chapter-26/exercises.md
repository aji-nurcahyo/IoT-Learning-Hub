# Latihan Soal & Praktik — Chapter 26

## Bagian A — Soal Konseptual

1. **Prinsip Situational Awareness**:
   Jelaskan mengapa dashboard pemantauan ruang kontrol industri dianjurkan menggunakan latar belakang gelap (*Dark Theme*) dengan warna indikator fungsional tegas (Hijau, Kuning, Merah), dibandingkan tema terang dengan warna-warni dekoratif yang ramai.
2. **Mitigasi Alert Fatigue**:
   Sebutkan dan jelaskan tiga strategi rekayasa sistem yang dapat diterapkan untuk melindungi teknisi lapangan dari kelelahan peringatan (*alert fatigue*).
3. **Kalkulasi Metrik MTBF**:
   Sebuah generator turbin IoT beroperasi selama 30 hari (720 jam). Selama periode tersebut, turbin mengalami 3 kali insiden pemadaman darurat (*tripping*) dengan total durasi perbaikan mencapai 18 jam. Hitung nilai *Mean Time Between Failures* (MTBF) turbin tersebut.

## Bagian B — Soal Praktik Komputasi

1. **Simulasi Transisi State Machine**:
   Gunakan skrip [`alert_state_machine.py`](content/chapter-26/src/alert_state_machine.py). Ubah parameter `pending_duration_sec` menjadi $10\text{ detik}$ dan `hysteresis` menjadi $2{,}0\,^\circ\text{C}$.
   - Tentukan pada detik ke berapa status berubah menjadi `FIRING` jika suhu naik ke $31{,}0\,^\circ\text{C}$ pada detik $t = 10\text{s}$ dan bertahan konstan.
   - Pada suhu berapa status baru dinyatakan `RESOLVED` jika ambang batas atas adalah $30{,}0\,^\circ\text{C}$?
2. **Eksplorasi Model JSON Grafana**:
   Buka file [`grafana_dashboard_model.json`](content/chapter-26/src/grafana_dashboard_model.json). Identifikasi panel nomor 3 (`Live Temperature Gauge`). Sebutkan nilai ambang batas numerik (*thresholds*) untuk perubahan warna dari hijau ke oranye, dan dari oranye ke merah.
