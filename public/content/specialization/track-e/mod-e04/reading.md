# Modul E04 — Municipal Network Contention, Slotted ALOHA & Priority Queueing

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memodelkan kontensi medium akses acak perkotaan menggunakan teori Pure ALOHA dan Slotted ALOHA.
2. Menghitung probabilitas tabrakan paket (packet collision) pada berbagai tingkat beban trafik perkotaan.
3. Merancang mekanisme antrean prioritas non-preemptive M/G/1 untuk memisahkan paket darurat dan paket rutin.
4. Membuktikan kepatuhan Service Level Agreement (SLA) latensi darurat (< 80 ms) di bawah utilisasi sistem tinggi.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 11, Chapter 23, Chapter 24.
- Modul Jalur Peminatan Prasyarat: Modul E01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Dinamika Kontensi Kanal Akses Acak Skala Kota
Dalam topologi nirkabel perkotaan terdistribusi, jutaan sensor memancarkan paket data secara asinkron tanpa negosiasi reservasi waktu tersentralisasi. Fenomena benturan sinyal (*packet collision*) merupakan konsekuensi fisik utama:
- Jika dua simpul memancarkan paket pada frekuensi yang sama dalam jendela waktu yang bertumpang tindih, penerima di stasiun pangkalan (gateway) akan mengalami degradasi rasio Carrier-to-Interference ($C/I$) yang merusak data.
- Protokol Pure ALOHA mentransmisikan paket secara instan, menghasilkan batas teoritis throughput maksimum $18{,}4\%$.
- Protokol Slotted ALOHA mendisiplinkan transmisi hanya pada batas awal slot waktu diskret, menggandakan efisiensi kanal menjadi $36{,}8\%$.

### 2. Teori Antrean Non-Preemptive Priority M/G/1
Pada tingkat gateway dan pemroses broker perkotaan, paket telemetri memiliki urgensi yang berbeda drastis:
- **Kelas 1 (High Priority / Emergency)**: Peringatan kebocoran gas alam, alarm gempa bumi, sirene banjir BPBD.
- **Kelas 2 (Low Priority / Background)**: Pembacaan meteran air rutin, sensor kelembapan taman kota, status tong sampah.
Dengan arsitektur **Non-Preemptive Priority M/G/1**, gateway mendahulukan paket Kelas 1 setiap kali server selesai melayani paket aktif, tanpa menghentikan transmisi paket aktif di tengah jalan (*non-preemption* menjamin efisiensi energi transmisi).

### 3. Landasan Matematis Kontensi & Waktu Tunggu Antrean

1. **Persamaan Throughput Kanal Akses Acak**:
   - Pure ALOHA:
     $$
     S_{\text{pure}} = G \cdot e^{-2G}
     $$
   - Slotted ALOHA:
     $$
     S_{\text{slotted}} = G \cdot e^{-G}
     $$
   dengan $G$ adalah beban trafik yang ditawarkan (*offered traffic load* dalam satuan Erlang).

2. **Waktu Tunggu Antrean Prioritas Non-Preemptive M/G/1**:
   - Utilisasi total:
     $$
     \rho = \rho_1 + \rho_2 = (\lambda_1 + \lambda_2) E[X]
     $$
   - Waktu layanan residual rata-rata ($R$):
     $$
     R = \frac{1}{2} (\lambda_1 + \lambda_2) E[X^2]
     $$
   - Latensi total Kelas 1 (Darurat):
     $$
     W_{q, 1} = \frac{R}{1 - \rho_1} \implies W_1 = W_{q, 1} + E[X]
     $$
   - Latensi total Kelas 2 (Telemetri Rutin):
     $$
     W_{q, 2} = \frac{R}{(1 - \rho_1)(1 - \rho)} \implies W_2 = W_{q, 2} + E[X]
     $$

## Latihan

## Latihan Pemahaman Mandiri

1. **Beban Trafik Kritis Slotted ALOHA**:
   - *Soal*: Mengapa saat beban trafik $G$ melampaui 1.0 Erlang, throughput Slotted ALOHA mengalami penurunan tajam?
   - *Jawaban*: Saat beban $G > 1{,}0$, laju kedatangan paket melampaui kapasitas slot waktu kanal. Probabilitas dua atau lebih perangkat memancarkan paket pada slot yang sama meningkat eksponensial ($P_{\text{collision}} = 1 - e^{-G}$), sehingga sebagian besar slot waktu terisi oleh tabrakan yang merusak paket alih-alih transmisi sukses.

2. **Non-Preemptive vs Preemptive Queueing**:
   - *Soal*: Mengapa arsitektur radio nirkabel memilih model antrean Non-Preemptive dibandingkan Preemptive?
   - *Jawaban*: Dalam sistem transmisi RF, membatalkan transmisi paket yang sedang dipancarkan di udara akan menyebabkan paket tersebut rusak sebagian di sisi penerima, menyia-nyiakan daya baterai pemancar dan memerlukan retransmisi total. Non-preemptive membiarkan paket aktif selesai dipancarkan (hanya memakan beberapa milidetik), lalu langsung melayani paket darurat berikutnya.

## Tugas

## Penugasan Mandiri: Pemodelan Antrean Multi-Prioritas Gateway Kota

1. Perluas fungsi simulasi M/G/1 untuk mendukung 3 kelas prioritas (Emergency, Control Command, Telemetry).
2. Lakukan uji stres dengan meningkatkan utilisasi total $\rho$ dari 0.50 hingga 0.98.
3. Analisis pada utilisasi berapa latensi Kelas 3 mulai mengalami ketidakstabilan eksponensial (*queue explosion*).
4. Buat algoritma pembatasan laju (*rate-limiting*) pada simpul telemetri rutin untuk mencegah kolapsnya antrean gateway saat terjadi bencana kota.

## Ringkasan
- Modul E04 memberikan pemahaman mendalam dan terapan mengenai Municipal Network Contention, Slotted ALOHA & Priority Queueing pada tingkat kedalaman L2: Undergraduate Complete.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [municipal_contention_queue_sim.py](src/municipal_contention_queue_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Kleinrock, L. - Queueing Systems, Volume II: Computer Applications, [https://www.wiley.com/en-us/Queueing+Systems%2C+Volume+2%2C+Computer+Applications-p-9780471491118](https://www.wiley.com/en-us/Queueing+Systems%2C+Volume+2%2C+Computer+Applications-p-9780471491118) (diperiksa 2026-11-18).
2. Abramson, N. - The ALOHA System: Another Alternative for Computer Communications, [https://doi.org/10.1145/1478462.1478502](https://doi.org/10.1145/1478462.1478502) (diperiksa 2026-11-18).
