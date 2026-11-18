# Latihan Terstruktur: Modul E04

## Latihan Pemahaman Mandiri

1. **Beban Trafik Kritis Slotted ALOHA**:
   - *Soal*: Mengapa saat beban trafik $G$ melampaui 1.0 Erlang, throughput Slotted ALOHA mengalami penurunan tajam?
   - *Jawaban*: Saat beban $G > 1{,}0$, laju kedatangan paket melampaui kapasitas slot waktu kanal. Probabilitas dua atau lebih perangkat memancarkan paket pada slot yang sama meningkat eksponensial ($P_{\text{collision}} = 1 - e^{-G}$), sehingga sebagian besar slot waktu terisi oleh tabrakan yang merusak paket alih-alih transmisi sukses.

2. **Non-Preemptive vs Preemptive Queueing**:
   - *Soal*: Mengapa arsitektur radio nirkabel memilih model antrean Non-Preemptive dibandingkan Preemptive?
   - *Jawaban*: Dalam sistem transmisi RF, membatalkan transmisi paket yang sedang dipancarkan di udara akan menyebabkan paket tersebut rusak sebagian di sisi penerima, menyia-nyiakan daya baterai pemancar dan memerlukan retransmisi total. Non-preemptive membiarkan paket aktif selesai dipancarkan (hanya memakan beberapa milidetik), lalu langsung melayani paket darurat berikutnya.
