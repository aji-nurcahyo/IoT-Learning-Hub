# Latihan Terstruktur: Modul E01

## Latihan Pemahaman Mandiri

1. **Mengapa standar ontologi data terhubung (Linked Data / JSON-LD) seperti FIWARE NGSI-LD sangat penting dalam integrasi sistem IoT perkotaan?**
   - *Jawaban*: Dalam lingkungan kota yang kompleks, dinas-dinas yang berbeda menggunakan vendor perangkat keras yang heterogen dengan format JSON acak yang berbeda nama field-nya. JSON-LD menyematkan konteks semantik global ("@context") yang secara presisi mendefinisikan arti setiap properti, memungkinkan sistem analitik lintas dinas memproses dan menghubungkan data tanpa perlu menulis ulang adaptor konversi untuk setiap vendor baru.

2. **Bagaimana arsitektur 4 gateway paralel dengan reliabilitas individual 90% mampu menghasilkan ketersediaan komposit Four-Nines (99.99%)?**
   - *Jawaban*: Melalui prinsip redundansi independen: paket data yang dipancarkan oleh simpul sensor akan diterima jika minimal salah satu dari 4 gateway beroperasi. Peluang sistem gagal total adalah probabilitas keempat gateway mati secara serentak, yaitu $(1 - 0{,}9)^4 = 0{,}1^4 = 0{,}0001$. Ketersediaan sistem adalah komplemennya: $1 - 0{,}0001 = 0{,}9999$ ($99{,}99%$).
