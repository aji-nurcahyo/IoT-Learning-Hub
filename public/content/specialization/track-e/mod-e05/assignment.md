# Tugas Rekayasa & Rubrik: Modul E05

## Penugasan Mandiri: Pemodelan Geofence Multi-Zona & Indeksasi H3

1. Buat script yang mendefinisikan tiga tingkatan zona bahaya banjir (Zona Bahaya Merah, Zona Waspada Kuning, Zona Aman Hijau).
2. Lakukan evaluasi ray-casting terhadap 1.000 titik sampel koordinat acak di wilayah perkotaan.
3. Hitung persentase simpul yang berada di masing-masing zona banjir.
4. Lakukan agregasi kepadatan sensor per sel H3 dan visualisasikan peta panas (heatmap) konsentrasi aset kota.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Implementasi Formula Haversine** | 30 | Akurasi perhitungan jarak lingkaran besar pada elipsoid WGS84 |
| **Algoritma Ray-Casting PiP** | 40 | Kebenaran logika deteksi batas dalam/luar poligon geofence |
| **Masking Privasi Spasial H3** | 30 | Keberhasilan kuantisasi spasial untuk perlindungan privasi publik |
