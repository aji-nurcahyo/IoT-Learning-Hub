# Chapter 39: Privacy, Threat Modeling & IoT Governance

## Tujuan pembelajaran

Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memahami prinsip tata kelola data IoT (*IoT Data Governance*) dan prinsip perancangan privasi sejak awal (*Privacy by Design*).
2. Menguasai metodologi pemodelan ancaman **STRIDE** (*Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege*).
3. Melakukan kuantifikasi risiko keamanan siber menggunakan skema penilaian **DREAD** (*Damage, Reproducibility, Exploitability, Affected Users, Discoverability*).
4. Mengimplementasikan prinsip **Minimisasi Data** (*Data Minimization*) untuk menyaring *Personally Identifiable Information* (PII) sebelum data dikirim ke awan.
5. Memahami kerangka regulasi perlindungan data pribadi global dan nasional (GDPR, ISO/IEC 27402, UU No. 27 Tahun 2022 tentang Perlindungan Data Pribadi / UU PDP).

## Prasyarat

- Pemahaman arsitektur keamanan IoT, sertifikat TLS, dan enkripsi payload (Chapter 28).
- Konsep dasar protokol jaringan internet dan manajemen identitas perangkat (Chapter 12 & 27).
- Kesadaran terhadap etika rekayasa perangkat lunak dan privasi pengguna akhir.

## Konsep dan teori

### 1. Prinsip Privacy by Design dalam Ekosistem IoT

Perangkat IoT di lingkungan domestik dan perkantoran (kamera pintar, mikrofon asisten suara, pelacak lokasi aset, pemantau suhu ruangan) terus-menerus mengumpulkan data privat pengguna. Sering kali pengembang secara ceroboh mencantumkan nama penghuni, alamat email, atau koordinat GPS presisi di dalam payload telemetri MQTT yang tidak dienkripsi.

Prinsip dasar tata kelola privasi:
1. **Data Minimization (Minimisasi Data)**: Hanya kumpulkan dan simpan data yang mutlak diperlukan untuk fungsi operasional perangkat. Jangan kumpulkan PII jika hanya data suhu yang dibutuhkan.
2. **Storage Limitation (Batas Retensi)**: Tetapkan masa kedaluwarsa data telemetri historis (misal retensi 90 hari, setelah itu dihapus otomatis).
3. **Purpose Limitation (Tujuan Spesifik)**: Data sensor tidak boleh dialihfungsikan untuk tujuan komersial atau pemantauan perilaku tanpa persetujuan eksplisit (*Informed Consent*).

```
   [Raw Physical World]
 (Suara, Gerakan, Lokasi, Suhu)
            |
            v
+-------------------------------------------------------------+
|             Edge Privacy Filter (Minimizer)                 |
|   +-----------------------------------------------------+   |
|   | Whitelist Filter: Hapus Nama, Email, Akun Pribadi    |   |
|   | Agregasi Spasial: Sensor Suhu Kamar -> Rata-rata    |   |
|   +-----------------------------------------------------+   |
+-------------------------------------------------------------+
            |
            v  (Data Higienis & Anonim)
 [Cloud Enterprise Data Lake]
```

### 2. Metodologi Pemodelan Ancaman STRIDE

STRIDE (dikembangkan oleh Microsoft) mengklasifikasikan ancaman keamanan siber sistem tertanam ke dalam enam kategori:

| Kategori | Arti Ancaman | Target Kerentanan IoT | Contoh Solusi Rekayasa |
|---|---|---|---|
| **S**poofing | Pemalsuan identitas | Penyerang menyamar sebagai sensor resmi | Mutual TLS (mTLS) dengan sertifikat X.509 unik. |
| **T**ampering | Modifikasi data ilegal | Manipulasi firmware atau paket data transit | *Secure Boot*, verifikasi signature RSA/ECDSA. |
| **R**epudiation | Penyangkalan aksi | Operator menyangkal perintah remote berbahaya | Log audit kriptografis yang tak dapat diubah (*Signed Logs*). |
| **I**nformation Disclosure | Kebocoran rahasia | Pencurian kunci privat dari SPI flash | *Flash Encryption*, enkripsi transport TLS 1.3. |
| **D**enial of Service | Kelumpuhan layanan | Banjir paket SYN atau payload berlebih | Pembatasan laju (*Rate limiting*), isolasi VLAN. |
| **E**levation of Privilege | Eskalasi hak akses | Peretasan port debugging UART/JTAG fisik | Menonaktifkan JTAG/UART pada firmware produksi (*eFuses*). |

### 3. Kuantifikasi Risiko: Skema DREAD

Untuk memprioritaskan mitigasi ancaman mana yang harus diperbaiki terlebih dahulu, setiap ancaman dinilai berdasarkan 5 parameter DREAD (skala 1–10):
- **D**amage potential (Dampak kerusakan jika berhasil dieksploitasi).
- **R**eproducibility (Kemudahan mengulangi serangan).
- **E**xploitability (Tingkat kemudahan teknis melakukan serangan).
- **A**ffected users (Proporsi perangkat/pengguna yang terdampak).
- **D**iscoverability (Kemudahan menemukan celah keamanan tersebut).

Skor Risiko Akhir dihitung sebagai rata-rata aritmatika:

$$\text{Risk Score} = \frac{D + R + E + A + D}{5}$$

- Skor $\ge 8.0$: **CRITICAL** (Wajib dimitigasi sebelum rilis produk).
- Skor $6.0 - 7.9$: **HIGH** (Wajib dimitigasi pada sprint rekayasa berikutnya).
- Skor $< 6.0$: **MEDIUM / LOW**.

## Latihan

1. **Analisis Ancaman Fisik Port JTAG/UART**:
   Dalam kategori STRIDE *Elevation of Privilege*, jelaskan bagaimana penyerang yang memiliki akses fisik langsung ke papan PCB mikrokontroler dapat memanfaatkan pinheader UART Serial atau interface JTAG untuk membongkar firmware dan mengekstraksi kunci enkripsi. Bagaimana teknik *Hardware eFuse Blowing* pada ESP32 memitigasi risiko ini secara permanen?
2. **Kalkulasi Skor DREAD**:
   Sebuah celah keamanan ditemukan pada web server konfigurasi Wi-Fi perangkat IoT: penyerang dapat melewati login tanpa password (*Bypass Authentication*). Tim keamanan memberikan skor: Damage = 9, Reproducibility = 9, Exploitability = 8, Affected Users = 9, Discoverability = 7. Hitung nilai skor risiko DREAD dan tentukan tingkat keparahannya.
3. **Kepatuhan Regulasi UU PDP Indonesia**:
   Pasal berapakah dalam UU No. 27 Tahun 2022 (UU PDP) yang mewajibkan Pengendali Data Pribadi menerapkan langkah teknis untuk melindungi data dari pemrosesan tidak sah? Apa sanksi hukum bagi pengembang sistem IoT yang lalai mengamankan kebocoran data pengguna?

## Tugas

Kembangkan modul simulasi tata kelola privasi dan pemodelan ancaman Python (`threat_model_governance_sim.py`) yang:
1. Menerapkan registri ancaman berbasis taksonomi STRIDE dan menghitung skor risiko kuantitatif DREAD untuk dua ancaman IoT nyata.
2. Membangun modul filter sanitasi privasi (*PrivacyDataMinimizer*) yang secara otomatis membuang atribut data pribadi sensitif (seperti nama pemilik, email, dan koordinat GPS presisi) dari payload telemetri sebelum diteruskan ke cloud.
3. Membuktikan bahwa payload keluaran murni hanya memuat variabel teknis yang diizinkan (*whitelisted telemetry*).

## Ringkasan

1. Tata kelola data IoT modern mewajibkan penerapan prinsip *Privacy by Design* dan minimisasi data sejak awal perancangan.
2. Pemodelan ancaman STRIDE mengidentifikasi celah kerentanan secara sistematis melintasi seluruh lapisan sistem tertanam.
3. Skoring DREAD memberikan dasar kuantitatif yang objektif untuk memprioritaskan alokasi sumber daya perbaikan keamanan siber.

## Referensi

1. Shostack, A. *Threat Modeling: Designing for Security*. John Wiley & Sons, 2014.
2. ISO/IEC 27402:2023. *Cybersecurity and Privacy — Device Security Requirements for IoT*. International Organization for Standardization, 2023.
3. Republik Indonesia. *Undang-Undang Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi*. Lembaran Negara Republik Indonesia, 2022.
