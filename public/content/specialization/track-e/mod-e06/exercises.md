# Latihan Terstruktur: Modul E06

## Latihan Pemahaman Mandiri

1. **Strategi Pemulihan Gateway Down**:
   - *Soal*: Jika satu tower seluler kota mati total akibat putusnya pasokan listrik, bagaimana arsitektur redundansi multi-gateway dan LPWAN perkotaan menjamin data sensor kritis tetap sampai ke markas komando?
   - *Jawaban*: Simpul IoT perkotaan berada dalam jangkauan sel tumpang tindih (*overlapping coverage*). Ketika base station primer mati, simpul secara otomatis melakukan retransmisi ke frekuensi alternatif atau gateway sekunder yang mendengarkan kanal bersama. Dengan model ketersediaan paralel komposit $A = 1 - \prod(1 - A_i)$, ketersediaan tautan tetap terjaga di atas 99.9%.

2. **Dampak Masking Privasi H3**:
   - *Soal*: Apakah masking spasial H3 mengurangi efektivitas deteksi dini banjir kota? Jelaskan trade-off teknologinya.
   - *Jawaban*: Tidak. Sensor debit air dan pintu air adalah aset fisik statis milik dinas (bukan individu personal), sehingga koordinat presisi tetap tersimpan di database internal tertutup (akses PUPR). Masking H3 hanya diterapkan pada portal Open Data publik yang diakses masyarakat luas untuk memantau tren genangan tingkat distrik tanpa membuka detail instalasi infrastruktur vital kepada pihak yang tidak berkepentingan.
