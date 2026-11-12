# Bukti & Output Eksekusi — Chapter 11

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (perhitungan subnet IPv4 CIDR, efisiensi *goodput* TCP vs UDP, serta statistik probe jaringan sintetis `telemetry.csv` di Python)
- **Tanggal**: 2026-11-11
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-11/src/network_diagnostics_sim.py`
- **Hardware / LAN fisik**: Tidak diuji (data probe di `telemetry.csv` adalah data sintetis)

## 2. Output Aktual (Verbatim — Software Verification)

```text
=== ANALISIS JARINGAN IoT: CIDR, GOODPUT & PROBE TELEMETRY (CHAPTER 11) ===
Subnet 192.168.50.0/26:
  Network / Broadcast : 192.168.50.0 / 192.168.50.63
  Netmask             : 255.255.255.192
  Rentang Host Usable : 192.168.50.1 .. 192.168.50.62 (62 host)

Efisiensi Goodput untuk Payload IoT = 48 B (Ethernet/MAC overhead=18 B):
  TCP/IPv4 (hdr 40 B) : total=106 B -> goodput=45.3%
  UDP/IPv4 (hdr 28 B) : total=94 B -> goodput=51.1%

Analisis Probe Sintetis (telemetry.csv, n=10):
  Paket hilang        : 1/10 (10.0% packet loss)
  RTT min/avg/max     : 2.4 / 6.57 / 18.6 ms
  Jitter (std dev)    : 5.16 ms
```

