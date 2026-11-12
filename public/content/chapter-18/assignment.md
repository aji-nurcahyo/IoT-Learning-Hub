# Tugas & Rubrik — Chapter 18: Perancangan Jaringan LoRaWAN & Analisis ToA

## Skenario Tugas

Sebuah kawasan perkebunan penelitian seluas radius $2{,}5\text{ km}$ memerlukan 30 titik sensor stasioner (suhu udara, kelembapan tanah, dan tegangan baterai) bertenaga baterai yang mengirim laporan setiap 15 menit.

## Instruksi Pengerjaan

1. **Pemisahan Lapisan & Arsitektur**:
   - Gambarkan alur data dari *End-Device* $\rightarrow$ *Gateway* $\rightarrow$ *Network Server* $\rightarrow$ *Application Server*, tentukan **Class LoRaWAN** (`A`/`B`/`C`) beserta alasan teknisnya, serta pilih metode aktivasi (**OTAA** vs **ABP**) dan kebijakan **ADR**.
2. **Desain Payload Biner & Kalkulasi `ToA`**:
   - Rancang format *FRMPayload* biner $\le 16\text{ byte}$ (+13 byte header MAC LoRaWAN minimum) sehingga total frame $\le 29\text{ byte}$.
   - Gunakan dan modifikasi [`lora_airtime_budget.py`](content/chapter-18/src/lora_airtime_budget.py) untuk menghitung `ToA` pada `SF7`, `SF9`, dan `SF11` (`BW = 125 kHz`), serta bandingkan dampaknya jika Anda memaksakan mengirim string JSON `55 byte`.
3. **Analisis Link Budget & Penempatan Gateway**:
   - Hitung estimasi $P_{\text{rx}}$ dan *margin* pada jarak terjauh $2{,}5\text{ km}$ dengan mencantumkan asumsi $P_{\text{tx}}$, penguatan antena, rugi kabel, dan *fading margin* vegetasi kebun.
4. **Checklist Verifikasi Parameter Regional**:
   - Susun tabel verifikasi berisi item apa saja yang wajib dicek pada dokumen **LoRa Alliance Regional Parameters (RP2)** dan peraturan regulator spektrum negara tempat deployment sebelum perangkat diaktifkan secara fisik (pita frekuensi, *sub-band*, batas *EIRP*, dan aturan waktu udara/*dwell time*).

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Poin | Indikator Keberhasilan |
| --- | :---: | --- |
| Ketepatan arsitektur LoRa PHY vs LoRaWAN | 25 | Membedakan PHY & MAC dengan benar; pemilihan Class A, OTAA, dan ADR beralasan kuat. |
| Desain payload biner & kalkulasi ToA | 30 | Format biner terdokumentasi byte-per-byte; perbandingan `ToA` biner vs JSON akurat dengan skrip Python. |
| Analisis link budget & dampak SF | 25 | Perhitungan FSPL + margin redaman konsisten; menjelaskan trade-off baterai, jangkauan, dan tabrakan. |
| Kepatuhan regulasi regional & kejujuran bukti | 20 | Menyertakan rujukan resmi LoRa Alliance RP2 / regulator tanpa mengarang batas legal; status uji jujur. |
| **Total** | **100** | |

