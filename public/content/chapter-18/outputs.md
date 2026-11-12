# Bukti & Output — Chapter 18: LoRa & LoRaWAN Fundamentals

- **Status Verifikasi Saat Ini**: Software Simulation **Terverifikasi (`software`)**; uji transceiver RF fisik (`SX1276`/`SX1262`), gateway LoRaWAN, dan *Network Server* (*The Things Stack* / *ChirpStack*) belum dijalankan (**Not Tested**).
- **Keterbatasan**: Perhitungan *link budget* pada skrip menggunakan model ruang bebas (FSPL) dengan margin *fading* asumsi `15 dB` sebagai dasar ilustrasi; kondisi propagasi kebun, gedung, atau topografi berbukit membutuhkan survei RF lapangan.

## Output Aktual `lora_airtime_budget.py`

Command:

```text
python public/content/chapter-18/src/lora_airtime_budget.py
```

Exit code: `0`

```text
=== CHAPTER 18: LORA PHY TIME-ON-AIR & LINK BUDGET CALCULATOR ===
Parameter simulasi: Payload=24 B, BW=125 kHz, CR=4/5, Preamble=8, CRC=ON
(Catatan regulasi: duty cycle/dwell time aktual wajib merujuk LoRa Alliance RP2 & regulator nasional.)

  SF | T_sym (ms) | DE |   ToA (ms) | Contoh 1% Wait (s) | Sens_SX1276 (dBm)
----------------------------------------------------------------------------
SF7  |      1.024 |  0 |      61.70 |               6.11 |            -123.0
SF8  |      2.048 |  0 |     113.15 |              11.20 |            -126.0
SF9  |      4.096 |  0 |     205.82 |              20.38 |            -129.0
SF10 |      8.192 |  0 |     370.69 |              36.70 |            -132.0
SF11 |     16.384 |  1 |     823.30 |              81.51 |            -134.5
SF12 |     32.768 |  1 |    1482.75 |             146.79 |            -137.0

[LINK BUDGET @ 3.0 km, 923 MHz, shadow_margin=15 dB]
FSPL = 101.29 dB | P_rx_est = -98.79 dBm
  Margin di SF7  (sens -123.0 dBm): +24.21 dB
  Margin di SF10 (sens -132.0 dBm): +33.21 dB
  Margin di SF12 (sens -137.0 dBm): +38.21 dB
```

