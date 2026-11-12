# Latihan Bertingkat — Chapter 08

## Bagian A — Pertanyaan Konseptual & Metrologi

1. Jelaskan dengan contoh perbedaan antara **accuracy**, **precision**, dan **resolution**. Mengapa sebuah sensor bisa sangat presisi namun tidak akurat?
2. Kelompokkan masalah berikut ke dalam **systematic error** atau **random error**, dan tentukan cara mengatasinya:
   - (a) Resistor pembagi $10\text{ k}\Omega$ ternyata bernilai aktual $10{,}3\text{ k}\Omega$.
   - (b) Fluktuasi $\pm 15\text{ mV}$ pada pembacaan ADC akibat *switching regulator* USB.
   - (c) Pembacaan selalu lebih tinggi $1{,}8\,^\circ\text{C}$ di seluruh rentang ukur.
3. Sebuah sensor kelembaban memiliki konstanta waktu $\tau = 6\text{ detik}$. Jika sensor dipindahkan tiba-tiba dari ruangan $40\%$ RH ke ruang $80\%$ RH, berapa persen perubahan yang terbaca pada $t = 6\text{ s}$, dan berapa lama harus ditunggu hingga mencapai $\approx 99{,}3\%$ nilai akhir?

## Bagian B — Perhitungan Kalibrasi & Ketidakpastian

4. **Kalibrasi Dua Titik**:
   Sebuah sensor tekanan diuji pada dua titik referensi:
   - Pada $P_{\text{ref, L}} = 0{,}0\text{ kPa}$, sensor membaca $P_{\text{raw, L}} = 2{,}4\text{ kPa}$.
   - Pada $P_{\text{ref, H}} = 100{,}0\text{ kPa}$, sensor membaca $P_{\text{raw, H}} = 97{,}4\text{ kPa}$.
   Hitung nilai *slope* $m$, *offset* $b$, serta hasil terkalibrasi jika sensor membaca $P_{\text{raw}} = 52{,}4\text{ kPa}$.

5. **Propagasi Ketidakpastian Sederhana**:
   Pengukuran berulang $N = 9$ kali pada kondisi stabil menghasilkan rata-rata $\bar{T} = 30{,}12\,^\circ\text{C}$ dengan simpangan baku sampel $s = 0{,}09\,^\circ\text{C}$. Diketahui termometer referensi memiliki akurasi datasheet $\pm 0{,}20\,^\circ\text{C}$ (distribusi persegi) dan resolusi pembacaan berkontribusi $u_{B,\text{res}} = 0{,}02\,^\circ\text{C}$.
   - Hitung $u_A$, $u_{B,\text{ref}}$, $u_c$, dan ketidakpastian diperluas $U$ ($k = 2$).
   - Tuliskan hasil pengukuran final dalam format $\bar{T} \pm U$.

## Bagian C — Simulasi Software & Mini Challenge

6. **Validasi Kalibrasi via Python (`calibration_uncertainty.py`)**:
   Jalankan:
   ```sh
   python public/content/chapter-08/src/calibration_uncertainty.py
   ```
   **Mini Challenge**: Tambahkan fungsi regresi linier *Ordinary Least Squares* (OLS) yang memanfaatkan **seluruh 5 titik** pada `cal_curve` di `telemetry.csv`, lalu bandingkan nilai RMSE-nya terhadap model kalibrasi dua-titik ($0{,}0266\,^\circ\text{C}$).

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **Accuracy vs Precision vs Resolution**: Presisi tanpa akurasi terjadi saat sebaran data sangat rapat (*random error* kecil), tetapi pusat sebaran bergeser jauh dari nilai referensi akibat *systematic bias*.
2. **Klasifikasi Error**: (a) *Systematic* (atasi dengan mengukur nilai aktual R atau kalibrasi); (b) *Random* (atasi dengan *averaging* + kapasitor decoupling); (c) *Systematic offset* (atasi dengan kalibrasi *offset*).
3. **Response Time ($\tau = 6\text{ s}$)**: Pada $t = 1\tau = 6\text{ s}$, sensor mencapai $63{,}2\%$ perubahan ($40 + 0{,}632 \times 40 = 65{,}28\%$ RH). Untuk mencapai $99{,}3\%$, perlu menunggu $5\tau = 30\text{ detik}$.
4. **Kalibrasi Dua Titik**:
   - $m = (100{,}0 - 0{,}0) / (97{,}4 - 2{,}4) = 100 / 95 \approx 1{,}0526$.
   - $b = 0{,}0 - 1{,}0526 \times 2{,}4 = -2{,}5263\text{ kPa}$.
   - Pada $P_{\text{raw}} = 52{,}4\text{ kPa}$: $P_{\text{cal}} = 1{,}0526 \times 52{,}4 - 2{,}5263 \approx 52{,}63\text{ kPa}$.
5. **Ketidakpastian ($N=9, s=0{,}09$)**:
   - $u_A = 0{,}09 / \sqrt{9} = 0{,}0300\,^\circ\text{C}$.
   - $u_{B,\text{ref}} = 0{,}20 / \sqrt{3} \approx 0{,}1155\,^\circ\text{C}$.
   - $u_c = \sqrt{0{,}0300^2 + 0{,}1155^2 + 0{,}0200^2} \approx 0{,}1210\,^\circ\text{C}$.
   - $U = 2 \times 0{,}1210 \approx 0{,}24\,^\circ\text{C} \implies$ **$30{,}12 \pm 0{,}24\,^\circ\text{C}$** ($k=2$).

</details>

