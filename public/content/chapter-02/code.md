# Source Code — Chapter 02: Kalkulator Kebutuhan Sistem & Trade-off Edge vs Cloud

Folder `src/` berisi model analitis Python untuk membandingkan arsitektur *Direct-to-Cloud Raw* versus *Edge Gateway Aggregation* pada sistem monitoring suhu terdistribusi (40 node).

## Ringkasan File

- [requirements_budget.py](content/chapter-02/src/requirements_budget.py): Menghitung jumlah paket harian, volume data termasuk *protocol overhead*, kebutuhan *offline buffer* selama gangguan backhaul 6 jam, dan latensi respons darurat.
- [telemetry.csv](content/chapter-02/telemetry.csv): Contoh data ringkasan jendela 60 detik hasil agregasi *Edge* (`source=synthetic`).

## Cara Menjalankan

```sh
python public/content/chapter-02/src/requirements_budget.py
```

## Status Verifikasi

- **Software model (`requirements_budget.py`)**: Dieksekusi nyata pada Python 3.12.10; output tercatat pada `outputs.md`.
- **Hardware / jaringan nyata**: Tidak diuji pada chapter arsitektur ini.

