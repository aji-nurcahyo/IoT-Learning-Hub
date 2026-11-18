# Chapter 22 — Raspberry Pi, Linux & IoT Gateways

Pada instalasi skala industri atau smart campus, tidak semua sensor nirkabel dan mikrokontroler mikro memiliki koneksi TCP/IP langsung ke jaringan luar. Banyak perangkat beroperasi menggunakan antarmuka serial berdaya rendah seperti UART, RS485/Modbus, BLE, atau sub-GHz radio. Untuk menjembatani dunia perangkat lapangan (*field devices*) dengan infrastruktur jaringan berbasis IP, diperlukan sebuah **IoT Edge Gateway**.

Papan komputasi tunggal (*Single Board Computer* / SBC) berbasis Linux seperti **Raspberry Pi** merupakan standar industri de facto untuk prototipe hingga gerbang edge komersial. Bab ini membahas arsitektur gateway berbasis sistem operasi Linux, konfigurasi komunikasi serial TTY non-blocking, manajemen dependensi Python dengan *virtual environment*, supervisi *daemon* menggunakan `systemd`, serta penanganan kegagalan secara deterministik.

![Arsitektur IoT Gateway: Raspberry Pi, Antarmuka Serial, dan Broker MQTT](content/chapter-22/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan bab ini, Anda diharapkan mampu:

1. **Memahami Arsitektur Edge Gateway**: Menjelaskan peran strategis gateway dalam topologi hierarkis IoT (penerjemah protokol, penyaring noise, dan *local buffer*).
2. **Mengonfigurasi Antarmuka Serial Linux**: Mengelola port perangkat serial (`/dev/ttyUSB0` atau `/dev/ttyAMA0`), mengatur hak akses grup `dialout`, serta mengonfigurasi parameter *line discipline* (baudrate, parity, framing).
3. **Membangun Daemon Jembatan Serial-ke-MQTT**: Mengembangkan program Python modular yang membaca frame berformat ASCII/biner, memvalidasi integritas data berbasis *checksum*, dan mempublikasikan data ke broker MQTT.
4. **Menerapkan Manajemen Layanan `systemd`**: Menyusun file unit `systemd` lengkap dengan parameter *sandboxing*, isolasi pengguna non-root, pemulihan otomatis saat *crash* (`Restart=always`), dan pembatasan sumber daya.
5. **Mendiagnosis Kesehatan Gateway**: Memanfaatkan perangkat diagnostik Linux modern (`journalctl`, `systemctl status`, `lsof`, `top`) untuk memonitor utilisasi memori dan jejak log secara *real-time*.

## Prasyarat

- Memahami konsep dasar komunikasi serial UART, baudrate, dan framing bit dari [Chapter 04](chapter-04) dan [Chapter 16](chapter-16).
- Memahami konsep arsitektur MQTT dari [Chapter 14](chapter-14).
- Memahami dasar navigasi terminal Linux/POSIX (perintah dasar shell `bash`, izin file `chmod`/`chown`).

## Konsep dan teori

### 1. Peran Arsitektural IoT Gateway

Gateway berada pada batas antara jaringan fisik lokal (*Field Network*) dan jaringan backbone (*Enterprise/Cloud Network*). Tiga fungsi utamanya meliputi:

1. **Penerjemahan Protokol (*Protocol Translation*)**: Mengonversi paket non-IP (misal: frame serial UART `$DATA,...*CS`) menjadi paket standar IP (MQTT/JSON melalui TCP/IP).
2. **Isolasi Keamanan (*Security Boundary*)**: Melindungi mikrokontroler berdaya rendah dari serangan jaringan eksternal; mikrokontroler tidak memiliki alamat IP publik atau soket terbuka yang rentan dieksploitasi.
3. **Offline Spooling & Local Caching**: Menampung data dalam basis data lokal saat koneksi internet terputus, sehingga tidak ada telemetri yang hilang.

### 2. Antarmuka Serial Linux (`termios` & TTY)

Pada kernel Linux, port serial direpresentasikan sebagai file karakter khusus di direktori `/dev/`:
- `/dev/ttyUSB0`: Perangkat USB-ke-UART converter (chip FTDI, CP2102, CH340).
- `/dev/ttyAMA0` atau `/dev/serial0`: UART bawaan pada header GPIO Raspberry Pi (Pin 8 TXD, Pin 10 RXD).

Agar program daemon dapat membuka port serial tanpa hak istimewa `root`, pengguna harus dimasukkan ke dalam grup sistem `dialout`:

```bash
sudo usermod -aG dialout iotgateway
```

### 3. Protokol Framing dan Integritas Checksum

Data serial mentah rentan mengalami *framing error* atau derau elektromagnetik. Oleh karena itu, stream serial wajib dibungkus dalam format *framing* yang memiliki penanda awal (*start delimiter*), pemisah token, penanda akhir, dan kode pemeriksa kesalahan:

$$\text{Format Frame} = \$ \text{HEADER} , \text{TOKEN}_{1} , \dots , \text{TOKEN}_{N} * \text{CHECKSUM} \backslash \text{r} \backslash \text{n}$$

Pada skrip [`serial_mqtt_gateway.py`](content/chapter-22/src/serial_mqtt_gateway.py), digunakan algoritma **Longitudinal Redundancy Check (LRC)** 8-bit hex untuk memastikan tidak ada byte yang terkorupsi selama transmisi kabel:

$$\text{LRC} = \left( \left( \sum_{i=1}^{m} b_i \bmod 256 \right) \oplus \text{0xFF} \right) + 1$$

Jika nilai *checksum* yang dihitung tidak sama dengan nilai yang diterima, frame langsung dibuang dan dicatat ke log peringatan.

### 4. Daemon Architecture & Penanganan Sinyal POSIX

Sebuah *daemon* IoT yang tangguh harus mampu menangani sinyal sistem operasi secara elegan (*graceful termination*):
- `SIGINT` (interupsi keyboard, Ctrl+C).
- `SIGTERM` (sinyal penghentian standar dari `systemctl stop`).

Saat menerima `SIGTERM`, daemon tidak boleh langsung mati mendadak, melainkan harus:
1. Menyelesaikan proses pembacaan frame yang sedang aktif.
2. Menutup port serial dan koneksi soket MQTT secara bersih.
3. Mengosongkan buffer penyimpanan sementara ke disk.
4. Keluar dengan kode status `0`.

### 5. Supervisi Layanan dengan `systemd`

Untuk menjamin ketersediaan tinggi (*high availability*), proses gateway dijalankan sebagai *system service* yang diawasi oleh `systemd` ([`iot-gateway.service`](content/chapter-22/src/iot-gateway.service)):

- `Restart=always`: Memulai ulang proses secara otomatis jika mengalami crash mendadak.
- `RestartSec=5s`: Memberi jeda 5 detik sebelum me-restart untuk mencegah beban berlebih (*CPU spin lock*).
- `ProtectSystem=full` & `ProtectHome=true`: Mengunci direktori sistem dari modifikasi ilegal (prinsip *least privilege*).
- `LimitNOFILE=65536`: Memperluas kuota *file descriptor* untuk koneksi socket yang banyak.

### 3.1 Landasan Matematis: Buffer Dimensioning & Latensi Pemrosesan Gateway (Mathematical Foundations)

Sebagai jembatan antara bus sensor fisik dan infrastruktur IP, gateway bertindak sebagai sistem antrean $M/M/1$:

1. **Pemodelan Antrean Gateway (Queueing Model)**:
   Jika kedatangan paket dari simpul sensor memiliki laju rata-rata $\lambda$ (paket/detik) berdistribusi Poisson, dan laju layanan transmisi gateway ke broker cloud adalah $\mu$ (paket/detik) dengan syarat kestabilan $\rho = \frac{\lambda}{\mu} < 1$:
   - Jumlah rata-rata paket dalam antrean buffer gateway $L_q$ adalah:
     $$
     L_q = \frac{\rho^2}{1 - \rho} = \frac{\lambda^2}{\mu(\mu - \lambda)}
     $$
   - Waktu tunggu rata-rata paket di gateway sebelum terkirim $W$ dirumuskan menurut Teorema Little:
     $$
     W = \frac{1}{\mu - \lambda}
     $$

2. **Perhitungan Waktu Tunggu Gateway Terhadap Utilitas (Worked Example)**:
   Sebuah gateway mengumpulkan data dari 50 sensor dengan total laju kedatangan $\lambda = 80\text{ paket/detik}$. Kapasitas pemrosesan dan enkapsulasi JSON gateway mencapai $\mu = 100\text{ paket/detik}$.
   Faktor utilitas gateway $\rho$ adalah:
   $$
   \rho = \frac{80}{100} = 0{,}80 \quad (80\%)
   $$
   Waktu tinggal rata-rata paket di gateway:
   $$
   W = \frac{1}{100 - 80} = \frac{1}{20} = 0{,}05\text{ detik } (50\text{ ms})
   $$
   Jika koneksi internet mengalami degradasi sehingga laju pengiriman turun menjadi $\mu' = 85\text{ paket/detik}$ (utilitas melonjak ke $\rho = 0{,}941$), maka waktu tunggu rata-rata melonjak drastis menjadi $W' = \frac{1}{85 - 80} = 0{,}20\text{ detik}$ ($200\text{ ms}$). Pemodelan ini membuktikan perlunya alokasi thread pool asinkron agar gateway tidak mengalami penumpukan antrean (*queue explosion*).

## Latihan

1. **Analisis Izin Akses Linux**:
   Jika sebuah skrip Python mencoba mengakses `/dev/ttyUSB0` dan menghasilkan kesalahan `PermissionError: [Errno 13] Permission denied: '/dev/ttyUSB0'`, jelaskan langkah konfigurasi grup Linux yang benar tanpa menggunakan `chmod 777` yang membahayakan keamanan sistem.
2. **Perhitungan Checksum LRC**:
   Hitung secara manual nilai *checksum* LRC 8-bit hex untuk string pesan `$DATA,NODE-A,10,25.5*` menggunakan rumus komplemen dua.
3. **Analisis Kegagalan Daemon**:
   Jelaskan mengapa opsi `Restart=always` pada unit `systemd` harus dikombinasikan dengan `RestartSec=5s` dan `StartLimitIntervalSec`. Apa konsekuensinya jika direktori serial terus-menerus gagal dibuka karena kabel terlepas?

## Tugas

Rancang dan konfigurasikan paket perangkat lunak IoT Gateway berbasis Python dan systemd untuk Raspberry Pi:

1. **Implementasi Gateway Serial-MQTT**:
   Buat modul gateway yang mampu membaca frame serial berpenanda, memverifikasi integritas data dengan checksum, dan menerbitkan hasil parsing ke broker MQTT lokal.
2. **Penanganan Sinyal Graceful Shutdown**:
   Pastikan skrip mendaftarkan signal handler `SIGINT` dan `SIGTERM` sehingga daemon dapat dimatikan dengan aman tanpa menyisakan port terkunci (*resource leak*).
3. **Konfigurasi Unit systemd**:
   Tulis file service `iot-gateway.service` dengan aturan isolasi user non-root dan supervisi pemulihan otomatis saat terjadi crash.

### Rubrik Penilaian

| Kriteria | Bobot | Deskripsi Teknis |
| :--- | :---: | :--- |
| **Parsing Serial & Validasi Checksum** | 40% | Frame serial di-parse dengan akurat; deteksi frame korup atau noise berhasil dibuktikan melalui pengujian unit. |
| **Arsitektur Daemon & Graceful Shutdown** | 30% | Skrip menangani sinyal sistem operasi secara elegan dan menutup seluruh resource secara bersih saat dihentikan. |
| **Konfigurasi systemd & Keamanan** | 30% | File unit mengimplementasikan prinsip least privilege (user non-root), pembatasan akses sistem, dan kebijakan restart otomatis. |

## Ringkasan

1. **Jembatan Protokol**: IoT Gateway menghubungkan perangkat lapangan non-IP dengan jaringan berbasis IP modern.
2. **Keandalan Serial**: Penggunaan start delimiter, format token eksplisit, dan checksum LRC/CRC wajib diterapkan untuk menyaring derau fisik.
3. **Graceful Handling**: Handler sinyal POSIX memastikan daemon melepaskan port serial dan menutup soket secara bersih saat menerima `SIGTERM`.
4. **Supervisi systemd**: Menjalankan gateway sebagai layanan `systemd` menjamin eksekusi otomatis saat booting dan pemulihan mandiri saat terjadi crash.
5. **Isolasi Keamanan**: Menjalankan daemon di bawah akun pengguna khusus (`iotgateway`) mencegah potensi eskalasi hak akses sistem.

## Referensi
- Kleinrock, L., *Queueing Systems, Volume 1: Theory*, John Wiley & Sons, 1975.
- POSIX.1-2017 / IEEE Std 1003.1-2017, *Standard for Information Technology—Portable Operating System Interface (POSIX)*.

1. Kerrisk, M. *The Linux Programming Interface: A Linux and UNIX System Programming Handbook*. No Starch Press.
2. Poettering, L. *systemd System and Service Manager Documentation*. https://systemd.io/
3. Raspberry Pi Foundation. *Raspberry Pi Documentation — Configuration and Interfaces (UART)*. https://www.raspberrypi.com/documentation/
