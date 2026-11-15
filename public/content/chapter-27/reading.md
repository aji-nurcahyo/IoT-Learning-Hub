# Chapter 27 — Device Configuration, Inventory & Fleet Management

Ketika sebuah sistem IoT berkembang dari satu purwarupa di atas meja laboratorium menjadi armada ratusan atau ribuan perangkat yang tersebar di berbagai gedung dan kota, tantangan utama bergeser dari sekadar "bagaimana membaca sensor" menjadi "bagaimana mengelola armada secara terpusat dan andal". Mengubah frekuensi sampling atau ambang batas alarm satu per satu secara manual dengan mencolokkan kabel USB ke ribuan perangkat lapangan adalah hal yang mustahil dilakukan.

**Fleet Management** adalah tulang punggung operasional skala enterprise yang mencakup pendaftaran identitas fisik (*device enrollment*), pemeliharaan inventaris (*device registry*), sinkronisasi konfigurasi melalui pola **Digital Twin** (*Desired vs Reported State*), pemantauan detak kesehatan (*Heartbeat & Dead Node Detection*), serta pemensiunan aman (*decommissioning*).

![Arsitektur Manajemen Armada: Registri Inventaris, Sinkronisasi Digital Twin, dan Deteksi Node Mati](content/chapter-27/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan bab ini, Anda diharapkan mampu:

1. **Merancang Skema Registri Inventaris (Device Registry)**: Mengelola basis data identitas perangkat keras (Device ID, MAC Address, Model Hardware, Versi Firmware, dan Status Siklus Hidup).
2. **Menerapkan Pola Sinkronisasi Digital Twin**: Memisahkan secara tegas antara konfigurasi yang diinginkan oleh operator (*Desired State*) dengan kondisi aktual yang dilaporkan perangkat (*Reported State*), serta mendeteksi ketidaksesuaian (*configuration drift*).
3. **Mengelola Versi Konfigurasi & Rekonsiliasi**: Mengimplementasikan penomoran versi konfigurasi bertahap (*semantic versioning*), transmisi konfigurasi delta, dan konfirmasi penerapan (*ACK/NACK*).
4. **Membangun Sistem Deteksi Simpul Mati (Dead Node Detection)**: Menerapkan mekanisme penerimaan denyut jantung (*heartbeat ping*) dengan klasifikasi status otomatis (`ONLINE`, `DEGRADED`, `OFFLINE`).
5. **Menerapkan Alur Pemensiunan Aman (Decommissioning)**: Mencabut hak akses, menonaktifkan token otentikasi, dan memblokir paket transmisi dari perangkat yang telah dipensiunkan.

## Prasyarat

- Memahami arsitektur protokol MQTT dan data model JSON dari [Chapter 14](chapter-14) dan [Chapter 21](chapter-21).
- Memahami konsep basis data relasional/SQLite dari [Chapter 25](chapter-25).
- Memahami penanganan stempel waktu UTC presisi tinggi.

## Konsep dan teori

### 1. Struktur Basis Data Registri Inventaris

Setiap perangkat yang beroperasi dalam sistem IoT wajib memiliki rekaman unik dalam tabel registri terpusat. Registri ini menyimpan metadata statis dan dinamis:

- **Identitas Keras (*Hardware Identity*)**: Alamat MAC Wi-Fi/Ethernet, nomor seri chip silikon, tipe SoC (misal: ESP32-WROOM-32D atau ESP32-S3).
- **Identitas Logis (*Logical Identity*)**: `device_id` ramah sistem (misal: `node-env-01`), penanda lokasi/gedung, grup armada (*fleet tags*).
- **Metadata Keamanan**: Token otentikasi prapasang (*pre-shared token*), sidik jari sertifikat X.509, tanggal pendaftaran.
- **Status Operasional**: `PROVISIONED`, `ONLINE`, `DEGRADED`, `OFFLINE`, atau `DECOMMISSIONED`.

### 2. Pola Digital Twin (Desired vs Reported State)

Salah satu pola arsitektur paling penting dalam IoT modern (diadopsi oleh AWS IoT Device Shadow, Azure IoT Device Twin, dan Eclipse Ditto) adalah konsep **Digital Twin**:

$$\text{Drift} = (\text{Desired State} \ne \text{Reported State})$$

1. **Desired State**: Ditulis oleh operator atau aplikasi cloud (misal: mengubah interval sampling dari $10\text{s}$ menjadi $5\text{s}$, `version: 2`).
2. **Delta Detection**: Gateway mendeteksi perbedaan antara konfigurasi yang diinginkan dengan konfigurasi yang terakhir dilaporkan perangkat. Gateway memancarkan konfigurasi delta ke topik kendali perangkat:
   `iot/fleet/{dev_id}/config/desired`
3. **Reported State**: Mikrokontroler menerima delta, memperbarui memori non-volatil (NVS/Flash), mengonfirmasi keberhasilan penerapan, dan mengirimkan pesan konfirmasi (*Reported ACK*):
   `iot/fleet/{dev_id}/config/reported`
4. **Reconciliation Complete**: Begitu reported state sama dengan desired state, bendera *drift* hilang.

### 3. Pemantauan Denyut Jantung (Heartbeat Monitor)

Bagaimana server mengetahui sebuah perangkat sensor di lapangan mati jika sensor tersebut dirancang hanya mengirim data sesekali saat ada pergerakan?

Sistem menerapkan **Heartbeat Telemetry**:
- Perangkat memancarkan paket denyut kecil secara berkala (misal tiap $10\text{ detik}$):
  `{"dev": "node-01", "type": "heartbeat", "vbatt": 3300, "ts": 1762822800}`
- Server menjalankan daemon evaluator berbasis selisih waktu:
  $$\Delta t = t_{\text{current}} - t_{\text{last\_heartbeat}}$$

Klasifikasi status ketersediaan:
- Jika $\Delta t \le T_{\text{degraded}}$ ($15\text{s}$): Status **`ONLINE`** (konektivitas prima).
- Jika $T_{\text{degraded}} < \Delta t \le T_{\text{timeout}}$ ($30\text{s}$): Status **`DEGRADED`** (beberapa paket denyut hilang, sinyal melemah).
- Jika $\Delta t > T_{\text{timeout}}$ ($30\text{s}$): Status **`OFFLINE`** (simpul dianggap mati / baterai habis, memicu alarm pemeliharaan).

### 4. Siklus Hidup & Pemensiunan Aman (Decommissioning)

Ketika sebuah sensor rusak permanen, hilang dicuri, atau masa kontraknya berakhir:
1. Operator menandai status perangkat menjadi **`DECOMMISSIONED`**.
2. Server otorisasi mencabut token akses dan sertifikat perangkat dari daftar putih broker MQTT.
3. Seluruh transmisi telemetri maupun heartbeat yang masih dipancarkan oleh perangkat tersebut langsung ditolak di pintu gerbang (*access denied*).
4. Jika perangkat masih dapat dihubungi melalui jaringan, server mengirimkan perintah *crypto-erase* / *remote factory reset* untuk menghapus kunci enkripsi dan kredensial Wi-Fi dari memori flash NVS.

## Latihan

1. **Analisis Configuration Drift**:
   Jelaskan apa yang terjadi jika operator mengubah ambang batas suhu di cloud saat perangkat sedang berada dalam kondisi mati (*offline*). Bagaimana pola Digital Twin memastikan perangkat tersebut otomatis mendapatkan konfigurasi terbaru begitu ia menyala kembali dan terhubung ke jaringan?
2. **Kalkulasi Frekuensi Heartbeat**:
   Sebuah sistem pemantauan armada terdiri atas 10.000 sensor bertenaga baterai. Jika setiap sensor mengirimkan paket heartbeat berukuran 60 byte setiap 5 detik:
   - Hitung jumlah pesan heartbeat per detik yang harus diproses oleh broker.
   - Usulkan strategi penjadwalan heartbeat (seperti *adaptive heartbeat* atau *piggybacking* pada telemetri reguler) untuk memperpanjang usia baterai perangkat.
3. **Keamanan Decommissioning**:
   Mengapa sekadar mencabut baterai perangkat fisik di lapangan belum dianggap sebagai prosedur *decommissioning* yang aman pada sistem enterprise? Apa risiko yang terjadi jika identitas dan kredensial perangkat tersebut tidak dicabut dari registri cloud?

## Tugas

Bangun sistem manajemen armada dan rekonsiliasi konfigurasi digital twin menggunakan Python:

1. **Implementasi Kelas `DeviceRecord` & Registri**:
   Susun kelas penyimpanan identitas perangkat yang mencakup model hardware, MAC address, versi firmware, status siklus hidup, dan objek kembar *Desired/Reported state*.
2. **Mekanisme Deteksi Drift & Rekonsiliasi**:
   Bangun metode `set_desired_config` dan `report_device_config`. Buktikan bahwa sistem mampu mendeteksi keberadaan *configuration drift* dan menghilangkannya setelah perangkat mengirimkan ACK konfirmasi.
3. **Heartbeat Monitor & Deteksi Node Mati**:
   Implementasikan fungsi `evaluate_fleet_health` dengan batas ambang *Degraded* ($15\text{ detik}$) dan batas ambang *Offline* ($30\text{ detik}$).
4. **Alur Pemensiunan (Decommissioning)**:
   Terapkan fungsi `decommission_device` dan buktikan bahwa seluruh paket denyut jantung yang dikirimkan oleh perangkat berstatus pensiun ditolak secara mutlak oleh sistem.

### Rubrik Penilaian

| Kriteria | Bobot | Deskripsi Capaian |
| :--- | :---: | :--- |
| **Registri Inventaris & Identitas Perangkat** | 30% | Struktur data registri mencakup seluruh atribut perangkat keras dan status siklus hidup; proses enrollment berjalan valid. |
| **Rekonsiliasi Digital Twin & Versioning** | 35% | Logika Desired vs Reported state twin bekerja akurat; deteksi drift dan penomoran versi konfigurasi terbukti deterministik. |
| **Deteksi Node Mati & Decommissioning Aman** | 35% | Klasifikasi status ketersediaan (Online/Degraded/Offline) berbasis waktu tepat; alur penolakan perangkat pensiun berhasil diverifikasi. |

## Ringkasan

1. **Skalabilitas Sentral**: Registri inventaris terpusat memungkinkan pemantauan dan pengelolaan ribuan perangkat tanpa kontak fisik langsung.
2. **Ketahanan Digital Twin**: Pola Desired vs Reported state menjamin sinkronisasi konfigurasi yang konsisten meskipun konektivitas perangkat sering terputus-putus.
3. **Visibilitas Ketersediaan**: Sistem heartbeat mendeteksi simpul mati dan degradasi tautan radio secara otomatis sebelum pengguna akhir mengeluhkan ketiadaan data.
4. **Sanitasi Siklus Hidup**: Alur decommissioning yang ketat mencegah eksploitasi perangkat usang atau terbengkalai di lingkungan produksi.

## Referensi

1. Amazon Web Services. *AWS IoT Core Developer Guide: Device Shadow Service Architecture*. https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html
2. Microsoft Learn. *Azure IoT Hub: Understand and use device twins in IoT Hub*. https://learn.microsoft.com/azure/iot-hub/iot-hub-devguide-device-twins
3. Eclipse Foundation. *Eclipse Ditto: Digital Twin Framework for IoT Systems*. https://www.eclipse.org/ditto/
