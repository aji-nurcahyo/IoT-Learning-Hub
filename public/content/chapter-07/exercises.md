# Latihan Bertingkat — Chapter 07

## Bagian A — Perhitungan Kuantisasi, PWM & Nyquist

1. Sebuah sensor menghasilkan tegangan analog $0\dots 3{,}30\text{ V}$ yang dibaca oleh ADC **12-bit**.
   - Hitung besar $1\text{ LSB}$ dalam milivolt ($\text{mV}$).
   - Jika nilai ADC terbaca `2730`, berapa tegangan input idealnya?
   - Berapa batas kesalahan kuantisasi idealnya ($\pm 0{,}5\text{ LSB}$)?
2. Sinyal PWM bertegangan $3{,}3\text{ V}$ menggunakan resolusi **10-bit** (`0..1023`). Jika nilai duty ditulis `384`, hitung persentase *duty cycle* dan tegangan rata-rata $V_{\text{avg}}$-nya.
3. Sinyal getaran mesin memiliki frekuensi fundamental $70\text{ Hz}$. Jika Anda melakukan *sampling* pada $f_s = 100\text{ Hz}$:
   - Apakah kriteria Nyquist terpenuhi?
   - Pada frekuensi berapa komponen $70\text{ Hz}$ akan muncul akibat *aliasing*?
   - Berapa $f_s$ minimum praktis (gunakan aturan $5\times f_{\max}$) agar bentuk gelombang terekam baik?

## Bagian B — Analisis Desain ESP32

4. Rekan Anda menulis `analogRead(4)` untuk membaca sensor kelembaban tanah sementara perangkat juga akan menyalakan Wi-Fi di Level 2. Jelaskan mengapa pilihan `GPIO 4` bermasalah pada ESP32-WROOM-32 dan sebutkan 3 pin pengganti yang aman.
5. Mengapa `analogReadMilliVolts()` lebih disarankan daripada rumus manual `(analogRead(pin) / 4095.0) * 3.3` pada ESP32?

## Bagian C — Simulasi Software & Mini Challenge

6. **Eksperimen Python (`adc_nyquist_sim.py`)**:
   Jalankan:
   ```sh
   python public/content/chapter-07/src/adc_nyquist_sim.py
   ```
   **Mini Challenge**: Modifikasi salinan skrip untuk menguji *moving average* dengan $N = 8$ pada `telemetry.csv`, lalu bandingkan simpangan baku antara $N = 1$ (mentah), $N = 4$, dan $N = 8$.
7. **Mini Challenge Firmware (Path A Wokwi / Path B Opsional)**:
   Pada [`ex01_adc_pwm_dimmer.ino`](content/chapter-07/src/ex01_adc_pwm_dimmer/ex01_adc_pwm_dimmer.ino), ubah pemetaan kecerahan LED dari linier menjadi **kurva kuadratik (*gamma correction* $\approx 2$)**:
   $$\text{norm} = \frac{\text{clampedMv}}{3300{,}0}, \qquad \text{duty} = \lfloor \text{norm}^2 \times 1023 \rfloor$$
   Jelaskan mengapa mata manusia mempersepsikan perubahan kecerahan kuadratik lebih mulus di tingkat redup!

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **ADC 12-bit ($3{,}30\text{ V}$)**:
   - $1\text{ LSB} = 3300 / 4095 \approx 0{,}8059\text{ mV}$.
   - Tegangan pada `2730`: $2730 \times 3{,}30 / 4095 \approx 2{,}200\text{ V}$.
   - Kesalahan kuantisasi ideal: $\pm 0{,}403\text{ mV}$.
2. **PWM 10-bit (`384/1023`)**:
   - $D = (384 / 1023) \times 100\% \approx 37{,}54\%$.
   - $V_{\text{avg}} = 0{,}3754 \times 3{,}3\text{ V} \approx 1{,}239\text{ V}$.
3. **Nyquist ($f_{\text{sig}} = 70\text{ Hz}, f_s = 100\text{ Hz}$)**:
   - Tidak terpenuhi ($100 \ngtr 2 \times 70 = 140\text{ Hz}$).
   - Frekuensi alias: $|70 - 100| = 30\text{ Hz}$.
   - Rekomendasi praktis ($5\times$): $f_s \ge 350\text{ Hz}$.
4. **ADC2 + Wi-Fi**: `GPIO 4` berada di unit `ADC2` yang digunakan bersama subsistem Wi-Fi pada ESP32 klasik. Pengganti aman (`ADC1`): `GPIO 32`, `GPIO 34`, `GPIO 35`, `GPIO 36`, atau `GPIO 39`.
5. **`analogReadMilliVolts()`**: Memanfaatkan data kalibrasi *eFuse* per-chip dari pabrik untuk mengoreksi tegangan referensi internal (~1,1 V yang bervariasi antar-chip) serta non-linearitas ADC ESP32.

</details>

