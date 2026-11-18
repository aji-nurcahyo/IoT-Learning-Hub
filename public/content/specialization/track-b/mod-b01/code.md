# Implementasi Kode & Walkthrough: Modul B01

## 1. Arsitektur Modul Simulasi
Modul [purdue_security_sim.py](src/purdue_security_sim.py) mengimplementasikan mesin penegakan aturan keamanan jaringan industri (*Industrial Security Policy Engine*) berbasis standar IEC 62443 dan model Purdue (ISA-95).

Kode diorganisasikan ke dalam:
1. `PurdueZone`: Enumerasi level hierarki otomasi (Level 0 Field hingga Level 4 Enterprise).
2. `IndustrialSecurityGateway`: Mesin inspeksi paket yang memvalidasi conduit legal, protokol yang diizinkan, serta larangan perintah tulis langsung dari luar.
3. `run_simulation()`: Harness pengujian deterministik yang menguji 5 skenario paket uji dan memverifikasi kriteria penerimaan.

---

## 2. Cara Menjalankan Simulasi
Eksekusi langsung dari terminal tanpa dependensi eksternal:

```bash
python public/content/specialization/track-b/mod-b01/src/purdue_security_sim.py
```

Luaran eksekusi terekam pada berkas bukti [outputs.md](outputs.md).

