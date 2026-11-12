# Latihan Bertingkat — Chapter 03

## Bagian A — Pertanyaan Konseptual & Keselamatan

1. Mengapa dua modul (misalnya papan ESP32 yang dicatu USB dan modul sensor eksternal yang dicatu baterai 5 V) wajib memiliki koneksi **`GND` bersama (*common ground*)**?
2. Jelaskan mengapa menghubungkan *multimeter* dalam mode **Ammeter (mA/A)** secara paralel melintasi kutub `+5V` dan `GND` sangat berbahaya bagi rangkaian maupun multimeter.
3. Apa yang dimaksud dengan kondisi ***floating pin*** pada input digital, dan bagaimana resistor *pull-up* $10\text{ k}\Omega$ menyelesaikannya?

## Bagian B — Applied Engineering Problems

4. **Perhitungan Resistor LED & Batas Pin GPIO**:
   Anda memiliki GPIO bertegangan keluaran $3{,}3\text{ V}$ dengan batas arus aman desain $\le 10\text{ mA}$. Anda ingin menyalakan sebuah **LED biru** dengan tegangan maju $V_F = 3{,}0\text{ V}$ dan target arus sekitar $5\text{ mA}$.
   - Hitung nilai resistor ideal $R_{\text{min}}$ dan pilih resistor standar terdekat ($47\,\Omega, 68\,\Omega, 100\,\Omega, 220\,\Omega$).
   - Hitung arus aktual dan disipasi daya pada resistor tersebut.
   - Bagaimana jika Anda memasang **3 buah LED merah** ($V_F = 2{,}0\text{ V}$, masing-masing dengan resistor $220\,\Omega$) secara paralel pada **satu pin GPIO yang sama**? Hitung total arus yang ditarik dari pin tersebut!

5. **Perancangan Voltage Divider untuk Sensor $5\text{ V}$**:
   Sebuah sensor mengeluarkan sinyal digital $0\text{ V}$ (`LOW`) dan $5{,}0\text{ V}$ (`HIGH`), sedangkan input GPIO mikrokontroler memiliki batas maksimum $3{,}3\text{ V}$ (dan ambang minimum `HIGH` sebesar $2{,}5\text{ V}$).
   - Jika Anda memilih $R_1 = 10\text{ k}\Omega$ (terhubung ke output sensor $5\text{ V}$), tentukan nilai $R_2$ standar ($4{,}7\text{ k}\Omega, 10\text{ k}\Omega, 15\text{ k}\Omega, 22\text{ k}\Omega$) yang menghasilkan $V_{\text{out}}$ berada di antara $2{,}5\text{ V}$ dan $3{,}3\text{ V}$.
   - Hitung arus yang mengalir melewati pembagi tegangan saat sinyal bernilai $5\text{ V}$.

6. **Analisis Power Budget Baterai**:
   Sebuah node sensor lingkungan memakai baterai LiFePO4 berkapasitas $1500\text{ mAh}$ ($\eta_{\text{usable}} = 0{,}85$). Node bangun setiap $600\text{ detik}$ (10 menit): fase aktif berlangsung selama $4\text{ detik}$ dengan arus $75\text{ mA}$, dan fase *deep sleep* selama $596\text{ detik}$ dengan arus $0{,}10\text{ mA}$.
   - Hitung arus rata-rata $I_{\text{avg}}$ (mA).
   - Hitung estimasi lama operasi baterai dalam jam dan hari.

## Bagian C — Eksplorasi Software & Praktik Opsional

7. **Simulasi Perhitungan (Path A)**:
   Jalankan [`electronics_calc.py`](content/chapter-03/src/electronics_calc.py) dan verifikasi hasil perhitungan soal nomor 4–6 dengan memodifikasi parameter pada salinan lokal skrip.
8. **Praktik Opsional Hardware (Path B — Hanya jika alat tersedia)**:
   *Peringatan: Gunakan hanya sumber daya DC 3,3 V / 5 V, bukan listrik AC!*
   - Rangkai sebuah LED + resistor $220\,\Omega$ pada breadboard dari rail $+3{,}3\text{ V}$ ke `GND`.
   - Ukur tegangan jatuh melintasi resistor ($V_R$) dan melintasi LED ($V_F$) secara **paralel** dengan multimeter.
   - Hitung arus melalui Hukum Ohm ($I = V_R / R$) lalu bandingkan dengan hasil perhitungan teoretis. Catat kondisi dan toleransi komponen.

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **Common Ground**: Tegangan adalah beda potensial. Tanpa titik acuan `GND` yang sama, level tegangan sinyal dari sensor tidak terdefinisi relatif terhadap pin input MCU.
2. **Bahaya Ammeter Paralel**: Ammeter memiliki resistansi dalam sangat kecil (mendekati $0\,\Omega$). Memasangnya paralel melintasi rel daya menciptakan *short circuit* berarus besar yang merusak sekering meter, kabel, atau regulator catu daya.
3. **Floating Pin**: Pin input berimpedansi tinggi yang tidak terhubung ke rail daya maupun `GND` bertindak seperti antena penangkap *noise*. Resistor *pull-up* $10\text{ k}\Omega$ mengikat pin ke $+3{,}3\text{ V}$ saat saklar terbuka sehingga status idle pasti `HIGH`.
4. **LED Biru & 3 LED Paralel**:
   - $R_{\text{min}} = (3{,}3 - 3{,}0) / 0{,}005 = 60\,\Omega \rightarrow$ pilih **$68\,\Omega$**.
   - $I_{\text{aktual}} = 0{,}3 / 68 \approx 4{,}41\text{ mA}$; $P_R = 0{,}3 \times 0{,}00441 \approx 1{,}32\text{ mW}$.
   - 3 LED merah @ $220\,\Omega$ paralel: tiap LED menarik $(3{,}3 - 2{,}0)/220 = 5{,}91\text{ mA}$. Total arus pin = $3 \times 5{,}91 = 17{,}73\text{ mA}$ (melampaui batas desain aman $10\text{ mA}$!).
5. **Voltage Divider ($V_{\text{in}} = 5\text{ V}, R_1 = 10\text{ k}\Omega$)**:
   - Uji $R_2 = 15\text{ k}\Omega$: $V_{\text{out}} = 5 \times 15 / 25 = 3{,}00\text{ V}$ (aman di antara $2{,}5\dots 3{,}3\text{ V}$!). ($R_2 = 10\text{ k}\Omega$ memberi $2{,}50\text{ V}$ tepat di batas bawah; $R_2 = 22\text{ k}\Omega$ memberi $3{,}44\text{ V}$ — overvoltage!).
   - Arus divider saat $V_{\text{in}} = 5\text{ V}$: $I = 5 / (10\text{k} + 15\text{k}) = 0{,}2\text{ mA}$.
6. **Power Budget ($1500\text{ mAh}, \eta = 0{,}85$)**:
   - $I_{\text{avg}} = \frac{(75 \times 4) + (0{,}10 \times 596)}{600} = \frac{300 + 59{,}6}{600} = 0{,}5993\text{ mA}$.
   - Kapasitas efektif = $1500 \times 0{,}85 = 1275\text{ mAh}$.
   - Estimasi umur = $1275 / 0{,}5993 \approx 2127{,}4\text{ jam} \approx 88{,}6\text{ hari}$.

</details>

