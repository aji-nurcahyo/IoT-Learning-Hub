# Tugas & Rubrik — Chapter 02

## Skenario Tugas: Desain Arsitektur IoT dari Kebutuhan Sistem

Anda ditugaskan merancang arsitektur untuk **salah satu** skenario kebutuhan berikut:
- **Skenario 1 — Monitoring Cold-Chain Gudang Vaksin**: 30 ruang pendingin, target suhu $2\dots 8\,^\circ\text{C}$, butuh alarm lokal $< 100\text{ ms}$ jika pintu terbuka $> 2\text{ menit}$ atau suhu keluar rentang, plus audit data 12 bulan.
- **Skenario 2 — Pemantauan BTS & Shelter Telekomunikasi**: 15 menara di daerah dengan koneksi 4G intermiten, memantau suhu kabinet, tegangan baterai, dan status pintu akses, dengan kuota data maksimal 1 GiB/bulan untuk seluruh armada.

## Dokumen yang Harus Dikumpulkan

Buat dokumen desain sistem (3–5 halaman, format Markdown atau PDF) yang memuat:

1. **Tabel Functional & Non-Functional Requirements**: Minimal 5 kebutuhan fungsional dan 6 dimensi kebutuhan non-fungsional lengkap dengan **angka target terukur**.
2. **Arsitektur 5-Lapis & System Boundaries**: Petakan komponen pada setiap lapisan (*Device, Network, Edge, Platform, Application*) dan gambar **Use-Case Diagram** serta **Block Diagram** dengan label protokol/antarmuka.
3. **Analisis Trade-Off Edge vs Cloud & Anggaran Kapasitas**: Hitung volume *wire* harian/bulanan ($B + H$) dan kapasitas *offline buffer* pada kondisi gangguan 6–12 jam, serta jelaskan alasan pemilihan arsitektur.
4. **Matriks Skenario Kegagalan & Mitigasi**: Minimal 3 skenario kegagalan (WAN putus, buffer penuh, catu daya terganggu) beserta respons *fail-safe* dan rujukan primer.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Spesifikasi kebutuhan fungsional & non-fungsional** | **25** | Seluruh kebutuhan terukur secara numerik (latensi, daya, bandwidth, jangkauan, ketersediaan, biaya) dan konsisten dengan skenario. |
| **Desain arsitektur 5-lapis & system boundaries** | **25** | Pembagian tanggung jawab 5 lapisan tepat, batas sistem jelas, serta *use-case* dan *block diagram* mudah dipahami. |
| **Analisis trade-off Edge vs Cloud & perhitungan kapasitas** | **25** | Keputusan penempatan logika di Edge/Cloud beralasan kuat dan perhitungan *bandwidth* serta *offline buffer* tepat. |
| **Skenario kegagalan, fail-safe & referensi** | **25** | Penanganan gangguan koneksi/daya/buffer realistis dengan perilaku *fail-safe* dan rujukan teknis valid. |

