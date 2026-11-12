# Tugas & Rubrik — Chapter 01

## Skenario Tugas: Pemetaan Sistem IoT End-to-End

Pilih **satu** studi kasus berikut:
1. Pemantauan suhu dan daya cadangan pada **kabinet BTS telekomunikasi**.
2. Pemantauan kelembaban tanah dan kendali irigasi pada **rumah kaca (*smart agriculture*)**.
3. Pemantauan kualitas udara atau tinggi muka air untuk **peringatan dini lingkungan**.

## Instruksi Pengerjaan

Susun dokumen rancangan konseptual (format Markdown atau PDF maksimal 4 halaman) yang memuat:

1. **Identifikasi Konteks & Batas Sistem**: Jelaskan tujuan sistem, batas antara *Embedded System* lokal dan layanan jaringan, serta mengapa kasus tersebut memerlukan arsitektur IoT.
2. **Pemetaan 6 Komponen Ekosistem**: Jabarkan pilihan logis untuk *Sensor*, *Embedded Node*, *Actuator*, *Connectivity*, *Gateway* (atau alasan jika tidak terpisah), dan *Platform/Application*.
3. **Diagram Alur Data & Contoh Payload Sintetis**: Buat diagram blok aliran *uplink* dan *downlink*, serta sertakan minimal satu contoh payload JSON berlabel `"source": "synthetic"` dengan satuan eksplisit pada setiap field.
4. **Estimasi Beban Data**: Tentukan jumlah node $M$, ukuran payload $B$, dan interval $\Delta t$, lalu hitung $N_{\text{hari}}$ dan $V_{\text{hari}}$.
5. **Analisis Risiko, Fail-Safe & Referensi**: Identifikasi minimal dua skenario kegagalan (jaringan putus, data sensor rusak) beserta perilaku *fail-safe* lokal dan pertimbangan keamanan dasar (merujuk NISTIR 8259).

## Kriteria Penerimaan (Acceptance Criteria)

- Seluruh 6 komponen terpetakan konsisten dengan alur *uplink* dan *downlink*.
- Payload sintetis tidak mengklaim sebagai pembacaan hardware nyata dan menyertakan satuan eksplisit.
- Perhitungan volume data harian dituliskan lengkap dengan langkah dan satuan.
- Terdapat pemisahan jelas antara aksi darurat lokal dan pemantauan jarak jauh.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Pemetaan komponen ekosistem** | **25** | Ketepatan membedakan dan memetakan Sensor, Embedded Node, Actuator, Connectivity, Gateway, dan Platform pada kasus pilihan. |
| **Analisis alur data uplink & downlink** | **25** | Alur dua arah digambarkan jelas; payload JSON sintetis terstruktur dengan `device_id`, `seq`, dan satuan eksplisit. |
| **Estimasi beban data & batasan teknis** | **25** | Perhitungan paket/volume harian akurat serta analisis dampak interval pengiriman dan skenario kegagalan jaringan. |
| **Kejelasan diagram, keselamatan & referensi** | **25** | Diagram blok terbaca rapi, mekanisme *fail-safe* lokal dijelaskan, dan sumber rujukan primer dicantumkan valid. |

