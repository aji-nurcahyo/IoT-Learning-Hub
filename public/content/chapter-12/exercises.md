# Latihan Bertingkat — Chapter 12

## Bagian A — Pertanyaan Konseptual & Keamanan

1. Mengapa menanam SSID dan *password* Wi-Fi langsung di *source code* (`.ino`) merupakan praktik buruk untuk proyek IoT? Sebutkan dua risiko keamanan dan dua risiko operasionalnya.
2. Jelaskan perbedaan antara **`WIFI_STA`**, **`WIFI_AP`**, dan **`WIFI_AP_STA`**. Kapan mode `WIFI_AP_STA` digunakan?
3. Mengapa pada papan berbasis `ESP32-WROOM-32`, sensor analog seperti NTC atau potensiometer tidak boleh ditempatkan pada `GPIO 4` atau `GPIO 26` ketika Wi-Fi diaktifkan?

## Bagian B — Analisis State Machine & Perhitungan Backoff

4. **Analisis Kode Anti-Pattern**:
   Jelaskan apa yang terjadi pada LED status dan sensor suhu lokal apabila potongan kode berikut dijalankan ketika router Wi-Fi sedang mati selama 15 menit:
   ```cpp
   void setup() {
     WiFi.begin(ssid, pass);
     while (WiFi.status() != WL_CONNECTED) {
       delay(500);
     }
   }
   ```
5. **Perhitungan Exponential Backoff**:
   Sebuah node memakai `CONNECT_TIMEOUT_MS = 10 s`, `BACKOFF_MIN_MS = 2 s`, dan `BACKOFF_MAX_MS = 60 s`. Tuliskan urutan waktu tunggu *backoff* untuk 6 kali kegagalan koneksi beruntun, serta hitung total waktu (*timeout* + *backoff*) yang telah berlalu hingga percobaan ke-7 dimulai.

## Bagian C — Simulasi Software & Mini Challenge

6. **Verifikasi FSM (`wifi_fsm_sim.py`)**:
   ```sh
   python public/content/chapter-12/src/wifi_fsm_sim.py
   ```
   **Mini Challenge**:
   - Pada salinan lokal [`wifi_prov_fsm.ino`](content/chapter-12/src/wifi_prov_fsm/wifi_prov_fsm.ino) dan `wifi_fsm_sim.py`, tambahkan dukungan perintah Serial **`STATUS`** yang mencetak status FSM saat ini, SSID tersimpan (tanpa password!), IP lokal, `RSSI`, dan nilai `backoffMs` berjalan—serta tambahkan fitur **Static IP opsional** melalui `WiFi.config()` bila pengguna mengirim perintah `STATIC:<ip>,<gw>,<mask>`.

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **Bahaya Hardcoded Credentials**: Risiko keamanan: (a) kredensial terekspos saat kode di-push ke Git atau dibagikan; (b) semua perangkat memakai jejak kode yang sulit diaudit/rotasi. Risiko operasional: (a) perangkat tidak bisa dipindah ke jaringan lain tanpa *re-flash*; (b) kompilasi ulang diperlukan untuk setiap lokasi pemasangan.
2. **Mode Wi-Fi**: `WIFI_STA` = klien terhubung ke router; `WIFI_AP` = memancarkan hotspot sendiri; `WIFI_AP_STA` = keduanya aktif bersamaan (misal agar pengguna mengisi form provisioning lewat AP sementara ESP32 menguji koneksi STA ke router target).
3. **Konflik ADC2**: `GPIO 4` dan `GPIO 26` terhubung ke `ADC2` yang digunakan bersama subsistem Wi-Fi pada ESP32 klasik sehingga pembacaan ADC2 gagal saat Wi-Fi aktif. Gunakan `ADC1` (`GPIO 32–39`).
4. **Blocking `while` di `setup()`**: Program terjebak selamanya di `setup()`, tidak pernah masuk ke `loop()`, sehingga pembacaan sensor, kontrol histeresis, maupun tombol lokal lumpuh total selama 15 menit!
5. **Perhitungan Backoff ($t_{\text{timeout}}=10\text{ s}, t_{\min}=2\text{ s}, t_{\max}=60\text{ s}$)**:
   - Urutan backoff: `2 s, 4 s, 8 s, 16 s, 32 s, 60 s` (total backoff = $122\text{ s}$).
   - Total timeout 6 kali usaha = $6 \times 10\text{ s} = 60\text{ s}$.
   - Total waktu berlalu hingga percobaan ke-7 dimulai = $60 + 122 = 182\text{ detik}$ ($3\text{ menit } 2\text{ detik}$).

</details>

