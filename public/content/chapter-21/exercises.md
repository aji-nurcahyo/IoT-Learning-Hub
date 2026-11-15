# Latihan Soal & Praktik — Chapter 21

## Bagian A — Soal Konseptual

1. **Klasifikasi Pesan IoT**:
   Klasifikasikan masing-masing skenario pertukaran data berikut ke dalam kategori *Telemetry*, *Event*, *Command*, atau *Device State*:
   - a. Node cuaca mengirimkan pembacaan intensitas radiasi matahari ($W/m^2$) setiap 1 menit.
   - b. Sistem cloud mengirim instruksi pembaruan ambang batas suhu maksimal ke node pendingin ruang server.
   - c. Sensor akselerometer mendeteksi benturan mekanis melebihi $5g$ pada boks kargo logistik.
   - d. Node melaporkan parameter konfigurasi firmware versi `v2.1.0` yang sedang aktif setelah booting.
2. **Kelemahan Penggunaan Waktu Penerimaan (*Ingestion Time*)**:
   Jelaskan risiko analitik deret waktu jika arsitektur IoT Anda tidak menyertakan stempel waktu penangkapan data ($t_{\text{capture}}$) dan hanya mengandalkan waktu kedatangan paket di server cloud ($t_{\text{server}}$), khususnya ketika gateway edge mengalami pemutusan koneksi internet selama 2 jam dan mengirimkan akumulasi buffer data secara simultan (*burst drain*).
3. **Idempotensi pada Perintah Aktuasi**:
   Sebuah perintah kontrol dikirimkan dari aplikasi ponsel untuk membuka pintu gerbang otomatis.
   - Mengapa perintah berbentuk `{"action": "toggle_gate"}` rentan terhadap bahaya keamanan jika terjadi transmisi ulang jaringan?
   - Bagaimana Anda mengubah rancangan perintah tersebut agar memenuhi prinsip *idempotent action*?

## Bagian B — Soal Praktik Komputasi

1. **Kalkulasi Bandwidth & Biaya Payload**:
   Sebuah armada terdiri atas $500$ unit perangkat pelacak logistik pintar. Setiap perangkat mengirimkan laporan telemetri setiap $15\text{ detik}$ selama 24 jam non-stop ($86.400\text{ detik/hari}$).
   - a. Jika payload menggunakan format JSON biasa dengan ukuran rata-rata $180\text{ byte}$ per paket, hitung total volume konsumsi data bulanan (30 hari) untuk seluruh armada (dalam gigabyte).
   - b. Jika payload dioptimalkan menggunakan teknik binary packing menjadi $28\text{ byte}$ per paket, hitung total volume konsumsi data bulanan armada tersebut.
   - c. Hitung persentase penghematan kuota data seluler yang diperoleh.
2. **Implementasi Validasi JSON Schema**:
   Menggunakan skrip [`data_models_validator.py`](content/chapter-21/src/data_models_validator.py), tambahkan satu aturan validasi baru ke dalam `TELEMETRY_SCHEMA`:
   - Tambahkan metrik `co2_ppm` dengan tipe integer, batas minimum $300\text{ ppm}$, dan batas maksimum $5000\text{ ppm}$.
   - Uji skrip Anda dengan payload yang memuat `co2_ppm = 250` dan pastikan pesan penolakan skema tertangkap secara tepat.
