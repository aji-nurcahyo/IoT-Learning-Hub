# Latihan Chapter 39: Privacy, Threat Modeling & IoT Governance

## Latihan Konseptual

1. **Prinsip Data Minimization**:
   Mengapa pengumpulan data telemetri yang "terlalu lengkap" (misalnya menyertakan informasi identitas pengguna, tipe router rumah tangga, dan koordinat GPS berpresisi tinggi) justru menjadi liabilitas keamanan dan hukum yang besar bagi perusahaan pengembang IoT? Jelaskan prinsip *Data Minimization* dalam kerangka regulasi GDPR dan UU PDP No. 27/2022.

2. **Dinamika Pemodelan Ancaman STRIDE**:
   Pilihlah sebuah arsitektur sistem kunci pintu pintar nirkabel (*Smart Door Lock*), lalu identifikasi minimal 3 skenario ancaman spesifik yang masing-masing merepresentasikan kategori:
   - **S**poofing
   - **T**ampering
   - **E**levation of Privilege
   Sebutkan pula mekanisme rekayasa mitigasi yang relevan untuk masing-masing ancaman tersebut.

3. **Metodologi Skoring Risiko DREAD**:
   Jelaskan mengapa skoring DREAD menggunakan nilai rata-rata dari lima parameter (*Damage, Reproducibility, Exploitability, Affected Users, Discoverability*) untuk menentukan tingkat keparahan risiko ancaman siber. Apa perbedaan tindakan rekayasa antara ancaman berkategori **CRITICAL** ($\ge 8.0$) dengan ancaman berkategori **MEDIUM** ($< 6.0$)?

## Latihan Praktik & Perhitungan

1. **Kalkulasi Skor Risiko DREAD**:
   Sebuah kerentanan ditemukan pada proses pembaruan firmware (OTA) node sensor luar ruangan: perangkat menerima file binary firmware tanpa memverifikasi tanda tangan digital (*No Signature Verification*). Tim rekayasa memberikan estimasi penilaian parameter sebagai berikut:
   - Damage: $10$ (Perangkat dapat diambil alih total menjadi botnet).
   - Reproducibility: $9$ (Serangan dapat diulang setiap kali perangkat meminta update).
   - Exploitability: $7$ (Memerlukan kemampuan memalsukan respon DNS lokal).
   - Affected Users: $10$ (100% dari seluruh armada node di lapangan terdampak).
   - Discoverability: $8$ (Protokol HTTP tanpa enkripsi mudah diinspeksi dengan Wireshark).
   
   *Instruksi*:
   - Hitung nilai *Risk Score* akhir DREAD.
   - Tentukan kategori tingkat keparahan (*Severity Level*).
   - Jelaskan langkah mitigasi kriptografis yang mutlak harus dipasang untuk menurunkan skor tersebut ke level terendah.

2. **Perancangan Modul Sanitasi Privasi Python**:
   Rancang fungsi pembersih payload telemetri Python yang menerima dictionary data sensor mentah dan mengembalikan data bersih yang hanya mempertahankan field yang terdaftar dalam *whitelist*, membuang field berbau PII secara otonom.
