# Latihan Bertingkat — Chapter 10 (Persiapan Capstone)

## Bagian A — Review Integrasi Lintas-Chapter

1. Petakan setiap modul di [`capstone_env_monitor.ino`](content/chapter-10/src/capstone_env_monitor/capstone_env_monitor.ino) ke materi Level 1 yang mendasarinya (Chapter 03, 04, 05, 06, 07, 08, dan 09).
2. Mengapa pada fungsi `evaluateControl()`, pemeriksaan `interlockOpen` dan `isnan(latestTempC)` diletakkan **sebelum** pengecekan mode `MANUAL_ON`? Apa risikonya jika urutannya dibalik?
3. Jelaskan mengapa `GPIO 34` dipilih untuk `PIN_NTC_ADC` dan `GPIO 27` dipilih untuk `PIN_MODE_BUTTON` (bukan sebaliknya).

## Bagian B — Analisis Fault Injection

4. Prediksi isi payload JSON Serial yang dicetak oleh firmware Capstone pada kondisi berikut:
   - (a) Mode awal `AUTO_NORMAL`, suhu turun dari $30{,}2\,^\circ\text{C}$ ke $29{,}1\,^\circ\text{C}$.
   - (b) Mode `MANUAL_ON`, lalu kabel antara `GPIO 34` dan sensor NTC terlepas sehingga pin tertarik ke `3V3` ($3300\text{ mV}$).
   - (c) Suhu stabil $24{,}0\,^\circ\text{C}$, saklar interlock tertutup (`LOW`), lalu tombol `GPIO 27` ditekan sebanyak 2 kali beruntun (sudah ter-*debounce*).

## Bagian C — Verifikasi Test Harness & Mini Challenge

5. **Menjalankan Acceptance Test (`capstone_logic_test.py`)**:
   ```sh
   python public/content/chapter-10/src/capstone_logic_test.py
   ```
   Pastikan seluruh **13/13 skenario lulus**.
6. **Mini Challenge Capstone**:
   - Tambahkan aturan **Emergency Over-Temperature Override**: apabila suhu terukur mencapai $\ge 45{,}0\,^\circ\text{C}$ pada mode apa pun (kecuali saat `INTERLOCK_OPEN` atau `NaN`), kipas PWM langsung dipaksa ke **`255` (`100%` duty cycle)** dan `alarm = true` sampai suhu turun di bawah $42{,}0\,^\circ\text{C}$.
   - Implementasikan perubahan tersebut baik di salinan `capstone_env_monitor.ino` maupun di skrip uji `capstone_logic_test.py` dengan menambah minimal 2 baris skenario baru di `telemetry.csv`.

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **Pemetaan Lintas-Chapter**: Ch03 (resistor LED 220 $\Omega$, common GND, batas 3,3 V); Ch04 (pin aman ESP32-DevKitC V4); Ch05 (`env_config.h`, `millis()` non-blocking, `snprintf`); Ch06 (`INPUT_PULLUP` + *debounce* 50 ms tombol mode); Ch07 (`ADC1` + *moving average* + `LEDC` PWM 5 kHz); Ch08 (kurva NTC + kalibrasi 2-titik); Ch09 (driver MOSFET/flyback, histeresis, *interlock*, dan *fail-safe*).
2. **Urutan Keselamatan**: Jika `MANUAL_ON` dicek lebih dulu daripada `interlockOpen`, kipas akan tetap berputar meskipun tutup pelindung dibuka teknisi—melanggar prinsip *safety interlock*.
3. **Alasan Pin `34` vs `27`**: `GPIO 34` adalah pin *input-only* di `ADC1` tanpa *internal pull-up* (cocok untuk input analog, tidak bisa dipakai untuk tombol `INPUT_PULLUP` tanpa resistor luar), sedangkan `GPIO 27` mendukung `INPUT_PULLUP` internal.
4. **Prediksi Payload**:
   - (a) `fan: "ON"` (masih di dalam *deadband* $28\dots 30\,^\circ\text{C}$), `alarm: false`, `fault: "NONE"`.
   - (b) $3300\text{ mV} > 3200\text{ mV} \implies$ `temp_c: null`, `mode: "FAULT_SAFE"`, `fan: "OFF"`, `alarm: true`, `fault: "SENSOR_FAULT_NAN"`.
   - (c) Tekan ke-1 $\rightarrow$ `AUTO_STRICT` (`fan: "OFF"`), tekan ke-2 $\rightarrow$ `MANUAL_ON` (`fan: "ON"`).

</details>

