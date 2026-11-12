# Latihan Bertingkat — Chapter 02

## Bagian A — Pertanyaan Konseptual

1. Jelaskan perbedaan utama antara model arsitektur **3-lapis** dan **5-lapis**. Mengapa pemisahan *Edge/Middleware Layer* sangat penting pada sistem IoT lapangan?
2. Ubah pernyataan kebutuhan yang kabur berikut menjadi **Non-Functional Requirements** yang terukur dan dapat diuji:
   - *"Sensor harus mengirim data dengan cepat."*
   - *"Node lapangan harus hemat baterai."*
   - *"Sistem harus tetap aman jika internet mati."*
3. Kapan pemrosesan di *Cloud* lebih unggul dibanding *Edge*, dan kapan *Edge* wajib didahulukan? Berikan masing-masing dua kriteria teknis.

## Bagian B — Applied Engineering Problems

4. **Perancangan System Boundary & Block Diagram (Smart Irrigation)**:
   Sebuah kebun percobaan seluas 2 hektar memiliki 12 zona tanaman. Setiap zona memiliki sensor kelembaban tanah dan katup air DC 12 V (melalui driver). Terdapat satu *Gateway* bertenaga listrik AC-DC di pos jaga yang terhubung ke internet via router seluler.
   - Gambarkan *block diagram* 5 lapis beserta label protokol/sinyal antar-blok.
   - Tentukan *system boundary* untuk kondisi darurat: jika tanah terlalu kering atau pipa bocor (katup terbuka terus $> 15\text{ menit}$), komponen mana yang harus memutus aliran air?

5. **Analisis Anggaran Bandwidth & Offline Buffer**:
   Sebuah jaringan pemantau ruang server memiliki $M = 20$ node. Setiap node mengirim paket dengan payload $B = 180\text{ byte}$ dan *protocol overhead* $H = 64\text{ byte}$ setiap $\Delta t = 15\text{ detik}$ langsung ke server melalui *Gateway*.
   - Hitung volume *wire* total per hari (MiB/hari).
   - Hitung kapasitas *offline buffer* minimum (dalam MiB) pada *Gateway* jika backhaul internet berpotensi putus selama $T_{\text{outage}} = 12\text{ jam}$ (hitung berdasarkan ukuran payload $B$).
   - Jika *Gateway* meringkas data menjadi 1 paket agregat berukuran $240\text{ byte}$ per node setiap $120\text{ detik}$, berapa persen penghematan volume *wire* hariannya?

## Bagian C — Eksplorasi Model Software (`requirements_budget.py`)

6. Jalankan [`requirements_budget.py`](content/chapter-02/src/requirements_budget.py):
   ```sh
   python public/content/chapter-02/src/requirements_budget.py
   ```
   **Mini Challenge**: Modifikasi salinan skrip untuk menguji skenario $M = 100$ node dengan kuota seluler maksimum **500 MiB per bulan** (30 hari). Tentukan $\Delta t_{\text{uplink}}$ minimum (dalam detik) agar arsitektur *Edge Aggregation* tetap berada di bawah kuota tersebut (asumsikan $B = 220\text{ B}, H = 64\text{ B}$).

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **3-Lapis vs 5-Lapis**: Model 5-lapis memisahkan *Edge/Middleware* (agregasi, *store-and-forward*, kontrol lokal) dari jaringan transport, serta memisahkan *Platform* (broker, TSDB) dari *Application* (UI/bisnis). Pemisahan *Edge* krusial untuk keandalan *offline* dan efisiensi *bandwidth*.
2. **Konversi ke Non-Functional Requirements Terukur**:
   - *"Latensi deteksi kejadian kritis hingga aktivasi aktuator lokal maksimum $50\text{ ms}$; pengiriman telemetry ke broker maksimum $5\text{ detik}$ dalam kondisi jaringan normal."*
   - *"Konsumsi arus rata-rata node maksimum $0{,}5\text{ mA}$ sehingga baterai $3000\text{ mAh}$ bertahan minimal 180 hari pada interval kirim 10 menit."*
   - *"Saat koneksi WAN putus hingga 6 jam, Gateway menyimpan seluruh ringkasan telemetry pada ring buffer lokal dan tetap mengeksekusi alarm lokal."*
3. **Cloud vs Edge**: Cloud unggul untuk arsip jangka panjang, korelasi lintas wilayah, dan pelatihan model berat; Edge wajib untuk kontrol *safety* berlatensi rendah ($< 50\text{ ms}$), operasi otonom saat internet putus, dan reduksi *bandwidth*.
4. **Smart Irrigation**: Batas pengaman (*fail-safe timer* maksimum 15 menit bukaan katup) harus berada di level *Node/Edge Controller* lokal agar kebun tidak kebanjiran bila koneksi ke server terputus.
5. **Perhitungan 20 Node ($\Delta t = 15\text{ s}, B=180, H=64$)**:
   - Paket/hari = $20 \times (86400/15) = 115.200\text{ paket/hari}$.
   - $V_{\text{wire}} = 115.200 \times 244 = 28.108.800\text{ B} \approx 26{,}81\text{ MiB/hari}$.
   - Buffer 12 jam = $20 \times (12 \times 3600 / 15) \times 180 = 10.368.000\text{ B} \approx 9{,}89\text{ MiB}$.
   - Dengan agregasi $\Delta t = 120\text{ s}$ ($B=240, H=64 \Rightarrow 304\text{ B}$): paket/hari = $20 \times 720 = 14.400$; $V_{\text{wire}} = 14.400 \times 304 = 4.377.600\text{ B} \approx 4{,}17\text{ MiB/hari}$ (penghematan $\approx 84{,}4\%$).

</details>

