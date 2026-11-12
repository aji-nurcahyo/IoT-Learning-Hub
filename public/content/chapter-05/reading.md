# Chapter 05 — Embedded Programming with C/C++

## Overview

Menulis *Firmware* untuk *Microcontroller* berbeda dengan menulis skrip Python atau aplikasi desktop yang memiliki RAM bergiga-bita dan sistem operasi penuh. Pada *Embedded System*, program berjalan langsung di atas perangkat keras (*bare-metal* atau RTOS ringan), berbagi waktu CPU antara membaca sensor, merespons tombol, menjaga komunikasi serial, dan mengendalikan *Actuator* secara berkesinambungan.

Chapter ini membangun keterampilan pemrograman C/C++ tertanam secara bertahap: mulai dari alur kerja *embedded*, tipe data berlebar tetap (*fixed-width integers*), modularisasi menggunakan *header file*, struktur `setup()` dan `loop()`, teknik *Serial debugging*, eksekusi **non-blocking** dengan `millis()`, kesadaran memori (*Flash* vs *SRAM*, *stack* vs *heap*), hingga merancang **Finite State Machine (FSM)** dasar yang bersih dan mudah dirawat.

## Prasyarat

- Memahami arsitektur MCU (`Flash`, `SRAM`, `GPIO`, `UART`) serta pembatasan pin pada `ESP32-DevKitC V4` dari [Chapter 04](#/chapter/4).
- Mengenal dasar alur kontrol pemrograman (variabel, kondisi, perulangan, fungsi).

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Menggunakan** tipe data C/C++ berlebar tetap (`uint8_t`, `uint16_t`, `uint32_t`), fungsi, *struct*, dan *header file* (`.h`) untuk menyusun kode *Firmware* yang modular.
2. **Menerapkan** *timing* berbasis `millis()` yang aman terhadap *rollover* 32-bit untuk menggantikan *blocking* `delay()`.
3. **Menganalisis** penggunaan memori *Flash* vs *SRAM* (*stack* vs *heap*) serta mencegah fragmentasi memori akibat objek dinamis seperti `String`.
4. **Merancang** *Finite State Machine* (FSM) sederhana yang terbaca rapi, teruji logikanya, dan siap menerima input paralel.

## Konsep dan teori

### 1. Embedded Programming Workflow & Arduino `setup()` / `loop()`

Pada ekosistem *Arduino-ESP32*, setiap *Firmware* memiliki dua titik masuk utama yang dipanggil oleh kerangka kerja di atas FreeRTOS:
- `void setup()`: Dijalankan **satu kali** saat MCU menyala atau di-reset. Digunakan untuk inisialisasi komunikasi `Serial.begin()`, konfigurasi `pinMode()`, dan menetapkan status awal *Actuator* ke kondisi aman (*fail-safe*).
- `void loop()`: Dijalankan **berulang terus-menerus** tanpa henti (*super-loop*). Kecepatan eksekusi `loop()` menentukan seberapa cepat sistem merespons kejadian baru; karena itu, **satu tugas tidak boleh memblokir CPU terlalu lama**.

### 2. C/C++ Fundamentals untuk Embedded

**A. Fixed-Width Data Types (`<cstdint>`)**
Di pemrograman desktop, ukuran `int` bisa berbeda antar arsitektur (16-bit di AVR Arduino Uno vs 32-bit di ESP32). Gunakan tipe data berlebar pasti agar ukuran memori dan batas nilainya eksplisit:

| Tipe Data | Ukuran | Rentang Nilai | Contoh Penggunaan IoT |
| --- | --- | --- | --- |
| `uint8_t` | 1 byte | $0 \dots 255$ | Nomor pin GPIO, nilai PWM 8-bit, *enum state* |
| `uint16_t` | 2 byte | $0 \dots 65.535$ | Nilai mentah ADC 12-bit ($0\dots 4095$), *port* TCP |
| `int16_t` | 2 byte | $-32.768 \dots 32.767$ | Suhu dikalikan 100 (`2545` = $25{,}45\,^\circ\text{C}$) |
| `uint32_t` | 4 byte | $0 \dots 4.294.967.295$ | Nilai waktu `millis()` dan `micros()` |
| `bool` | 1 byte | `true` / `false` | Status tombol, *flag* alarm |
| `float` | 4 byte | IEEE-754 *single* | Perhitungan fisik (suhu, tegangan, kalibrasi) |

**B. Operator, Kondisional, Perulangan, dan Fungsi**
Gunakan `constexpr` atau `const` untuk konstanta pin dan ambang batas (bukan `#define` tanpa tipe), pecah logika menjadi fungsi kecil dengan satu tanggung jawab, dan hindari *magic numbers* di tengah kode.

**C. Modularisasi dengan Header File (`.h`)**
Memasukkan seluruh *struct*, helper timer, dan logika aplikasi ke satu file `.ino` ratusan baris membuat kode sulit dibaca dan diuji ulang. Gunakan *include guard* (`#ifndef ... #define ... #endif`) pada file `.h` seperti [`led_timer.h`](content/chapter-05/src/ex02_nonblocking_fsm/led_timer.h) untuk memisahkan utilitas timer LED dari alur utama [`ex02_nonblocking_fsm.ino`](content/chapter-05/src/ex02_nonblocking_fsm/ex02_nonblocking_fsm.ino).

### 3. Serial Debugging yang Efektif

`Serial` adalah "kaca mata" utama insinyur *embedded*. Namun, mencetak teks terlalu cepat di dalam `loop()` tanpa jeda waktu akan membanjiri *UART TX buffer* dan melambatkan sistem.
- Inisialisasi sekali di `setup()`: `Serial.begin(115200);`
- Format pesan terstruktur dengan `snprintf()` ke *char array* berkapasitas tetap agar keluaran mudah diparse dan tidak membocorkan memori *heap*.

### 4. Blocking `delay()` vs Non-Blocking `millis()`

Fungsi `delay(1000)` menghentikan eksekusi tugas di `loop()` selama 1 detik penuh—tombol ditekan tidak terbaca, pesan masuk terlewat, dan LED lain berhenti berkedip. Solusinya adalah pola **non-blocking polling** dengan `millis()` (jumlah milidetik sejak MCU menyala):

![Perbandingan blocking delay versus non-blocking millis dan FSM dasar](content/chapter-05/diagram.svg)

Pola pengurangan *unsigned* 32-bit yang benar:

```cpp
if ((uint32_t)(nowMs - prevMs) >= intervalMs) {
  prevMs = nowMs;
  // jalankan aksi periodik
}
```

**Mengapa harus pengurangan `(nowMs - prevMs)`, bukan `nowMs >= nextTargetMs`?**
Setelah menyala $\frac{2^{32}-1}{1000 \times 86400} \approx 49{,}71\text{ hari}$, penghitung `millis()` kembali ke `0` (*rollover*). Jika Anda menulis `if (millis() >= nextTime)`, saat `nextTime` melewati batas $2^{32}$, perbandingan bisa macet atau langsung memicu palsu. Dengan **aritmatika modular *unsigned* 32-bit**, misalnya `prevMs = 0xFFFFFFF0` ($16\text{ ms}$ sebelum overflow) dan `nowMs = 0x000003D8` ($984\text{ ms}$ sesudah overflow), hasil `(uint32_t)(nowMs - prevMs)` tetap tepat **`1000 ms`**! Sifat ini telah diverifikasi melalui skrip [`fsm_timing_sim.py`](content/chapter-05/src/fsm_timing_sim.py).

### 5. Memory Awareness: Flash vs SRAM, Stack vs Heap

| Wilayah Memori | Sifat | Apa yang Disimpan? | Risiko Kegagalan |
| --- | --- | --- | --- |
| **Flash (RODATA/Code)** | Non-volatil | Kode mesin, `const char*`, tabel kalibrasi konstan | Habis jika terlalu banyak aset/library besar |
| **SRAM Statis / Global** | Volatil | Variabel global, array tetap (`char buf[96]`) | Terlalu besar saat kompilasi $\rightarrow$ gagal link |
| **SRAM Stack** | Volatil (LIFO) | Variabel lokal fungsi & alamat kembali | Rekursi dalam / array lokal raksasa $\rightarrow$ *Stack overflow* |
| **SRAM Heap** | Volatil (dinamis) | Objek `new`, `malloc`, konkatenasi `String` Arduino | **Heap fragmentation** setelah berjalan berhari-hari $\rightarrow$ *crash* |

**Praktik Terbaik**: Hindari menggabungkan `String s = "temp=" + String(t) + " C";` berulang-ulang di dalam `loop()`. Gunakan buffer lokal tetap `char buf[96]` + `snprintf(...)` seperti pada [`ex01_types_serial.ino`](content/chapter-05/src/ex01_types_serial/ex01_types_serial.ino).

### 6. Finite State Machine (FSM) Dasar

Saat logika bertambah kompleks (misalnya *menunggu jadwal $\rightarrow$ membaca sampel $\rightarrow$ mode alarm berkedip cepat*), kumpulan `if-else` bertumpuk dengan banyak variabel boolean (`isAlert`, `wasSampled`, `flag1`) cepat berubah menjadi *spaghetti code*. **FSM** menyederhanakannya menjadi sekumpulan **state** eksklusif (`enum class SystemState { IDLE, SAMPLE, ALERT };`) dan **transisi eksplisit** di dalam `switch (currentState)`.

### 7. Implementasi Praktis Bertahap (Path A & Path B)

- **Tahap 1 — Dasar Tipe Data & Serial**: [`ex01_types_serial.ino`](content/chapter-05/src/ex01_types_serial/ex01_types_serial.ino)
- **Tahap 2 — Header Modular & Non-Blocking FSM**: [`led_timer.h`](content/chapter-05/src/ex02_nonblocking_fsm/led_timer.h) + [`ex02_nonblocking_fsm.ino`](content/chapter-05/src/ex02_nonblocking_fsm/ex02_nonblocking_fsm.ino)
- **Simulasi Wokwi (Path A)**: [`wokwi_diagram.json`](content/chapter-05/src/wokwi_diagram.json) (`ESP32-DevKitC V4`, LED Hijau `GPIO 25`, LED Merah `GPIO 26`, masing-masing seri resistor $220\,\Omega$).
- **Verifikasi Software Logika**: [`fsm_timing_sim.py`](content/chapter-05/src/fsm_timing_sim.py) dieksekusi nyata di Python 3.12.10 (lihat [`outputs.md`](content/chapter-05/outputs.md)). Firmware `.ino` berstatus **Belum diuji** pada *compiler*/Wokwi/hardware di server ini.

### 8. Common Mistakes & Troubleshooting

| Kesalahan Kode | Akibat di Runtime | Solusi |
| --- | --- | --- |
| Memakai `delay(5000)` di `loop()` | Sistem tampak "hang", tombol atau sensor tidak responsif | Pecah ke pola `millis()` non-blocking |
| `if (millis() >= nextMs)` | Bug saat sistem menyala $> 49{,}7$ hari (*rollover*) | Selalu gunakan `(uint32_t)(now - prev) >= interval` |
| `String msg = ... + ...` di `loop()` | Kehabisan memori *heap* terfragmentasi setelah berjam-jam | Ganti dengan `char buf[N]` + `snprintf()` |
| Lupa `break;` pada `switch-case` FSM | *Fall-through* tidak sengaja ke state berikutnya | Selalu tutup setiap `case` dengan `break;` |

### 9. Real-World Applications

- **Node Sensor Pertanian / Telekomunikasi**: Menjalankan *heartbeat* LED tiap 1 s, pembacaan sensor tiap 5 s, dan pengiriman status tiap 60 s secara bersamaan tanpa *RTOS task* yang rumit.
- **Perangkat Industri 24/7**: Penggunaan pengurangan *unsigned* `millis()` dan *fixed buffer* menjaga *Firmware* berjalan berbulan-bulan tanpa *memory leak* atau *rollover hang*.

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-05/exercises.md)):
1. Analisis perbedaan *stack*, *heap*, dan *Flash* pada potongan kode C++.
2. Refaktor kode *blocking* (`delay()`) menjadi pola `millis()` dengan dua timer paralel (kedip LED 350 ms dan logging serial 1000 ms).
3. Verifikasi kasus *rollover* 32-bit menggunakan [`fsm_timing_sim.py`](content/chapter-05/src/fsm_timing_sim.py).
4. Mini Challenge: Memperluas FSM pada `ex02_nonblocking_fsm.ino` dengan menambahkan state `COOLDOWN` berdurasi 3 detik setelah kondisi `ALERT`.

## Tugas

Bangun **Firmware Non-Blocking 3-Task + Finite State Machine Modular** (detail & *acceptance criteria* di tab **Tugas & Rubrik** — [assignment.md](content/chapter-05/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Struktur C/C++, tipe data & modularitas header | 25 | Penggunaan `uint*_t`, `constexpr`, pemisahan `.h` dengan include guard, tanpa *heap String* |
| Implementasi non-blocking millis() | 30 | Bebas `delay()` di `loop()`, aman terhadap *rollover* 32-bit, multi-interval independen |
| Desain Finite State Machine (FSM) | 25 | State & transisi jelas via `enum class` + `switch`, termasuk kondisi awal aman |
| Dokumentasi, uji logika & keterbatasan | 20 | Output Serial yang diharapkan/aktual terdokumentasi jujur serta bebas kesalahan kompilasi logis |

## Ringkasan

- Kode *embedded* yang baik memanfaatkan tipe data berlebar tetap (`uint8_t`, `uint16_t`, `uint32_t`), header modular, dan buffer statis `snprintf()` alih-alih alokasi *heap* `String` berulang.
- Mengganti `delay()` dengan `(uint32_t)(millis() - prevMs) >= intervalMs` menjaga responsivitas sistem sekaligus aman terhadap *rollover* 49,7 hari.
- FSM dengan `enum class` dan `switch` membuat alur kerja *Firmware* mudah diperluas dan diaudit.
- Verifikasi aritmatika *rollover* dan transisi FSM telah dijalankan via Python `fsm_timing_sim.py`; kompilasi `.ino` dan uji pada Wokwi/ESP32 fisik belum dijalankan di lingkungan ini.

## Referensi

1. Arduino Official Documentation, *Blink Without Delay & millis() Reference*, [https://docs.arduino.cc/built-in-examples/digital/BlinkWithoutDelay/](https://docs.arduino.cc/built-in-examples/digital/BlinkWithoutDelay/) (diperiksa 2026-11-10).
2. Espressif Systems, *Arduino-ESP32 API Reference & Memory Guidelines*, [https://docs.espressif.com/projects/arduino-esp32/en/latest/](https://docs.espressif.com/projects/arduino-esp32/en/latest/) (diperiksa 2026-11-10).
3. cppreference.com, *Fixed Width Integer Types (`<cstdint>`)*, [https://en.cppreference.com/w/cpp/types/integer](https://en.cppreference.com/w/cpp/types/integer) (diperiksa 2026-11-10).

