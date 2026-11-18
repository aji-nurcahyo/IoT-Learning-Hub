# Latihan Terstruktur: Modul E02

## Latihan Pemahaman Mandiri

1. **Mengapa redaman propagasi di area metropolitan padat (COST 231 Hata) pada jarak 2.5 km bernilai sekitar 34 dB lebih tinggi dibandingkan perhitungan ruang bebas (FSPL)?**
   - *Jawaban*: Pada lingkungan perkotaan padat, gelombang elektromagnetik tidak merambat secara bebas tanpa hambatan. Sebagian besar energi gelombang diserap oleh material beton, dipantulkan berulang kali oleh fasad kaca gedung (*multipath clutter*), dan dibiaskan secara tidak sempurna melintasi tepi atap (*diffraction loss*), menghasilkan pelemahan daya akumulatif sebesar $34	ext{ dB}$ (faktor pelemahan daya lebih dari 2500 kali lipat).

2. **Berapa besar fading margin yang harus disisipkan pada link budget radio untuk menjamin tingkat keandalan penerimaan paket 99% pada kanal multipath Rayleigh murni?**
   - *Jawaban*: Sekitar $+19{,}98	ext{ dB}$ (dibulatkan menjadi $+20	ext{ dB}$). Nilai ini diturunkan secara analitis dari integral fungsi kerapatan probabilitas Rayleigh di mana probabilitas kedalaman redaman melampaui ambang batas dibatasi maksimum $1%$ ($P_{	ext{out}} = 0{,}01$).
