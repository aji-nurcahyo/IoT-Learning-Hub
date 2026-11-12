# Source Code — Chapter 11: Kalkulator CIDR, Goodput & Probe Jaringan

Folder `src/` berisi skrip Python 3 standar (memakai modul bawaan `ipaddress`, `csv`, `statistics`):

- [network_diagnostics_sim.py](content/chapter-11/src/network_diagnostics_sim.py): Menghitung subnet IPv4 CIDR, membandingkan efisiensi *goodput* TCP vs UDP pada payload IoT kecil ($48\text{ B}$), serta menghitung *packet loss*, RTT rata-rata, dan *jitter* dari dataset sintetis [telemetry.csv](content/chapter-11/telemetry.csv).

## Cara Menjalankan

```sh
python public/content/chapter-11/src/network_diagnostics_sim.py
```

## Status Verifikasi

- **Software model (`network_diagnostics_sim.py`)**: Dieksekusi nyata pada Python 3.12.10; hasil lengkap tercatat pada `outputs.md`.
- **Jaringan fisik / ping LAN nyata**: Tidak diuji pada perangkat keras lapangan; `telemetry.csv` adalah data sintetis.

