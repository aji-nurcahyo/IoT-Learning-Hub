# Siapkan lingkungan belajar

Panduan ini terpisah dari 40 chapter. Pilih bagian sesuai kebutuhan; tidak semua tool harus dipasang sekaligus. Perintah di bawah adalah petunjuk persiapan, **belum diuji pada hardware** dalam proyek ini. Jangan menafsirkan contoh sebagai bukti eksperimen.

## Pilih jalur: simulator atau hardware

| Jalur | Yang dapat dipelajari | Batasan |
| --- | --- | --- |
| Simulator | Logika Firmware, alur GPIO, protokol yang didukung simulator | Tidak membuktikan arus, kualitas radio, akurasi Sensor, atau kompatibilitas board fisik |
| Hardware yang tersedia | Wiring dan perilaku perangkat nyata | Memerlukan pemeriksaan datasheet, alat ukur, dan pencatatan kondisi uji |
| Software lokal | Payload JSON, Broker, Gateway, flow Node-RED | Belum memvalidasi timing dan keterbatasan Microcontroller |

Tidak perlu membeli hardware atau memakai cloud berbayar untuk mulai. Simulator merupakan pilihan, bukan persyaratan. Periksa dukungan board dan peripheral sebelum memilih simulator; jangan menganggap semua varian ESP32 didukung.

## Development board dan varian ESP32

1. Baca tulisan pada chip/module dan nama produk board; ambil foto untuk catatan pribadi.
2. Cari schematic dan pinout **model serta revisi yang sama** di situs produsen.
3. Cocokkan target chip dengan dokumentasi Espressif. ESP32, ESP32-S3, ESP32-C3, dan varian lain bukan satu pinout yang dapat saling dipertukarkan.
4. Catat USB interface, jenis konektor, fitur radio, memori, pin khusus boot, dan pin yang tidak boleh dipakai pada konfigurasi tersebut.

Jangan menetapkan pin LED, tegangan input, atau kapasitas arus dari nama “ESP32” saja. Pilih SoC target pada [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/index.html), kemudian buka dokumen hardware yang tepat. Fondasi ini belum menetapkan BOM atau wiring praktik sehingga belum ada angka electrical rating yang diklaim berlaku umum.

## Editor dan toolchain

- **Arduino IDE**: jalur awal dengan editor, board manager, build, upload, dan Serial Monitor. Gunakan [panduan IDE resmi](https://docs.arduino.cc/software/ide/) untuk OS yang digunakan. Pilih board package dan target yang cocok; catat versi package dan library.
- **VS Code + PlatformIO**: alternatif untuk konfigurasi proyek yang disimpan dalam file. Cocokkan board identifier dan platform version dari [dokumentasi PlatformIO](https://docs.platformio.org/en/latest/platforms/espressif32.html).
- **Arduino CLI**: alternatif tanpa IDE. Catat FQBN dari daftar board yang terpasang, bukan menebak identifier.
- **ESP-IDF**: jalur lanjutan untuk konfigurasi SDK, RTOS, dan kontrol Firmware. Ikuti [Get Started resmi](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/) sesuai OS dan target. Pin versi SDK sebelum praktik agar dapat direproduksi.

Pilih satu jalur dulu. Contoh urutan CLI berikut perlu disesuaikan dengan instalasi; bukan log hasil uji:

```sh
arduino-cli version
arduino-cli board list
arduino-cli core list
```

## USB, flashing, dan Serial Monitor

1. Gunakan kabel USB yang mendukung data. Periksa port sebelum dan sesudah board dihubungkan.
2. Bila dibutuhkan, pasang USB driver dari vendor chip USB-to-serial yang teridentifikasi pada board; jangan memakai installer acak.
3. Pilih port serial dan board target yang benar. Tutup program lain yang memakai port tersebut.
4. Jalankan build terlebih dahulu. Build berhasil hanya mendukung label **Compile-verified** apabila log dan lingkungan disimpan.
5. Ikuti prosedur boot/download board sebelum upload. Buka Serial Monitor pada baud rate yang sama dengan Firmware.
6. Simpan command, versi tool, log asli, waktu, revisi board, dan kondisi pengujian. Upload tanpa pengamatan perilaku bukan bukti praktik sepenuhnya berhasil.

## Peralatan dan keselamatan low-voltage DC

Praktik awal dibatasi pada low-voltage DC. Siapkan breadboard, jumper, resistor yang sesuai rangkaian, multimeter, dan power supply dengan batas arus jika menggunakan hardware. Tidak semua alat perlu dibeli untuk jalur software/simulator.

- Putuskan daya sebelum mengubah wiring. Periksa polaritas dan kemungkinan short circuit.
- Baca datasheet setiap komponen, schematic board, batas voltage/current, serta kebutuhan driver dan protection sebelum menghubungkan rangkaian.
- Jangan menghubungkan motor atau beban berarus besar langsung ke GPIO. Kebutuhan driver, flyback protection, dan sumber daya harus ditentukan dari komponen spesifik.
- Ukur tegangan secara paralel. Pengukuran arus memerlukan rangkaian seri dan terminal/range alat yang benar; jangan memasang multimeter mode arus melintang pada supply.
- Jangan mengerjakan listrik PLN, mains switching, atau rangkaian tegangan tinggi dalam praktik awal ini.

## Python Development Environment untuk Gateway

Python digunakan sebagai tool Gateway atau pengolah telemetry bila relevan. Ia bukan persyaratan seluruh chapter. Gunakan interpreter dari [python.org](https://www.python.org/downloads/) atau package OS yang didukung. Catat versi OS dan interpreter.

```sh
python --version
python -m venv .venv
```

Di Windows, gunakan interpreter environment secara langsung tanpa harus mengubah execution policy:

```powershell
.\.venv\Scripts\python.exe -m pip --version
```

Di Linux/macOS:

```sh
.venv/bin/python -m pip --version
```

## Virtual Environment dan package management

Pasang dependency hanya ketika diperlukan praktik. Jalankan pip melalui interpreter environment, catat versi dependency dalam requirements, dan jangan commit `.venv`. [Dokumentasi venv](https://docs.python.org/3/library/venv.html) menjelaskan isolasi environment. Contoh untuk proyek yang sudah menyediakan requirements:

```sh
.venv/bin/python -m pip install -r requirements.txt
```

Pada Windows, ganti interpreter dengan `.\.venv\Scripts\python.exe`. Perintah tersebut memerlukan file requirements nyata; fondasi ini belum membagikan aplikasi Gateway.

## MQTT Broker lokal dan MQTT client

Gunakan [Eclipse Mosquitto](https://mosquitto.org/documentation/) atau Broker lokal yang sesuai. Untuk latihan satu komputer, jalankan hanya pada loopback. Jangan membuka listener anonymous ke jaringan publik.

Contoh isi `mosquitto-local.conf` untuk eksperimen lokal saja:

```conf
listener 1883 127.0.0.1
allow_anonymous true
```

Jalankan Broker dan dua terminal client setelah Mosquitto terpasang:

```sh
mosquitto -c mosquitto-local.conf -v
mosquitto_sub -h 127.0.0.1 -t lab/demo -v
mosquitto_pub -h 127.0.0.1 -t lab/demo -m '{"source":"synthetic"}'
```

Perintah contoh belum dijalankan di lingkungan ini; hasil yang diharapkan adalah subscriber menerima payload, bukan pengukuran latency. Quoting shell dapat berbeda; gunakan payload file bila shell mengubah JSON. Perangkat fisik tidak bisa mencapai loopback komputer: koneksi antarperangkat memerlukan listener, firewall, autentikasi, dan TLS yang dikonfigurasi sesuai jaringan. Pelajari [spesifikasi MQTT](https://mqtt.org/mqtt-specification/) untuk jaminan protokol.

## Node-RED

Ikuti [panduan lokal Node-RED](https://nodered.org/docs/getting-started/local) dan gunakan versi Node.js yang didukung. Instalasi native tersedia; Docker tidak wajib. Setelah berjalan, mulai dari flow Inject → Debug sebelum menghubungkan MQTT. Editor memiliki akses mengubah flow: batasi akses jaringan dan atur autentikasi sebelum penggunaan bersama.

## Docker opsional

Docker dapat membantu mengisolasi Broker atau penyimpanan telemetry. Pengguna yang sudah memiliki instalasi native tidak perlu berpindah. Catat image tag, volume, port binding, serta cara menghentikan service. Jangan memakai tag berubah-ubah untuk laporan yang harus dapat direproduksi. Fondasi ini belum menyediakan Docker stack teruji.

## Jaringan dan kredensial

Catat alamat Broker, subnet, firewall, SSID yang relevan, dan bagaimana perangkat memperoleh waktu. Periksa dokumentasi varian board untuk dukungan radio. Simpan secret di konfigurasi lokal yang diabaikan Git; jangan menulis password asli di Firmware contoh, screenshot, slide, atau log. Redaksi informasi sensitif sebelum membagikan bukti uji. TLS memerlukan trust dan validasi sertifikat yang benar, bukan sekadar mengganti nomor port.

## Troubleshooting

| Gejala | Pemeriksaan awal | Bukti yang dicatat |
| --- | --- | --- |
| Port tidak muncul | Kabel data, USB driver vendor, izin OS | Identitas board dan daftar port |
| Flash gagal | Target chip, port dipakai aplikasi lain, boot mode | Command dan log error lengkap |
| Serial tidak terbaca | Baud rate dan port yang cocok | Konfigurasi Firmware dan monitor |
| Build gagal | Versi board package, library, target | Log compile dan manifest dependency |
| MQTT tidak terhubung | Broker berjalan, listener, host, firewall, autentikasi | Log client dan Broker tanpa secret |
| Nilai Sensor aneh | Wiring, supply, unit, kalibrasi, datasheet | Kondisi dan pembacaan asli |

Jangan mengganti kegagalan dengan angka hasil rekaan. Catat **Belum diuji**, **Compile-verified**, **Simulator-verified**, atau **Hardware-verified** sesuai bukti. Ketika hardware tidak tersedia, lanjutkan review, build, dan pengujian software yang dapat dilakukan dengan batasan eksplisit.
