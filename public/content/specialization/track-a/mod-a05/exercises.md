# Latihan Terstruktur: Modul A05

## Latihan Pemahaman Mandiri

1. **Mengapa kunci pintu darurat pada tangga kebakaran gedung bertingkat wajib menerapkan mekanisme fail-safe (unlocked on power loss) dan bukan fail-secure?**
   - *Jawaban*: Pada saat kebakaran hebat, pasokan listrik gedung sering kali terputus akibat korsleting atau pemutusan darurat oleh petugas pemadam kebakaran. Jika pintu bersifat *fail-secure*, pintu akan terkunci mati dan menjebak penghuni di dalam koridor berasap tebal, mengakibatkan korban jiwa fatal. Mekanisme *fail-safe* menjamin pintu langsung membuka bebas tanpa hambatan saat listrik padam.

2. **Bagaimana sirkuit loop terawasi dengan resistor EOL dapat membedakan kabel putus dari alarm kebakaran aktif?**
   - *Jawaban*: Saat sensor mendeteksi api, kontak sakelar terhubung singkat ($R approx 0$) menghasilkan tegangan tinggi pada resistor pengukur ($V_{	ext{sense}} approx 24	ext{ V}$). Namun jika kabel putus terpotong, rangkaian menjadi terbuka ($R 	o infty$) dan tidak ada arus yang mengalir, menghasilkan tegangan mendekati nol ($V_{	ext{sense}} approx 0	ext{ V}$), sehingga panel dapat membedakan status *Trouble* dari *Alarm*.
