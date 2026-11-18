# Latihan Terstruktur: Modul E03

## Latihan Pemahaman Mandiri

1. **Pemilihan Teknologi**:
   - *Soal*: Manakah teknologi yang paling tepat untuk sistem pelacakan armada bus kota real-time: NB-IoT atau LTE-M? Jelaskan secara ilmiah.
   - *Jawaban*: LTE-M (Cat-M1). NB-IoT tidak mendukung handover mulus saat perangkat bergerak melintasi batas sel tower seluler. NB-IoT harus memutus koneksi dan melakukan registrasi ulang yang memicu latensi tinggi dan konsumsi energi besar. LTE-M mendukung seamless handover dan throughput 1 Mbps yang ideal untuk telemetri posisi kendaraan yang dinamis.

2. **Dampak Pemanjangan Timer T3324**:
   - *Soal*: Apa akibatnya jika timer T3324 diatur terlalu besar (misalnya 120 detik) pada sensor parkir nirkabel?
   - *Jawaban*: Perangkat akan tertahan pada status Active Idle mendengarkan kanal radio selama 2 menit setiap selesai transmisi dengan daya sekitar 10 mW, alih-alih lelap ke status PSM (15 uW). Hal ini akan menguras baterai dengan cepat dan menggagalkan target operasional multi-tahun.
