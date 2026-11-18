# Latihan Terstruktur: Modul A02

## Latihan Pemahaman Mandiri

1. **Mengapa sensor PIR tidak mampu mendeteksi orang yang sedang tertidur lelap di dalam ruangan, sementara radar mmWave mampu mendeteksinya?**
   - *Jawaban*: Sensor PIR hanya merespons perubahan fluks inframerah ketika sumber panas berpindah melintasi batas optik segmen lensa Fresnel yang berbeda. Orang yang tertidur lelap tidak menghasilkan perpindahan spasial tubuh. Sebaliknya, radar mmWave memancarkan gelombang elektromagnetik dan mendeteksi pergeseran fase mikroskopik ($< 0{,}5	ext{ mm}$) akibat gerakan naik-turun dinding dada saat bernapas.

2. **Bagaimana penerapan histeresis deadband melindungi aktuator katup ventilasi mekanikal?**
   - *Jawaban*: Histeresis mencegah osilasi buka-tutup berulang frekuensi tinggi (*actuator chattering*) di sekitar nilai ambang batas kendali, sehingga motor servo tidak terus-menerus bekerja bolak-balik saat fluktuasi derau pembacaan sensor bernilai kecil, memperpanjang usia mekanikal roda gigi aktuator.
