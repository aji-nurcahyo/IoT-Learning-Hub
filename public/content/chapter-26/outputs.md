# Bukti Pengujian & Hasil Eksekusi — Chapter 26

Pengujian mesin status peringatan industri (*Alert State Machine*), evaluasi durasi penahanan $T_{\text{for}}$, pelepasan histeresis, dan pembatasan laju notifikasi dieksekusi menggunakan lingkungan runtime Python 3.

## Perintah Eksekusi

```bash
python public/content/chapter-26/src/alert_state_machine.py
```

## Hasil Keluaran Terminal (Standard Output)

```text
=== IoT Alert State Machine & Anti-Fatigue Verification Suite ===
t= 0.0s | Temp: 27.5 C | State: NORMAL  
         Catatan: Kondisi awal normal
t= 2.0s | Temp: 31.0 C | State: PENDING 
         Catatan: Spike sesaat mulai muncul (PENDING)
t= 4.0s | Temp: 28.0 C | State: NORMAL  
         Catatan: Spike hilang cepat sebelum 5s -> harus kembali ke NORMAL tanpa alert spam!
t=10.0s | Temp: 30.5 C | State: PENDING 
         Catatan: Kondisi panas persisten dimulai (PENDING)
t=12.0s | Temp: 31.2 C | State: PENDING 
         Catatan: Masih panas dalam jendela PENDING
t=16.0s | Temp: 31.5 C | State: FIRING   [NOTIF DIKIRIM]
         Catatan: Telah melewati 5 detik PENDING -> Harus FIRING!
t=20.0s | Temp: 31.0 C | State: FIRING  
         Catatan: Masih panas, tapi dalam jeda throttle -> Notifikasi diredam
t=32.0s | Temp: 30.8 C | State: FIRING   [NOTIF DIKIRIM]
         Catatan: Masih panas melewati 15s throttle -> Notifikasi pengingat dikirim
t=35.0s | Temp: 29.5 C | State: FIRING  
         Catatan: Suhu turun ke 29.5 C, tapi di atas 29.0 C (histeresis) -> Tetap FIRING, anti-flapping!
t=40.0s | Temp: 28.5 C | State: RESOLVED [NOTIF DIKIRIM]
         Catatan: Suhu turun di bawah 29.0 C -> Transisi RESOLVED!

Total Notifikasi Terkirim Sepanjang Simulasi: 3
Verifikasi Alert State Machine & Hysteresis SUKSES.
```

## Analisis Hasil

1. **Peredaman Lonjakan Transien**: Pada detik $t = 2\text{s}$, suhu melompat ke $31{,}0\,^\circ\text{C}$ (status menjadi `PENDING`), namun kembali turun ke $28{,}0\,^\circ\text{C}$ pada detik $t = 4\text{s}$ (sebelum durasi $5\text{s}$ tercapai). Sistem kembali ke `NORMAL` tanpa mengirimkan satu pun notifikasi palsu ke operator.
2. **Pemicuan Sah & Throttling**: Ketika suhu tinggi bertahan dari detik $t = 10\text{s}$ hingga $t = 16\text{s}$, sistem secara sah menaikkan status menjadi `FIRING` dan mengirim notifikasi #1. Pada detik $t = 20\text{s}$, notifikasi diredam karena masih berada di dalam interval throttle $15\text{s}$. Pengingat #2 baru dikirim pada detik $t = 32\text{s}$.
3. **Pemberantasan Flapping**: Pada detik $t = 35\text{s}$, suhu turun ke $29{,}5\,^\circ\text{C}$ (di bawah ambang $30{,}0\,^\circ\text{C}$ tetapi masih di atas $29{,}0\,^\circ\text{C}$). Status tetap bertahan `FIRING`, mencegah osilasi notifikasi on/off. Sistem baru memicu status `RESOLVED` dan mengirim notifikasi #3 pada detik $t = 40\text{s}$ saat suhu benar-benar menyentuh $28{,}5\,^\circ\text{C}$.
