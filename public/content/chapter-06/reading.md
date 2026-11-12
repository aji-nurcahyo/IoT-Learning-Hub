# Chapter 06 — GPIO, Digital Input/Output & Debouncing

## Overview

Antarmuka paling dasar antara *Microcontroller* dan dunia fisik adalah **General Purpose Input/Output (GPIO)**. Meskipun tampak sederhana (`HIGH` atau `LOW`), membaca saklar mekanis atau mengendalikan indikator secara andal membutuhkan pemahaman tentang logika digital, konfigurasi resistor *pull-up / pull-down*, fenomena fisik ***switch bounce***, deteksi tepi sinyal (*edge detection*), perbedaan *polling* vs *interrupt*, serta penggabungan ke dalam *Finite State Machine* (FSM) non-blocking.

Chapter ini membawa mahasiswa merancang praktik **button-controlled LED dengan software debouncing yang benar**, lengkap dengan alternatif *interrupt* dan verifikasi simulasi.

## Prasyarat

- Memahami *pull-up / pull-down resistor* serta pembatas arus LED dari [Chapter 03](#/chapter/3).
- Memahami klasifikasi pin `ESP32-DevKitC V4` (terutama sifat *input-only* `GPIO 34–39` tanpa *internal pull-up*) dari [Chapter 04](#/chapter/4).
- Menguasai pola `millis()` non-blocking dan `enum class` FSM dari [Chapter 05](#/chapter/5).

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Mengonfigurasi** pin GPIO sebagai `OUTPUT`, `INPUT`, `INPUT_PULLUP`, dan `INPUT_PULLDOWN` sesuai level logika (*active-high* vs *active-low*) dan batasan varian ESP32.
2. **Menjelaskan** penyebab fisik *switch bounce* dan membandingkan *software debouncing* berbasis waktu dengan *hardware RC debouncing*.
3. **Mengimplementasikan** *falling-edge / rising-edge detection* non-blocking dan *Finite State Machine* (FSM) untuk mengendalikan LED melalui tombol.
4. **Membandingkan** metode *polling* di `loop()` dengan *external interrupt* (`attachInterrupt`, `IRAM_ATTR`, `volatile`) beserta aturan keselamatan ISR.

## Konsep dan teori

### 1. Digital Logic: `HIGH`, `LOW`, dan Konfigurasi Pin

Pada sistem logika $3{,}3\text{ V}$ ESP32:
- **`HIGH` (`1`)**: Tegangan mendekati $3{,}3\text{ V}$ (umumnya $V_{IH} \ge 0{,}75 \cdot V_{DD} \approx 2{,}48\text{ V}$).
- **`LOW` (`0`)**: Tegangan mendekati $0\text{ V}$ (umumnya $V_{IL} \le 0{,}25 \cdot V_{DD} \approx 0{,}83\text{ V}$).

Konfigurasi `pinMode(pin, mode)` pada *Arduino-ESP32*:
- `OUTPUT`: Pin mengendalikan tegangan ke `HIGH` ($3{,}3\text{ V}$) atau `LOW` ($0\text{ V}$) melalui `digitalWrite()`.
- `INPUT`: Impedansi tinggi tanpa resistor internal—**wajib** memiliki resistor *pull-up* atau *pull-down* eksternal jika terhubung ke saklar.
- `INPUT_PULLUP`: Mengaktifkan resistor *pull-up* internal ($\approx 45\text{ k}\Omega$ pada ESP32) ke $3{,}3\text{ V}$. Paling umum dipakai untuk tombol karena cukup menyambungkan tombol antara pin GPIO dan `GND` (*active-low*: dilepas = `HIGH`, ditekan = `LOW`).
- `INPUT_PULLDOWN`: Mengaktifkan resistor *pull-down* internal ke `GND` (*active-high*).
- **Peringatan ESP32-WROOM-32**: `GPIO 34, 35, 36, 39` **tidak memiliki** resistor *internal pull-up / pull-down*! Memanggil `pinMode(34, INPUT_PULLUP)` tidak akan menarik pin ke $3{,}3\text{ V}$—pin akan tetap *floating* kecuali Anda memasang resistor $10\text{ k}\Omega$ eksternal.

### 2. Switch Bounce & Mengapa Pembacaan Mentah Gagal

Saat dua kontak logam di dalam *push button* mekanis menutup atau membuka, sifat elastis logam menyebabkan kontak **memantul (*bounce*)** berkali-kali selama $5\text{--}30\text{ ms}$ sebelum menetap stabil. Pada *Microcontroller* yang menjalankan `loop()` ribuan kali per detik, **satu kali tekanan jari terbaca sebagai 4 hingga 10 kali penekanan beruntun!**

![Fenomena switch bounce, jendela waktu debounce 50 ms, dan wiring INPUT_PULLUP](content/chapter-06/diagram.svg)

### 3. Software Debouncing vs Hardware Debouncing

| Pendekatan | Mekanisme | Kelebihan | Keterbatasan |
| --- | --- | --- | --- |
| **Software Debouncing** | Mencatat waktu perubahan terakhir (`lastBounceMs`); menerima status baru hanya jika sinyal bertahan konstan $\ge T_{db}$ ($20\text{--}50\text{ ms}$) | Nol komponen tambahan, mudah diubah via parameter kode | Memerlukan polling cepat atau mekanisme lockout pada interrupt |
| **Hardware RC Debouncing** | Resistor + Kapasitor (*low-pass filter*) + *Schmitt trigger* sebelum masuk pin | Sinyal sudah bersih sebelum menyentuh MCU; sangat cocok untuk interrupt murni | Menambah biaya BOM dan ukuran PCB |

**Jangan Pernah Men-debounce dengan `delay(50)` di Tengah `loop()`!** Pemblokiran menghentikan tugas lain dan tetap salah bila *bounce* terjadi di tepi pelepasan tombol.

### 4. Edge Detection vs Level Detection

- **Level Detection (`if (state == LOW)`)**: Selama jari menahan tombol selama 1 detik, kondisi terus bernilai benar $\rightarrow$ mode LED berputar ratusan kali per detik!
- **Edge Detection**: Mendeteksi **momen transisi** saja—misalnya *falling edge* (`HIGH -> LOW` pada tombol *active-low*) atau *rising edge* (`LOW -> HIGH`). Aksi hanya dieksekusi **tepat 1 kali per penekanan**.

### 5. Polling vs External Interrupt (`attachInterrupt`)

- **Non-Blocking Polling**: Membaca `digitalRead()` di setiap iterasi `loop()`. Sederhana, mudah di-debounce dengan timer `millis()`, dan sangat memadai untuk tombol manusia selama `loop()` bebas `delay()`.
- **External Interrupt (`attachInterrupt`)**: Perangkat keras langsung menghentikan sementara program utama dan memanggil fungsi *Interrupt Service Routine* (ISR) ketika tepi sinyal terjadi. Berguna untuk sinyal sangat cepat (*rotary encoder*, pulsa sensor aliran) atau membangunkan MCU dari *sleep*.

**Aturan Wajib ISR pada ESP32 (`ex02_interrupt_flag.ino`)**:
1. Beri atribut **`IRAM_ATTR`** pada fungsi ISR agar tetap berada di SRAM instruksi (*IRAM*), bukan di Flash (mencegah crash saat operasi akses Flash/Wi-Fi).
2. Buat ISR **sesingkat mungkin**: hanya setel *flag* `volatile bool` dan catat timestamp `millis()`.
3. **DILARANG** memanggil `Serial.print()`, `delay()`, atau alokasi memori di dalam ISR! Proses pencetakan dan *debounce* dilakukan di `loop()`.

### 6. Implementasi Praktis: Button-Controlled LED FSM

**Spesifikasi Target (`ESP32-DevKitC V4`)**:
- **BOM**: 1x `ESP32-DevKitC V4`, 1x *Push Button*, 1x LED Hijau, 1x Resistor $220\,\Omega$, *breadboard* & *jumper*.
- **Pin Mapping**:
  - `GPIO 27` (`INPUT_PULLUP`) $\leftrightarrow$ *Push Button* $\leftrightarrow$ `GND`
  - `GPIO 25` (`OUTPUT`) $\rightarrow$ Resistor $220\,\Omega$ $\rightarrow$ Anoda LED $\rightarrow$ Katoda LED $\rightarrow$ `GND`
- **Logika FSM 3-Mode**: Setiap *falling edge* yang ter-debounce menggeser mode secara siklik: `OFF -> ON -> BLINK (250 ms) -> OFF`.

**Kode & Simulasi**:
- Firmware lengkap *polling debounce + FSM*: [`ex01_button_debounce_fsm.ino`](content/chapter-06/src/ex01_button_debounce_fsm/ex01_button_debounce_fsm.ino)
- Firmware *interrupt flag + debounce*: [`ex02_interrupt_flag.ino`](content/chapter-06/src/ex02_interrupt_flag/ex02_interrupt_flag.ino)
- Skema Wokwi (Path A, dilengkapi simulasi *bounce*): [`wokwi_diagram.json`](content/chapter-06/src/wokwi_diagram.json)
- Verifikasi *software* pada dataset pantulan sintetis ([`telemetry.csv`](content/chapter-06/telemetry.csv)) melalui [`debounce_sim.py`](content/chapter-06/src/debounce_sim.py): tanpa *debounce*, 2 penekanan fisik memicu **6 event palsu**; dengan *software debounce* $50\text{ ms}$, tepat **2 event valid** terdeteksi (`outputs.md`). Firmware `.ino` berstatus **Belum diuji** di server ini.

### 7. Common Mistakes & Troubleshooting

| Masalah Umum | Penyebab | Solusi |
| --- | --- | --- |
| Sekali tekan tombol, mode LED melompat acak | Tidak ada *debouncing* atau memakai *level detection* alih-alih *edge detection* | Terapkan jendela stabilitas $50\text{ ms}$ dan deteksi transisi `HIGH -> LOW` saja |
| `INPUT_PULLUP` pada `GPIO 34/35/36/39` selalu terbaca acak | Pin input-only ESP32 klasik tidak punya resistor *pull-up* internal | Pindahkan ke `GPIO 27` (atau tambah resistor $10\text{ k}\Omega$ eksternal ke `3V3`) |
| Board *Guru Meditation Error / Panic* saat interrupt | Memanggil `Serial.println()` di dalam ISR atau lupa `IRAM_ATTR` | Gunakan `IRAM_ATTR` + `volatile bool` flag; cetak di `loop()` |
| Tombol ditekan terbalik (`HIGH` saat ditekan) | Salah wiring: tombol ke `3V3` padahal mode `INPUT_PULLUP` | Hubungkan tombol `INPUT_PULLUP` ke `GND`, atau gunakan `INPUT_PULLDOWN` ke `3V3` |

### 8. Real-World Applications

- **Tombol Darurat & Saklar Pintu Kabinet BTS**: Deteksi pembukaan pintu shelter atau tombol *maintenance override* memakai *debouncing* agar alarm tidak mengirim puluhan notifikasi palsu dalam satu detik.
- **Sensor Pulsa Tipping Bucket Rain Gauge / Flow Meter**: Saklar *reed switch* magnetik di stasiun cuaca mengalami *bounce* mekanik yang harus difilter agar hitungan curah hujan atau debit air tidak berlipat ganda.

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-06/exercises.md)):
1. Perbandingan *level* vs *edge detection*, *active-high* vs *active-low*, serta kendala `GPIO 34–39`.
2. Diagnosis kesalahan *wiring* dan pelanggaran aturan ISR (`IRAM_ATTR`, `Serial` di ISR).
3. Simulasi *software* dengan [`debounce_sim.py`](content/chapter-06/src/debounce_sim.py) untuk menganalisis pengaruh variasi `DEBOUNCE_MS` ($10\text{ ms}$ vs $50\text{ ms}$ vs $200\text{ ms}$).
4. Mini Challenge: Menambahkan fitur **Long Press ($\ge 1500\text{ ms}$)** pada tombol untuk langsung mematikan LED (`OFF`) dari mode mana pun.

## Tugas

Implementasikan **Sistem Antarmuka Tombol Dual-Action (Short Press + Long Press) dengan Debounce & FSM** (spesifikasi & rubrik di tab **Tugas & Rubrik** — [assignment.md](content/chapter-06/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Konfigurasi GPIO & keamanan rangkaian | 20 | Pin valid (bukan 6–11 / input-only tanpa pull-up eksternal), resistor LED $220\,\Omega$ |
| Implementasi debouncing & edge detection | 30 | Non-blocking `millis()`, bebas pemicuan ganda pantulan maupun penahanan tombol |
| Desain FSM & logika short/long press | 30 | Transisi state bersih (`OFF`, `ON`, `BLINK`, `LOCKED/RESET`), responsif tanpa `delay()` |
| Dokumentasi, simulasi & kejujuran bukti | 20 | Wiring table lengkap, log uji simulasi/expected output terdokumentasi jujur |

## Ringkasan

- Gunakan `INPUT_PULLUP` (*active-low* ke `GND`) pada pin GPIO yang mendukung pull-up internal (hindari `GPIO 34–39` tanpa resistor eksternal).
- *Switch bounce* mekanik berlangsung $5\text{--}30\text{ ms}$; kombinasikan **software debouncing berbasis waktu** ($50\text{ ms}$) dan **edge detection** agar satu penekanan menghasilkan tepat satu aksi.
- Untuk *external interrupt* ESP32, gunakan `IRAM_ATTR` dan `volatile` flag, serta pindahkan seluruh pemrosesan berat (`Serial`, logika FSM) ke `loop()`.
- Logika debounce telah diverifikasi secara *software* via `debounce_sim.py` (`outputs.md`); eksekusi `.ino` di board/Wokwi tetap berstatus **Belum diuji** di lingkungan server ini.

## Referensi

1. Espressif Systems, *ESP-IDF GPIO & RTC GPIO Documentation*, [https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/gpio.html](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/gpio.html) (diperiksa 2026-11-10).
2. Arduino Official Documentation, *Debounce on a Pushbutton & attachInterrupt()*, [https://docs.arduino.cc/built-in-examples/digital/Debounce/](https://docs.arduino.cc/built-in-examples/digital/Debounce/) (diperiksa 2026-11-10).
3. Wokwi Documentation, *Pushbutton Component & Bounce Simulation*, [https://docs.wokwi.com/parts/wokwi-pushbutton](https://docs.wokwi.com/parts/wokwi-pushbutton) (diperiksa 2026-11-10).

