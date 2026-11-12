# Latihan Bertingkat — Chapter 06

## Bagian A — Pertanyaan Konseptual

1. Jelaskan perbedaan antara **level detection** dan **edge detection** saat membaca tombol pada `loop()`. Mengapa *edge detection* (`HIGH -> LOW` pada *active-low*) lebih cocok untuk mengganti mode LED?
2. Mengapa `pinMode(35, INPUT_PULLUP)` pada `ESP32-WROOM-32` tidak bekerja seperti yang diharapkan pemula? Bagaimana cara memperbaikinya jika Anda terpaksa memakai `GPIO 35`?
3. Sebutkan **tiga** hal yang dilarang dilakukan di dalam fungsi ISR (`attachInterrupt`) pada ESP32 dan jelaskan alasannya.

## Bagian B — Analisis Kode & Perbandingan Metode

4. **Menemukan Bug pada Kode Interrupt**:
   Temukan **minimal 3 kesalahan** pada potongan kode berikut:
   ```cpp
   bool pressed = false;
   void onPress() {
     Serial.println("Tombol ditekan!");
     delay(50);
     pressed = true;
   }
   ```
5. **Pemilihan Polling vs Interrupt**:
   Tentukan metode mana (*Non-Blocking Polling* atau *External Interrupt*) yang lebih tepat untuk kasus berikut beserta alasannya:
   - (a) Tombol menu antarmuka manusia yang ditekan paling cepat 3 kali per detik.
   - (b) Sensor *optical encoder* motor berputar 3.000 RPM yang menghasilkan 1.000 pulsa per detik.

## Bagian C — Simulasi Software & Mini Challenge

6. **Eksperimen Jendela Debounce (`debounce_sim.py`)**:
   Jalankan:
   ```sh
   python public/content/chapter-06/src/debounce_sim.py
   ```
   - Amati hasil perbandingan *naive* (6 pemicu palsu) vs *software debounce* 50 ms (2 pemicu valid).
   - **Uji sensitivitas**: Pada salinan lokal skrip, ubah `DEBOUNCE_MS = 10` dan `DEBOUNCE_MS = 150`. Catat nilai mana yang mulai gagal menyaring bounce pada `telemetry.csv` dan mengapa nilai terlalu besar juga berbahaya!
7. **Mini Challenge Firmware (Wokwi Path A / Hardware Path B Opsional)**:
   Modifikasi [`ex01_button_debounce_fsm.ino`](content/chapter-06/src/ex01_button_debounce_fsm/ex01_button_debounce_fsm.ino) untuk mendukung **Long Press** ($\ge 1500\text{ ms}$):
   - *Short Press* ($< 1500\text{ ms}$): Beralih mode `OFF -> ON -> BLINK -> OFF`.
   - *Long Press* ($\ge 1500\text{ ms}$): Langsung memaksa mode ke `OFF` dan mencetak `[LONG PRESS] Forced OFF`.

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **Level vs Edge**: *Level detection* bernilai benar berulang kali selama tombol ditahan, sedangkan *edge detection* hanya terpicu sekali pada momen transisi dari dilepas ke ditekan.
2. **GPIO 35 ESP32**: `GPIO 34–39` pada `ESP32-WROOM-32` adalah pin *input-only* tanpa sirkuit *internal pull-up / pull-down*. Jika tetap memakai GPIO 35, wajib pasang resistor *pull-up* eksternal (misal $10\text{ k}\Omega$ ke `3V3`).
3. **Larangan ISR**: (1) Tidak boleh `Serial.print()` (lambat & bisa deadlock/panic); (2) Tidak boleh `delay()` (menghentikan sistem & memicu watchdog); (3) Jangan lupa `IRAM_ATTR` agar kode ISR berada di RAM dan tidak crash saat Flash sibuk; serta variabel bersama wajib bertipe `volatile`.
4. **Bug Kode Interrupt**: (1) `pressed` tidak bertipe `volatile`; (2) `onPress()` tidak memakai `IRAM_ATTR`; (3) memanggil `Serial.println()` dan `delay(50)` di dalam ISR.
5. **Polling vs Interrupt**: (a) *Polling* non-blocking lebih sederhana dan mudah di-debounce; (b) *Interrupt* wajib dipakai untuk 1.000 pulsa/detik agar tidak ada tepi sinyal sempit yang terlewat di antara iterasi `loop()`.

</details>

