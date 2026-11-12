# Exercises — Chapter 18: LoRa & LoRaWAN Fundamentals

## A. Pertanyaan Konseptual

1. Jelaskan secara ringkas perbedaan peran **LoRa (PHY)** dan **LoRaWAN (MAC/Network)**! Mengapa dua ESP32 yang menjalankan contoh *LoRa P2P* bawaan Arduino tidak otomatis bisa terhubung ke server *The Things Stack* atau *ChirpStack*?
2. Mengapa arsitektur LoRaWAN menggunakan topologi **Star-of-Stars** (bukan *multi-hop mesh*) untuk sensor lapangan bertenaga baterai?
3. Pada perangkat **Class A**, kapan node dapat menerima pesan perintah (*downlink*) dari *Network Server*? Apa implikasinya jika Anda ingin mematikan katup irigasi dalam waktu maksimal `2 detik` setelah tombol operator ditekan?

## B. Analisis Time-on-Air & Link Budget (`lora_airtime_budget.py`)

4. Berdasarkan tabel hasil [`lora_airtime_budget.py`](content/chapter-18/outputs.md) untuk `24 byte` payload (`BW = 125 kHz`, `CR = 4/5`):
   - a) Hitung perbandingan rasio *Time-on-Air* antara `SF12` (`1482.75 ms`) dengan `SF7` (`61.70 ms`)!
   - b) Mengapa flag **DE** (*Low Data Rate Optimization*) berubah dari `0` menjadi `1` mulai `SF11` ($T_{\text{sym}} = 16.384\text{ ms}$)?
5. Modifikasi skrip [`lora_airtime_budget.py`](content/chapter-18/src/lora_airtime_budget.py) untuk menguji ukuran payload **51 byte** (mengilustrasikan JSON teks yang boros) dibanding **12 byte** (biner ringkas) pada `SF10, BW 125 kHz`. Catat selisih persentase penghematan *Time-on-Air*-nya!
6. Sebuah tautan radio memiliki $P_{\text{tx}} = 14\text{ dBm}$, $G_{\text{tx}} = 2\text{ dBi}$, $G_{\text{rx}} = 5\text{ dBi}$, rugi kabel total $2\text{ dB}$, rugi propagasi lintasan ($L_{\text{path}}$) sebesar $126\text{ dB}$, dan *fading margin* $10\text{ dB}$. Hitung $P_{\text{rx}}$ yang diterima *gateway*, lalu tentukan *Spreading Factor* terkecil (`SF7`–`SF12`) yang masih menghasilkan *margin* positif minimal $+6\text{ dB}$ memakai sensitivitas referensi SX1276 (`-123` s.d. `-137 dBm`)!

## C. Analisis Kepatuhan Regional & Keamanan

7. Jelaskan mengapa langkah pertama sebelum memprogram frekuensi kanal pada proyek LoRaWAN harus berupa pengecekan **LoRa Alliance Regional Parameters (RP2)** dan regulasi otoritas spektrum nasional, bukan menyalin kode `915E6` atau `868E6` dari tutorial daring secara mentah!
8. Jelaskan perbedaan kunci keamanan **OTAA** (`DevEUI`, `JoinEUI`, `AppKey` -> `NwkSKey`, `AppSKey`) dibanding **ABP**, khususnya ketika node mengalami pemadaman baterai dan restart dari nol.

## Expected Output Acuan

Menjalankan skrip default [`lora_airtime_budget.py`](content/chapter-18/src/lora_airtime_budget.py) harus menghasilkan nilai referensi pada [`outputs.md`](content/chapter-18/outputs.md):

- `SF7`: `T_sym=1.024 ms`, `DE=0`, `ToA=61.70 ms`
- `SF10`: `T_sym=8.192 ms`, `DE=0`, `ToA=370.69 ms`
- `SF12`: `T_sym=32.768 ms`, `DE=1`, `ToA=1482.75 ms`
- Link budget `3.0 km`: `FSPL = 101.29 dB`, `P_rx_est = -98.79 dBm`.

