# Tugas Terbimbing: Pemodelan Ancaman STRIDE & Filter Kepatuhan Privasi IoT

## Deskripsi Tugas

Dalam tugas ini, Anda diminta membangun sistem tata kelola keamanan dan privasi data (*IoT Governance & Privacy Engine*) yang memodelkan analisis ancaman siber berbasis kerangka kerja STRIDE dan skoring risiko DREAD, serta mengimplementasikan filter penyaringan privasi data (*Privacy by Design*) pada payload telemetri.

Tugas ini mewajibkan:
1. Pembuatan modul registri pemodelan ancaman (*ThreatModelRegistry*) yang mengklasifikasikan kerentanan ke dalam taksonomi STRIDE dan menghitung skor risiko kuantitatif DREAD untuk menentukan tingkat keparahan (*CRITICAL*, *HIGH*, *MEDIUM*).
2. Pembuatan modul penyaringan privasi (*PrivacyDataMinimizer*) yang membersihkan rekaman data telemetri mentah dari data sensitif pribadi (*Personally Identifiable Information / PII*) seperti nama pemilik, email, dan koordinat GPS presisi, menyisakan hanya atribut teknis yang diizinkan (*whitelisted*).
3. Verifikasi otomatis skenario mitigasi risiko dan sanitasi data melalui eksekusi modul pengujian Python terpadu.

## Petunjuk Pengumpulan

1. Kode sumber simulasi Python: `public/content/chapter-39/src/threat_model_governance_sim.py`.
2. Laporan analisis teknis yang mencakup tabel registri ancaman STRIDE, lembar kerja skoring DREAD, dan analisis kepatuhan terhadap regulasi UU PDP No. 27/2022.

## Rubrik Penilaian (Total: 100 Poin)

| Kriteria | Bobot | Deskripsi |
|---|:---:|---|
| **Akurasi Pemodelan Ancaman STRIDE & Skoring DREAD** | 35 Poin | Kategori STRIDE terdefinisi tepat, komputasi rata-rata 5 parameter DREAD terbukti akurat, dan pemetaan tingkat keparahan (*severity threshold*) tervalidasi secara konsisten. |
| **Implementasi Filter Minimisasi Data & Higienitas Privasi** | 35 Poin | Modul sanitasi berhasil membuang seluruh atribut data pribadi sensitif (PII), mempertahankan field telemetri yang diizinkan, dan menjamin nol kebocoran identitas personal. |
| **Analisis Kepatuhan Regulasi & Kebijakan Tata Kelola** | 30 Poin | Pembahasan menyajikan analisis mendalam mengenai mitigasi perangkat keras fisik (eFuse/Flash Encryption), batas retensi data, dan kepatuhan terhadap perundang-undangan perlindungan data. |
