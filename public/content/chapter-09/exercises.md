# Latihan Bertingkat — Chapter 09

## Bagian A — Pertanyaan Konseptual & Keselamatan Driver

1. Mengapa pin GPIO ESP32 tidak boleh digunakan untuk menggerakkan motor DC $5\text{ V}$ atau koil relay $5\text{ V}$ secara langsung? Sebutkan **tiga** mekanisme kerusakan atau kegagalan yang dapat terjadi.
2. Jelaskan fungsi masing-masing komponen pada rangkaian *low-side N-MOSFET driver*:
   - (a) Resistor seri $220\,\Omega$ menuju *gate*
   - (b) Resistor *pull-down* $10\text{ k}\Omega$ dari *gate* ke `GND`
   - (c) Dioda *flyback* antiparalel di sisi beban induktif
3. Jelaskan perbedaan kontrol *open-loop* vs *closed-loop*, serta mengapa *closed-loop* dengan satu ambang batas rentan mengalami *chattering*.

## Bagian B — Applied Engineering & Perhitungan

4. **Perhitungan PWM Servo & Motor DC**:
   - Sebuah motor servo standar menerima sinyal PWM $50\text{ Hz}$. Berapa periode ($T$) dalam milidetik? Jika menggunakan resolusi LEDC **16-bit** (`0..65535`), berapa nilai integer `duty` untuk menghasilkan lebar pulsa $1{,}5\text{ ms}$ ($90^\circ$)?
   - Sebuah kipas DC $12\text{ V}$ menarik arus $250\text{ mA}$ saat menyala penuh. Jika digerakkan dengan *duty cycle* $80\%$ via MOSFET driver, perkirakan arus rata-rata yang ditarik dari suplai $12\text{ V}$ (abaikan *switching loss*).

5. **Analisis Histeresis**:
   Sebuah sistem pendingin ruangan memiliki ambang nyala $T_{\text{high}} = 26{,}0\,^\circ\text{C}$ dan mati $T_{\text{low}} = 24{,}0\,^\circ\text{C}$. Kondisi awal kipas adalah `OFF`. Tentukan status kipas pada urutan pembacaan suhu berikut:
   `[24.5, 25.8, 26.2, 25.5, 24.3, 23.9, 25.1, NaN]` (asumsikan kondisi *fail-safe* menghentikan kipas).

## Bagian C — Simulasi Software & Mini Challenge

6. **Eksperimen Histeresis (`hysteresis_control_sim.py`)**:
   Jalankan:
   ```sh
   python public/content/chapter-09/src/hysteresis_control_sim.py
   ```
   **Mini Challenge**:
   - Modifikasi salinan skrip untuk menguji *deadband* sempit ($T_{\text{low}} = 29{,}7\,^\circ\text{C}, T_{\text{high}} = 30{,}0\,^\circ\text{C}$) terhadap `telemetry.csv`, lalu amati apakah *chattering* kembali muncul!
   - Pada salinan [`ex01_hysteresis_driver.ino`](content/chapter-09/src/ex01_hysteresis_driver/ex01_hysteresis_driver.ino), tambahkan aturan *minimum on-time* selama `5000 ms` menggunakan `millis()` agar kipas tidak mati sebelum beroperasi minimal 5 detik (kecuali saat *safety interlock* atau `NaN` terpicu — keselamatan tetap prioritas #1!).

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **Bahaya GPIO Langsung ke Motor/Relay**: (1) *Overcurrent* merusak pin GPIO ($>12\text{--}40\text{ mA}$); (2) *Voltage mismatch* ($3{,}3\text{ V}$ tidak cukup untuk beban $5\text{ V}$) + *brownout* regulator; (3) Lonjakan tegangan induktif ($L\,dI/dt$) saat beban dimatikan merusak chip.
2. **Fungsi 3 Komponen Driver**: (a) $220\,\Omega$ membatasi arus pengisian kapasitansi *gate* agar pin GPIO aman; (b) $10\text{ k}\Omega$ *pull-down* mencegah *gate* mengambang dan menyalakan beban saat MCU boot/reset (*fail-safe*); (c) *Flyback diode* mengalirkan arus induktif balik saat saklar membuka sehingga tegangan lonjakan terklamp aman.
3. **Open-Loop vs Closed-Loop & Chattering**: *Open-loop* tidak memakai umpan balik sensor; *closed-loop* membandingkan hasil ukur dengan *setpoint*. Satu ambang batas mengalami *chattering* karena *noise* kecil membuat sinyal bolak-balik melintasi batas tunggal.
4. **Servo $50\text{ Hz}$ (16-bit)**:
   - $T = 1 / 50\text{ Hz} = 20\text{ ms}$.
   - $\text{Duty} = (1{,}5 / 20{,}0) \times 65535 \approx 4915$.
   - Kipas $12\text{ V}$, $250\text{ mA}$ @ $80\%$ duty $\implies I_{\text{avg}} \approx 0{,}80 \times 250 = 200\text{ mA}$.
5. **Urutan Status Histeresis ($24{,}0\dots 26{,}0\,^\circ\text{C}$)**:
   - `24.5` $\rightarrow$ `OFF` (awal OFF, masih di bawah 26,0)
   - `25.8` $\rightarrow$ `OFF`
   - `26.2` $\rightarrow$ **`ON`** ($\ge 26{,}0$)
   - `25.5` $\rightarrow$ `ON` (masih di deadband)
   - `24.3` $\rightarrow$ `ON`
   - `23.9` $\rightarrow$ **`OFF`** ($\le 24{,}0$)
   - `25.1` $\rightarrow$ `OFF`
   - `NaN` $\rightarrow$ **`FAIL_SAFE_OFF` + Alarm ON**.

</details>

