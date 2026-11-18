# Tugas Rekayasa: Modul B01

## Perancangan Arsitektur Segmentasi Jaringan & Kebijakan IDMZ Pabrik Semen

### 1. Deskripsi Masalah
Sebuah pabrik semen terintegrasi berencana menghubungkan sistem pemantauan kondisi mesin penggiling vertikal (*Vertical Roller Mill*) ke platform analitik prediktif cloud korporat. Manajemen pabrik menuntut agar integrasi cloud ini sama sekali tidak boleh membuka celah serangan malware (seperti ransomware) masuk ke jaringan PLC penggiling semen yang beroperasi pada siklus waktu nyata kritis.

### 2. Instruksi Pengerjaan
1. **Diagram Aliran Data & Zonasi**: Buat diagram hierarki ISA-95/Purdue lengkap dengan penempatan Level 0, 1, 2, 3, IDMZ 3.5, dan Level 4.
2. **Definisi Tabel Firewall IDMZ**: Rancang tabel penyaringan paket untuk External Firewall (IDMZ $\leftrightarrow$ IT) dan Internal Firewall (OT $\leftrightarrow$ IDMZ), memuat Source IP Subnet, Destination IP Subnet, Port/Protokol, Arah, dan Tindakan (ALLOW/DROP).
3. **Mekanisme Replikasi Historian**: Jelaskan bagaimana data deret waktu getaran disalin dari Plant Historian internal ke Replicated Historian IDMZ tanpa membuka port inbound di firewall internal.
4. **Verifikasi Simulasi Perangkat Lunak**: Jalankan skrip [purdue_security_sim.py](src/purdue_security_sim.py), tambahkan minimal 2 skenario uji paket serangan baru (misal: serangan eksploitasi port 44818 Ethernet/IP dari luar), dan laporkan buktinya.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Ketepatan Pemetaan Model Purdue & Zonasi** | 25 | Seluruh aset terpetakan tepat pada level hierarki ISA-95 tanpa pelanggaran batas OT/IT. |
| **Desain Kebijakan Firewall & Isolasi IDMZ** | 25 | Aturan firewall eksplisit, prinsip least privilege terpenuhi, ketiadaan rute langsung IT ke OT. |
| **Arsitektur Replikasi Data & Protokol Industri** | 25 | Desain conduit replikasi data aman, pemilihan protokol tepat (OPC UA / HTTPS), zero write command. |
| **Verifikasi Eksperimental & Laporan Teknis** | 25 | Eksekusi skrip simulasi valid, penambahan skenario uji serangan terbukti diblokir, dokumentasi rapi. |

