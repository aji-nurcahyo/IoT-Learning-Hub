# Modul D03 — Deep TinyML: Quantization-Aware Training, Structured Pruning & Knowledge Distillation

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memahami keterbatasan Post-Training Quantization (PTQ) dan menerapkan Quantization-Aware Training (QAT) dengan simulasi galat kuantisasi saat backpropagation.
2. Menerapkan aproksimasi gradien Straight-Through Estimator (STE) pada fungsi pembulatan kuantisasi diskrit.
3. Mengeksekusi pemangkasan filter konvolusi berstruktur (Structured Pruning) untuk mengurangi beban komputasi MAC.
4. Mentransfer pengetahuan dari model Teacher berkapasitas besar ke model Student kompak menggunakan loss distilasi Hinton.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 35.
- Modul Jalur Peminatan Prasyarat: Modul D01, Modul D02.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Keterbatasan Post-Training Quantization (PTQ) vs Quantization-Aware Training (QAT)
Pada kuantisasi pasca-pelatihan (*Post-Training Quantization* / PTQ), model dilatih secara penuh dalam format float32 presisi tinggi, kemudian bobot dan aktivasinya langsung dibulatkan ke INT8. Untuk model jaringan yang sangat dalam atau memiliki distribusi fitur sensitif, galat pembulatan kumulatif dapat menyebabkan anjloknya akurasi klasifikasi (*Accuracy Drop* > 5%).
**Quantization-Aware Training (QAT)** memodelkan efek kuantisasi bilangan bulat selama proses pelatihan berlangsung (*Forward Pass*). Bobot tetap diperbarui dalam format float berpresisi tinggi di *Backward Pass*, namun aktivasi dan bobot dibulatkan ke representasi diskrit sebelum dikalikan, sehingga jaringan secara alami beradaptasi terhadap distorsi kuantisasi.

### 2. Aproksimasi Gradien Straight-Through Estimator (STE)
Fungsi pembulatan kuantisasi ($q = 	ext{round}(x)$) merupakan fungsi tangga diskrit yang memiliki turunan nol di hampir semua titik ($rac{dq}{dx} = 0$) dan tidak terdefinisi pada titik peralihan. Jika turunan ini digunakan dalam backpropagation, gradien optimasi akan lenyap (*Vanishing Gradient*), menghentikan proses pembelajaran. Algoritma **Straight-Through Estimator (STE)** memecahkan paradoks ini dengan mengasumsikan secara heuristik bahwa gradien kuantisasi bernilai 1 di dalam rentang saturasi:
$$
rac{partial q}{partial x} approx egin{cases} 1, & 	ext{jika } |x| le x_{	ext{max}} \ 0, & 	ext{lainnya} end{cases}
$$

### 3. Landasan Matematis: Fungsi Kerugian Distilasi Pengetahuan Hinton (Mathematical Foundations)

Dalam distilasi model (*Knowledge Distillation*), model Student kecil dilatih meniru distribusi probabilitas halus (*soft probabilities*) yang dihasilkan model Teacher berkapasitas besar melalui parameter suhu pelunakan $T$:

$$
p_i(T) = rac{exp(z_i / T)}{sum_j exp(z_j / T)}
$$

Fungsi kerugian gabungan distilasi memadukan Cross-Entropy terhadap label tanah ($y$) dan divergensi Kullback-Leibler (KL) terhadap output Teacher:
$$
mathcal{L}_{	ext{KD}} = (1 - alpha) cdot mathcal{L}_{	ext{CE}}(y, p_s(1)) + alpha cdot T^2 cdot mathcal{L}_{	ext{KL}}(p_t(T), p_s(T))
$$

**Worked Numerical Example**:
Sebuah model klasifikasi 3 kelas menghasilkan logits $z = [2{,}0, quad 0{,}5, quad -1{,}0]$.
Pada suhu standar $T = 1$:
$$
exp(z) = [7{,}389, quad 1{,}649, quad 0{,}368] implies sum = 9{,}406
$$
$$
p(1) = [0{,}7855, quad 0{,}1753, quad 0{,}0391] quad (	ext{sangat terkonsentrasi pada kelas 1})
$$
Saat suhu dinaikkan ke $T = 3$:
$$
rac{z}{3} = [0{,}667, quad 0{,}167, quad -0{,}333]
$$
$$
exp(z/3) = [1{,}948, quad 1{,}182, quad 0{,}717] implies sum = 3{,}847
$$
$$
p(3) = [0{,}5064, quad 0{,}3072, quad 0{,}1864] quad (	ext{distribusi probabilitas lembut})
$$
Probabilitas lembut pada $T=3$ membawa informasi "pengetahuan gelap" (*dark knowledge*) bahwa kelas 2 memiliki kemiripan fitur lebih dekat dengan kelas 1 dibanding kelas 3, mentransfer representasi spasial yang kaya ke model Student mikrokontroler.

## Latihan

### Soal 1: Perhitungan Gradien STE (C3)
Sebuah bobot bernilai $w = 2{,}8$ pada skala kuantisasi $S = 0{,}02$ ($x_{	ext{max}} = 2{,}56$). Jika gradien loss yang masuk adalah $rac{partial mathcal{L}}{partial q} = -0{,}15$, hitung nilai gradien STE $rac{partial mathcal{L}}{partial w}$ yang diperbarui ke bobot!

### Soal 2: Evaluasi Kompresi Model (C4)
Sebuah model neural network memiliki 120.000 parameter FP32 (ukuran berkas: $480	ext{ KiB}$). Jika model tersebut dikuantisasi penuh ke INT8 ($1	ext{ byte/parameter}$) dan diterapkan structured pruning dengan rasio sparsity $40%$, hitung ukuran memori berkas biner akhir!

## Tugas

## Pelatihan Model TinyML Klasifikasi Getaran dengan QAT & Structured Pruning

Rancang alur kerja kompresi model deep learning kompak:
1. Latih model CNN 1D baseline dalam format float32 pada dataset fitur sensor.
2. Terapkan Quantization-Aware Training (QAT) dengan simulasi kuantisasi INT8 pada layer konvolusi.
3. Lakukan pemangkasan filter terstruktur hingga mencapai sparsity minimal $25%$.
4. Bandingkan akurasi, ukuran berkas FlatBuffers TFLite, dan estimasi siklus komputasi MAC.

## Ringkasan
- Modul D03 memberikan pemahaman mendalam dan terapan mengenai Deep TinyML: Quantization-Aware Training, Structured Pruning & Knowledge Distillation pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [tinyml_qat_compression_sim.py](src/tinyml_qat_compression_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Jacob, B., et al., Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference, IEEE CVPR, 2018, [https://openaccess.thecvf.com/content_cvpr_2018/papers/Jacob_Quantization_and_Training_CVPR_2018_paper.pdf](https://openaccess.thecvf.com/content_cvpr_2018/papers/Jacob_Quantization_and_Training_CVPR_2018_paper.pdf) (diperiksa 2026-11-18).
2. Hinton, G., et al., Distilling the Knowledge in a Neural Network, NIPS Deep Learning Workshop, 2014, [https://arxiv.org/abs/1503.02531](https://arxiv.org/abs/1503.02531) (diperiksa 2026-11-18).
