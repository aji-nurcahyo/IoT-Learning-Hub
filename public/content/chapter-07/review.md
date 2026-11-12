# Laporan Review — Chapter 07

- **Reviewer**: Aji Pamungkas Tri Nurcahyo (Self-Review Kurikulum & Teknis)
- **Tanggal**: 2026-11-10
- **Status Publikasi**: Layak dipublikasi dengan label verifikasi **Belum diuji (`untested`)** untuk kompilasi `.ino`/Wokwi, disertai bukti **Software (`adc_nyquist_sim.py`)**.

## Hasil Pemeriksaan

1. **Cakupan Materi**: Mencakup analog vs digital, kuantisasi, atenuasi & non-linearitas ADC ESP32, konflik `ADC2` + Wi-Fi, PWM `LEDC` v3.x, kriteria Nyquist & *aliasing*, serta *moving average*.
2. **Validasi Numerik**: `adc_nyquist_sim.py` mengonfirmasi penurunan standar deviasi dari 21,32 mV menjadi 2,30 mV pada `telemetry.csv` dan kesamaan diskrit sinyal 60 Hz yang di-*undersample* pada 80 Hz dengan alias 20 Hz.
3. **Kejujuran Bukti**: Output `ex01_adc_pwm_dimmer.ino` diberi label teoretis; belum ada pengujian hardware/Wokwi di server.

