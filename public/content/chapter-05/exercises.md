# Latihan Bertingkat — Chapter 05

## Bagian A — Pertanyaan Konseptual & Memori

1. Jelaskan mengapa penggunaan `uint16_t` dan `uint32_t` lebih disarankan daripada `int` polos pada *Firmware* mikrokontroler.
2. Pada bagian memori mana (`Flash`, `SRAM Statis`, `SRAM Stack`, atau `SRAM Heap`) item berikut disimpan?
   - (a) `constexpr float V_REF = 3.30f;`
   - (b) Variabel lokal `char buf[64];` di dalam `loop()`
   - (c) Variabel global `uint32_t lastSampleMs = 0;`
   - (d) Objek `String payload = String("T=") + temp;` yang dibuat berulang di `loop()`
3. Mengapa perbandingan `if (millis() >= nextRunMs)` bermasalah setelah perangkat menyala selama $\sim 49{,}7$ hari, sedangkan `if ((uint32_t)(millis() - prevRunMs) >= intervalMs)` tetap bekerja benar?

## Bagian B — Refaktor & Perancangan FSM

4. **Refaktor Blocking ke Non-Blocking**:
   Perbaiki potongan kode *blocking* berikut agar kedua LED berkedip independen (`LED_A` setiap $400\text{ ms}$, `LED_B` setiap $1000\text{ ms}$) dan `Serial` mencetak status setiap $2000\text{ ms}$ tanpa satu pun `delay()` di `loop()`:
   ```cpp
   void loop() {
     digitalWrite(25, HIGH); delay(400);
     digitalWrite(25, LOW);  delay(400);
     digitalWrite(26, HIGH); delay(1000);
     digitalWrite(26, LOW);  delay(1000);
     Serial.println("Tick");
   }
   ```
5. **Desain State Machine**:
   Gambarkan diagram transisi state (dalam bentuk teks/tabel) untuk pengering gabah mini dengan 4 state: `IDLE`, `HEATING` (maks 10 menit), `COOLING` (3 menit), dan `FAULT` (suhu berlebih). Tentukan pemicu masuk dan keluar untuk setiap state.

## Bagian C — Simulasi Software & Mini Challenge

6. **Verifikasi Rollover & FSM (`fsm_timing_sim.py`)**:
   Jalankan:
   ```sh
   python public/content/chapter-05/src/fsm_timing_sim.py
   ```
   **Mini Challenge**:
   - Pada salinan lokal `ex02_nonblocking_fsm.ino` (uji logikanya juga di salinan `fsm_timing_sim.py`), tambahkan state ke-4 yaitu **`COOLDOWN`**: ketika suhu turun di bawah $30{,}0\,^\circ\text{C}$ dari state `ALERT`, sistem tidak langsung ke `IDLE`, melainkan bertahan di `COOLDOWN` selama `3000 ms` dengan LED status berkedip tiap `500 ms` sebelum kembali ke `IDLE`.

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **Fixed-width integers**: Menjamin lebar bit dan rentang nilai konsisten lintas arsitektur MCU (8-bit/32-bit), menghindari *signed overflow*, dan menghemat SRAM.
2. **Lokasi Memori**: (a) Flash/RODATA (konstanta kompilasi); (b) SRAM Stack; (c) SRAM Statis; (d) SRAM Heap (berisiko fragmentasi jika berulang).
3. **Rollover 32-bit**: `millis()` bertipe `uint32_t` dengan nilai maks $2^{32}-1$ ($49{,}71\text{ hari}$). Pada aritmatika modular *unsigned*, `(now - prev)` tetap menghasilkan selisih waktu positif yang tepat melintasi batas `0xFFFFFFFF -> 0x00000000`, sedangkan `nextRunMs` bisa melompat ke nilai kecil yang langsung lebih kecil dari `millis()` sebelum rollover.
4. **Refaktor Non-Blocking**: Gunakan dua instance `BlinkTask` dari `led_timer.h` (masing-masing interval `400` dan `1000 ms`) serta satu variabel `lastLogMs` dengan interval `2000 ms` di `loop()`.
5. **FSM Pengering Gabah**: `IDLE` $\xrightarrow{\text{start}}$ `HEATING` $\xrightarrow{t \ge 10\text{m}}$ `COOLING` $\xrightarrow{t \ge 3\text{m}}$ `IDLE`; dari `HEATING` atau `COOLING` jika `temp > T_max` $\rightarrow$ `FAULT` (aktuator mati sampai reset manual).

</details>

