# Latihan Terstruktur: Modul C04

## Latihan Pemahaman Mandiri

1. **Mengapa teknologi baterai Lithium Iron Phosphate ($	ext{LiFePO}_4$) lebih dipilih untuk stasiun IoT pertanian tropis dibandingkan Lithium-Cobalt Oxide ($	ext{LiCoO}_2$)?**
   - *Jawaban*: Sel $	ext{LiFePO}_4$ memiliki ikatan kimia kovalen $	ext{P}-	ext{O}$ yang jauh lebih stabil, tahan terhadap suhu tinggi hingga $60^circ	ext{C}$ tanpa resiko *thermal runaway* (terbakar/meledak di bawah sinar matahari langsung), memiliki siklus hidup lebih panjang ($> 2000$ siklus), dan kurva pelepasan tegangan yang sangat datar di sekitar $3{,}2	ext{ V}$.

2. **Apa yang menyebabkan osilasi brownout pada mikrokontroler saat catu daya kekurangan daya penyimpan?**
   - *Jawaban*: Saat mikrokontroler bangun dari mode sleep dan memulai transmisi, arus meningkat tajam sehingga resistansi internal sumber daya memicu penurunan tegangan di bawah ambang batas *Brownout Detector* (BOD). Mikrokontroler reset seketika, arus turun, tegangan naik kembali, mikrokontroler bangun lagi, dan siklus kegagalan ini berulang tanpa akhir hingga baterai rusak total.
