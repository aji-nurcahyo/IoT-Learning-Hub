# Latihan Bertingkat — Chapter 04

## Bagian A — Pertanyaan Konseptual

1. Mengapa sebuah *Microcontroller* seperti ESP32 dapat melakukan *boot* dalam hitungan milidetik dan mengonsumsi daya jauh lebih kecil dibandingkan *Single-Board Computer* seperti Raspberry Pi?
2. Jelaskan perbedaan fungsi antara **Flash Memory**, **SRAM**, dan **ROM Bootloader** pada ESP32. Data apa yang hilang jika catu daya diputus sejenak?
3. Kapan seorang insinyur sebaiknya memilih **ESP-IDF** dibandingkan **Arduino-ESP32 Framework**, dan apa hubungan teknis antara kedua *framework* tersebut?

## Bagian B — Applied Engineering & Troubleshooting

4. **Audit Pemilihan Pin Lintas Varian**:
   Anda memiliki skema pin berikut: `GPIO 6`, `GPIO 12`, `GPIO 25`, `GPIO 34`, `GPIO 1`.
   Evaluasi kelayakan masing-masing pin jika digunakan sebagai **OUTPUT pengendali LED** pada:
   - (a) `ESP32-DevKitC V4 (WROOM-32)`
   - (b) `ESP32-C3`
   - (c) `ESP32-S3`

5. **Diagnosis Masalah Bring-Up**:
   Berikan kemungkinan penyebab utama dan langkah pemeriksaan sistematis untuk tiga kasus berikut:
   - Kasus 1: Saat tombol upload ditekan di Arduino IDE, muncul pesan `A fatal error occurred: Failed to connect to ESP32: Timed out waiting for packet header`.
   - Kasus 2: Upload berhasil, tetapi Serial Monitor hanya mencetak simbol aneh `⸮⸮x⸮⸮` secara berulang.
   - Kasus 3: Program berjalan 2 detik lalu board restart terus-menerus dengan pesan `Brownout detector was triggered`.

## Bagian C — Eksplorasi Software & Simulasi

6. **Audit Varian via Python (`board_matrix.py`)**:
   Jalankan skrip audit pin:
   ```sh
   python public/content/chapter-04/src/board_matrix.py
   ```
   **Mini Challenge**: Tambahkan fungsi di salinan skrip Anda untuk mengaudit daftar 4 pin sekaligus (`[LED_PIN, BTN_PIN, ADC_PIN, UART_TX]`) dan pastikan tidak ada pin duplikat maupun bentrok dengan *Flash/Strapping/Input-Only* pada varian target yang dipilih.

7. **Simulasi Wokwi (Path A) / Board Fisik (Path B Opsional)**:
   Gunakan [`ch04_board_probe.ino`](content/chapter-04/src/ch04_board_probe/ch04_board_probe.ino) dan [`wokwi_diagram.json`](content/chapter-04/src/wokwi_diagram.json) pada Wokwi (atau papan `ESP32-DevKitC V4` fisik bila tersedia dengan resistor $220\,\Omega$). Catat output aktual Serial Monitor yang Anda amati.

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **MCU vs SBC**: MCU mengeksekusi *Firmware* langsung dari *Flash* internal tanpa memuat OS besar dari penyimpanan eksternal, memiliki *clock* dan periferal yang dapat ditidurkan (*deep sleep*), serta tidak menyuplai RAM DDR eksternal.
2. **Flash vs SRAM vs ROM**: *Flash* menyimpan program dan data persisten (tidak hilang saat mati); *SRAM* menyimpan variabel, *stack*, dan *heap* saat runtime (**hilang** saat reset/daya mati); *ROM* berisi bootloader permanen pabrik.
3. **Arduino vs ESP-IDF**: *Arduino-ESP32* berjalan di atas *ESP-IDF* + FreeRTOS dan dipilih untuk kemudahan prototipe; *ESP-IDF* dipilih saat butuh kendali penuh atas *task FreeRTOS*, optimasi memori/daya, atau fitur keamanan/partisi tingkat lanjut.
4. **Audit Pin OUTPUT LED**:
   - `GPIO 6`: **Dilarang** pada `ESP32-WROOM-32` (*SPI Flash*), aman pada `ESP32-C3` dan `ESP32-S3`.
   - `GPIO 12`: *Strapping pin* (hati-hati) pada `ESP32-WROOM-32`, **dilarang** (*SPI Flash*) pada `ESP32-C3`, aman pada `ESP32-S3`.
   - `GPIO 25`: Aman pada `ESP32-WROOM-32`; pada `ESP32-C3` (hanya GPIO 0–21) nomor pin 25 tidak tersedia!
   - `GPIO 34`: **Ditolak** (*input-only*) pada `ESP32-WROOM-32`; pada `ESP32-S3` aman sebagai output; pada `ESP32-C3` tidak ada GPIO 34.
   - `GPIO 1`: Jalur `TX0` Serial pada `ESP32-WROOM-32` (tidak disarankan jika memakai Serial Monitor).
5. **Diagnosis**: (1) Gagal masuk *Download Mode* / port dipakai / kabel *charge-only*; (2) *Baud rate* Serial Monitor tidak cocok dengan `Serial.begin(115200)`; (3) Tegangan suplai jatuh (*sag*) akibat arus berlebih atau kabel USB tipis.

</details>

