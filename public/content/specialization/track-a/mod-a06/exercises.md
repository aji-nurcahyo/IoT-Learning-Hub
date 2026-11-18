# Latihan Terstruktur: Modul A06

## Latihan Pemahaman Mandiri

1. **Mengapa kemampuan beroperasi mandiri secara lokal (Local-First Resilience) menjadi kriteria penerimaan wajib pada capstone pengontrol gedung cerdas (SATC-A02)?**
   - *Jawaban*: Dalam gedung perkantoran atau fasilitas publik, kegagalan koneksi internet luar kota (WAN) tidak boleh melumpuhkan kontrol suhu ruangan, ventilasi udara segar, maupun lampu tangga darurat. Sistem kendali lokal berbasis Matter/Thread menjamin seluruh otomasi zona tetap berfungsi normal tanpa risiko mati total akibat gangguan penyedia layanan internet.

2. **Bagaimana algoritma peak-shaving membedakan beban yang boleh dimatikan dari beban yang tidak boleh disentuh?**
   - *Jawaban*: Melalui hierarki klasifikasi tier beban: Tier 1 (beban kritis seperti sistem server dan keselamatan darurat) memiliki proteksi absolut dan tidak pernah dipadamkan, sedangkan Tier 3 (beban non-kritis seperti water heater dan pendingin ruang lobi/koridor) diprogram untuk dilepas terlebih dahulu saat daya total mendekati batas kapasitas trafo gedung.
