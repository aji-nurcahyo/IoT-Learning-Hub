# Modul C01 — Agro-Ecological System Modeling & In-Situ Sensing Constraints

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Menganalisis kurva karakteristik retensi air tanah (SWRC) untuk menentukan titik layu permanen dan kapasitas lapang.
2. Mengimplementasikan Persamaan Topp untuk konversi permitivitas relatif dielektrik tanah ke kadar air volumetrik (VWC).
3. Menerapkan teknik eksitasi gelombang AC frekuensi tinggi untuk menekan polarisasi ionik dan korosi elektroda in-situ.
4. Melakukan analisis sensitivitas kadar air terhadap variasi salinitas tanah dan kesalahan kedalaman pemasangan.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 01, Chapter 03, Chapter 07.
- Modul Jalur Peminatan Prasyarat: Tidak ada (modul awal jalur peminatan).
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Karakteristik Fisika Tanah & Retensi Air (Soil Water Retention Curve)
Tanah pertanian merupakan media berpori heterogen yang tersusun atas tiga fase: matriks padatan mineral dan bahan organik, larutan air tanah beserta ion terlarut, serta fase gas (udara tanah). Distribusi air dalam pori-pori tanah diatur oleh tegangan matriks (*matric potential* $\psi_m$) yang dinyatakan dalam satuan kilopascal ($\text{kPa}$) atau bar.

Kurva karakteristik retensi air tanah (*Soil Water Retention Curve* / SWRC) mendefinisikan hubungan non-linear antara potensial hisap matriks $\psi_m$ dan kadar air volumetrik tanah ($\text{VWC}$ atau $\theta$). Dua titik batas agronomi fundamental yang menentukan ketersediaan air bagi perakaran tanaman adalah:
1. **Kapasitas Lapang (Field Capacity / $\theta_{\text{FC}}$)**: Kadar air yang tersisa di dalam tanah setelah air gravitasi berlebih terbuang tuntas akibat gaya tarik bumi (tercapai pada tegangan hisap $\approx -10\text{ s.d } -33\text{ kPa}$).
2. **Titik Layu Permanen (Permanent Wilting Point / $\theta_{\text{PWP}}$)**: Kadar air tanah kritis di mana gaya hisap akar tanaman tidak mampu lagi melawan tegangan kapiler matriks tanah (tercapai pada tegangan hisap $\approx -1500\text{ kPa}$), menyebabkan tanaman layu secara ireversibel.

Rentang antara kapasitas lapang dan titik layu permanen didefinisikan sebagai Total Air Tersedia (*Total Available Water* / TAW):
$$
\text{TAW} = \theta_{\text{FC}} - \theta_{\text{PWP}}
$$

### 2. Teori Sensor Dielektrik & Persamaan Topp (1980)
Pengukuran kadar air tanah secara in-situ non-destruktif mengandalkan disparitas permitivitas relatif dielektrik ($\epsilon_r$) antara konstituen tanah:
- Permitivitas udara kering: $\epsilon_{\text{air}} \approx 1$
- Permitivitas partikel mineral padat tanah: $\epsilon_{\text{mineral}} \approx 3 - 5$
- Permitivitas air bebas pada suhu $20^\circ\text{C}$: $\epsilon_{\text{water}} \approx 80{,}3$

Karena permitivitas air murni jauh melampaui udara dan mineral tanah, permitivitas bulk campuran tanah sangat didominasi oleh fraksi volume air bebas. Pada tahun 1980, G. C. Topp memformulasikan persamaan empiris universal yang memetakan permitivitas bulk $\epsilon_r$ (diukur menggunakan TDR/FDR) ke kadar air volumetrik $\theta$:
$$
\theta = -5{,}3 \times 10^{-2} + 2{,}92 \times 10^{-2} \epsilon_r - 5{,}5 \times 10^{-4} \epsilon_r^2 + 4{,}3 \times 10^{-6} \epsilon_r^3
$$

### 3. Mitigasi Polarisasi Ionik & Korosi Elektroda In-Situ
Sensor resistif kontak langsung DC sering mengalami kegagalan fatal di lapangan dalam waktu beberapa minggu akibat:
1. **Polarisasi Ionik**: Akumulasi ion hidrogen dan hidroksil pada antarmuka elektroda-tanah yang membentuk lapisan ganda listrik Helmholtz, menghasilkan resistansi semu dan deviasi pengukuran masif.
2. **Korosi Galvanik Anodik**: Arus DC mengalirkan elektron secara searah yang melarutkan logam probe tembaga atau besi ke dalam larutan asam tanah.

Solusi rekayasa wajib menerapkan eksitasi gelombang kotak AC simetris berfrekuensi tinggi ($f_{\text{exc}} \ge 50\text{ kHz}$ hingga $100\text{ MHz}$ pada metode kapasitif/FDR) dengan isolasi dielektrik (lapisan conformal pelindung polimer/FR4 berlapis solder mask industri) sehingga probe beroperasi murni secara kopling kapasitif tanpa transfer muatan galvanik langsung ke tanah.

### 4. Landasan Matematis: Persamaan Topp & Model Kompleks Maxwell-De Loor

1. **Persamaan Polinomial Topp (1980)**:
   $$
   \theta(\epsilon_r) = -0{,}053 + 0{,}0292 \epsilon_r - 5{,}5 \times 10^{-4} \epsilon_r^2 + 4{,}3 \times 10^{-6} \epsilon_r^3
   $$
   dengan domain validitas permitivitas tanah $1 \le \epsilon_r \le 45$.

2. **Sensitivitas Pengukuran Derivatif Relatif**:
   Sensitivitas pembacaan $\frac{d\theta}{d\epsilon_r}$ mengukur seberapa besar perubahan VWC terhadap fluktuasi permitivitas terukur:
   $$
   \frac{d\theta}{d\epsilon_r} = 0{,}0292 - 1{,}1 \times 10^{-3} \epsilon_r + 1{,}29 \times 10^{-5} \epsilon_r^2
   $$
   Pada $\epsilon_r = 18{,}4$:
   $$
   \frac{d\theta}{d\epsilon_r} = 0{,}0292 - 1{,}1 \times 10^{-3}(18{,}4) + 1{,}29 \times 10^{-5}(18{,}4)^2 = 0{,}0292 - 0{,}02024 + 0{,}00437 = 0{,}01333 \text{ VWC/unit } \epsilon_r
   $$

3. **Worked Numerical Example (Contoh Perhitungan Rinci)**:
   - **Parameter Masukan**: Permitivitas terukur $\epsilon_r = 18{,}4$, kapasitas lapang $\theta_{\text{FC}} = 0{,}28$, titik layu $\theta_{\text{PWP}} = 0{,}12$.
   - **Perhitungan VWC**:
     $$
     \theta = -0{,}053 + (0{,}0292 \times 18{,}4) - (5{,}5 \times 10^{-4} \times 18{,}4^2) + (4{,}3 \times 10^{-6} \times 18{,}4^3)
     $$
     $$
     \theta = -0{,}053 + 0{,}53728 - 0{,}18621 + 0{,}02678 = 0{,}3248 \text{ atau } 32{,}48\%
     $$
   - **Evaluasi Agronomi**: Karena $\theta = 0{,}3248 > \theta_{\text{FC}} = 0{,}28$, tanah berada pada kondisi kapasitas lapang optimal menuju jenuh; irigasi harus dihentikan untuk menghindari limpasan gravitasi (*deep percolation*).

## Latihan

## Latihan Pemahaman Mandiri

1. **Mengapa permitivitas dielektrik relatif air murni ($approx 80$) jauh lebih tinggi dibandingkan permitivitas matriks mineral padat tanah ($approx 3 - 5$)?**
   - *Jawaban*: Molekul air ($H_2O$) memiliki momen dipol listrik permanen yang sangat kuat dan mampu berotasi bebas mengikuti osilasi medan elektromagnetik eksternal pada frekuensi radio, menghasilkan permitivitas orientasi yang sangat tinggi dibandingkan struktur kisi mineral kristalin yang terikat kaku.

2. **Apa dampak utama celah udara (air gap) mikro di sekitar elektroda sensor kapasitif tanah terhadap hasil pembacaan kadar air?**
   - *Jawaban*: Celah udara memiliki permitivitas dielektrik terendah ($epsilon_{	ext{air}} approx 1$). Garis medan listrik akan terkonsentrasi melewati celah udara dengan impedansi tinggi tersebut, menyebabkan sensor mengukur permitivitas bulk yang jauh lebih rendah daripada kondisi tanah aktual, menghasilkan *under-estimation* kelembaban tanah hingga 30–50%.

## Tugas

## Penugasan Mandiri: Pemodelan Retensi & Sensitivitas Dielektrik Tanah In-Situ

Kembangkan modul Python yang mengimplementasikan Persamaan Topp dan menganalisis sensitivitas kadar air terhadap variasi salinitas semu. Buat fungsi pembatasan yang mengklasifikasikan status kelembaban tanah berdasarkan nilai kapasitas lapang dan titik layu jenis tanah lempung berpasir (*sandy loam*).

## Ringkasan
- Modul C01 memberikan pemahaman mendalam dan terapan mengenai Agro-Ecological System Modeling & In-Situ Sensing Constraints pada tingkat kedalaman L2: Undergraduate Complete.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [soil_moisture_topp_sim.py](src/soil_moisture_topp_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Topp, G. C. et al., Electromagnetic Determination of Soil Water Content: Measurements in Coaxial Transmission Lines, Water Resources Research, 1980, [https://doi.org/10.1029/WR016i003p00574](https://doi.org/10.1029/WR016i003p00574) (diperiksa 2026-11-18).
2. ISO 11271:2022, Soil Quality — Determination of Redox Potential, [https://www.iso.org/standard/79262.html](https://www.iso.org/standard/79262.html) (diperiksa 2026-11-18).
