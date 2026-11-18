# Chapter 24 — Node-RED & Event-Driven Integration

Dalam lingkungan industri dan laboratorium riset modern, integrasi data IoT tidak selalu harus dibangun dengan menulis baris kode server backend dari nol. Kecepatan integrasi protokol, pembuatan prototipe antarmuka, dan perutean pesan antar layanan sangat terbantu oleh platform integrasi visual berbasis event (*low-code event-driven integration*). **Node-RED**, yang dikembangkan di atas lingkungan runtime Node.js, merupakan perangkat integrasi IoT sumber terbuka yang paling luas diadopsi di seluruh dunia.

Bab ini mengupas tuntas arsitektur berbasis event (*event-driven architecture*), manipulasi objek pesan `msg`, cakupan memori *Context Storage* (`flow` vs `global`), percabangan logika (*Switch Node*), pengayaan data kustom (*Function Node*), penyediaan endpoint API REST mikro (*HTTP In/Response*), mitigasi galat dengan *Catch Node*, serta manajemen aliran deklaratif portabel menggunakan file JSON.

![Arsitektur Aliran Node-RED: Ingestion MQTT, Context Store, REST API, dan Error Handling](content/chapter-24/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan bab ini, Anda diharapkan mampu:

1. **Memahami Arsitektur Event-Driven Node-RED**: Menjelaskan siklus hidup pesan di dalam *Node.js single-threaded event loop* dan bagaimana Node-RED mengalirkan objek `msg` melalui simpul-simpul kabel (*wires*).
2. **Mengelola Konteks Penyimpanan Data (Context Storage)**: Memanfaatkan cakupan memori `context` (lokal simpul), `flow` (berbagi dalam satu lembar kerja), dan `global` (dapat diakses seluruh sistem) untuk menyimpan status perangkat (*digital twin state*).
3. **Membangun Pipeline Logika Percabangan**: Menerapkan simpul `switch` dan `change` untuk mengevaluasi ambang batas numerik dan menyaring telemetri tanpa menulis kode script kompleks.
4. **Menyediakan Layanan REST API Mikro**: Menggabungkan simpul `http in` dan `http response` untuk melayani permintaan data telemetri terkini melalui antarmuka HTTP berbasis JSON.
5. **Menerapkan Penanganan Kesalahan Terpusat**: Mengonfigurasi simpul `catch` untuk mengisolasi kegagalan runtime (*uncaught exceptions*) dan mengalirkan pesan galat ke antrean surat mati (*Dead-Letter Queue*).

## Prasyarat

- Memahami arsitektur protokol MQTT (Publish/Subscribe, Topic, QoS) dari [Chapter 14](chapter-14).
- Memahami konsep data model telemetri dan format JSON dari [Chapter 21](chapter-21).
- Memahami dasar penanganan data JavaScript/JSON sederhana.

## Konsep dan teori

### 1. Model Komputasi Berbasis Aliran (*Flow-Based Programming*)

Node-RED menerapkan paradigma *Flow-Based Programming* (FBP), di mana aplikasi didefinisikan sebagai jaringan simpul (*black box nodes*) yang saling bertukar data melalui koneksi kawat yang telah ditentukan sebelumnya.

- **Pesan Inti (`msg`)**: Struktur data standar yang mengalir antar simpul. Objek `msg` wajib membawa properti `msg.payload`, dan lazimnya memuat metadata seperti `msg.topic`, `msg.qos`, atau `msg._msgid`.
- **Eksekusi Asinkron Non-blocking**: Seluruh simpul berjalan di atas *event loop* Node.js, memungkinkan penanganan ribuan event pesan I/O simultan dengan footprint memori RAM yang sangat hemat ($< 150\text{ MB}$).

### 2. Hierarki Context Storage (State Persistence)

Kelemahan umum pemrosesan pesan *stateless* adalah ketidakmampuan mengingat kondisi sebelumnya. Node-RED mengatasi hal ini melalui variabel konteks:

| Tingkat Konteks | Cakupan (*Scope*) | Contoh Penggunaan |
| :--- | :--- | :--- |
| **`context` (Node)** | Hanya dapat diakses oleh satu simpul fungsi tertentu | Menghitung akumulator jumlah pesan internal simpul |
| **`flow` (Tab)** | Dapat diakses oleh seluruh simpul dalam satu tab kerja | Menyimpan status sakelar atau timer dalam satu modul sistem |
| **`global` (Instance)** | Dapat diakses oleh seluruh simpul di seluruh flow/tab | Menyimpan tabel status terkini (*digital twin*) seluruh node |

Secara default, konteks disimpan di memori RAM volatil. Konfigurasi `settings.js` dapat diatur untuk mengaktifkan penyimpanan persisten berbasis sistem berkas lokal (*file-based local storage*) sehingga status tidak hilang saat gateway me-reboot.

### 3. Logika Percabangan & Pengayaan Pesan

- **Simpul Switch**: Mengevaluasi aturan perbandingan (`==`, `!=`, `<`, `>`, `between`, `regex`) pada properti `msg.payload.metrics.temp_c`. Simpul ini memiliki banyak keluaran (*multi-port outputs*), mengarahkan pesan ke jalur alarm jika suhu kritis atau ke jalur normal log.
- **Simpul Function**: Memungkinkan penulisan logika JavaScript penuh untuk memodifikasi atau memperkaya objek pesan:
  ```javascript
  const temp = msg.payload.metrics.temp_c;
  if (temp >= 30.0) {
      msg.payload = {
          event_id: "ALM-" + Date.now(),
          type: "HIGH_TEMPERATURE",
          measured_temp: temp,
          severity: "warning"
      };
      return msg;
  }
  return null; // Mematikan aliran jika tidak memenuhi kriteria
  ```

### 4. Integrasi Dua Arah: MQTT ke REST API

Kekuatan utama Node-RED adalah kemampuannya menjembatani protokol yang berbeda secara instan:
1. Simpul **`mqtt in`** menerima aliran data sensor berkala dari broker lokal, lalu simpul `change` menyimpan payload terbaru ke `global.set('latest_telemetry', msg.payload)`.
2. Simpul **`http in`** membuka endpoint REST `GET /api/v1/telemetry/latest`. Saat ada klien browser/dashboard eksternal yang memanggil URL tersebut, simpul fungsi membaca `global.get('latest_telemetry')` dan mengembalikannya melalui simpul **`http response`** dengan status kode `200 OK`.

### 5. Penanganan Galat & Antrean Surat Mati (*Dead-Letter*)

Jika sebuah payload yang diterima mengalami korupsi atau tidak memiliki field yang dibutuhkan oleh simpul fungsi (misal: `msg.payload.metrics` bernilai `undefined`), runtime JavaScript akan melempar pengecualian `TypeError`.

Simpul **`catch`** bertindak sebagai blok `try-catch` global yang menangkap seluruh pengecualian yang tidak tertangani di dalam canvas:
- Simpul `catch` menambahkan objek `msg.error` yang memuat deskripsi kesalahan, baris kode penyebab, dan identitas simpul yang gagal.
- Aliran keluaran simpul `catch` diarahkan ke antrean surat mati (*Dead-Letter Queue*) atau file log audit sehingga aliran data utama tidak terhenti (*fail-safe isolation*).

### 3.1 Landasan Matematis: Throughput Aliran Peristiwa & Latensi Pipeline Node-RED (Mathematical Foundations)

Pemrosesan berbasis aliran (*Flow-Based Programming*) pada Node-RED memproses pesan sebagai aliran peristiwa diskrit di atas event-loop single-threaded Node.js:

1. **Model Penjadwalan Event Loop & Waktu Eksekusi Fungsi**:
   Total latensi transit suatu pesan $T_{\text{pipeline}}$ yang melewati rantai $K$ node fungsi dihitung sebagai:
   $$
   T_{\text{pipeline}} = \sum_{i=1}^{K} t_{\text{exec},i} + \sum_{i=1}^{K-1} t_{\text{queue},i}
   $$
   di mana $t_{\text{exec},i}$ adalah waktu eksekusi komputasi node ke-$i$ dan $t_{\text{queue},i}$ adalah waktu tunggu di antrean mikro-task V8.

2. **Kapasitas Throughput Maksimum Pipeline (Worked Example)**:
   Sebuah flow Node-RED menerima pesan MQTT, memvalidasi skema JSON ($t_{\text{exec},1} = 0{,}8\text{ ms}$), mengevaluasi ambang batas alarm ($t_{\text{exec},2} = 0{,}2\text{ ms}$), dan memformat data untuk database ($t_{\text{exec},3} = 0{,}5\text{ ms}$). Total waktu eksekusi sinkron per pesan adalah:
   $$
   T_{\text{sync}} = 0{,}8 + 0{,}2 + 0{,}5 = 1{,}5\text{ ms}
   $$
   Throughput komputasi teoritis maksimum pipeline pada satu inti CPU adalah:
   $$
   \text{Throughput}_{\text{max}} = \frac{1}{T_{\text{sync}}} = \frac{1}{1{,}5 \times 10^{-3}\text{ s}} \approx 666{,}7\text{ pesan/detik}
   $$
   Jika beban kedatangan telemetri melampaui 667 pesan/detik, latensi antrean $t_{\text{queue}}$ akan meningkat tanpa batas (*starvation*), sehingga diperlukan partisi beban dengan kluster Node-RED atau pendelegasian pemrosesan berat ke worker thread.

## Latihan

1. **Analisis Konteks Simpul**:
   Jelaskan apa yang terjadi jika Anda menyimpan nilai pembacaan suhu terakhir pada konteks lokal `context.set('temp', t)` pada sebuah simpul Function, lalu mencoba membacanya dari simpul Function lain di tab yang sama menggunakan `context.get('temp')`. Bagaimana cara memperbaikinya?
2. **Perancangan Simpul Switch**:
   Rancang aturan konfigurasi pada simpul Switch yang memiliki 3 port keluaran untuk memilah tingkat voltase baterai node (`msg.payload.metrics.battery_mv`):
   - Port 1: `battery_mv >= 3600` (Status Normal)
   - Port 2: `3000 <= battery_mv < 3600` (Peringatan Baterai Lemah)
   - Port 3: `battery_mv < 3000` (Kritis / Butuh Penggantian Segera)
3. **Pencegahan Kebocoran Memori**:
   Jika sebuah simpul Function di Node-RED membuat objek array global dan terus menambahkan data setiap detik tanpa pernah membatasi panjangnya (`global.get('history').push(msg)`), jelaskan dampak sistemik terhadap performa Raspberry Pi setelah 1 minggu beroperasi.

## Tugas

Rancang dan validasi alur integrasi visual Node-RED menggunakan format deklaratif [`flows.json`](content/chapter-24/src/flows.json):

1. **Penyusunan Alur Deklaratif**:
   - Susun simpul `mqtt in` yang mendengarkan topik telemetri `iot/lab/+/telemetry`.
   - Hubungkan ke simpul `switch` yang mengevaluasi apakah suhu `>= 30.0 C`.
   - Bangun simpul `function` yang menyusun payload alarm baru dan menerbitkannya kembali ke topik `iot/lab/{dev}/event/alarm`.
2. **Penyediaan Endpoint HTTP REST**:
   - Hubungkan simpul `http in` pada path `/api/v1/telemetry/latest`.
   - Buat fungsi pembaca konteks global yang mengembalikan data telemetri terakhir dalam format JSON.
3. **Isolasi Galat (*Catch Error*)**:
   - Pasang simpul `catch` yang menangkap pesan malformed dan meneruskannya ke simpul log surat mati.
4. **Verifikasi Simulasi Otomatis**:
   - Uji alur menggunakan skrip eksekusi [`nodered_flow_runner.py`](content/chapter-24/src/nodered_flow_runner.py) dan buktikan bahwa seluruh kasus uji (normal, kritis, HTTP API, dan error catch) lolos evaluasi.

### Rubrik Penilaian

| Kriteria | Bobot | Deskripsi Capaian |
| :--- | :---: | :--- |
| **Arsitektur Flow & Percabangan Logika** | 35% | Struktur flow deklaratif tersusun rapi; simpul switch dan enricher berfungsi menyaring dan memformat alarm dengan tepat. |
| **Konteks Global & Integrasi REST API** | 35% | Konteks global diperbarui secara konsisten; endpoint HTTP berhasil melayani permintaan data status terakhir tanpa galat. |
| **Mitigasi Galat & Ketahanan Aliran** | 30% | Simpul catch menangani pesan anomali secara terisolasi tanpa merusak alur pesan utama; hasil uji otomatis tercatat lengkap. |

## Ringkasan

1. **Paradigma Berbasis Aliran**: Node-RED menyederhanakan perakitan sistem IoT kompleks melalui abstraksi visual dan manipulasi objek pesan `msg`.
2. **Cakupan State**: Penggunaan konteks `flow` dan `global` memungkinkan sistem mempertahankan memori status perangkat di atas arsitektur perutean yang fleksibel.
3. **Jembatan Protokol Instan**: Node-RED memfasilitasi konversi data dari MQTT ke REST API dan sebaliknya hanya dengan menghubungkan simpul standar.
4. **Resiliensi Terisolasi**: Pemasangan simpul `catch` menjamin stabilitas runtime terhadap payload korup tanpa memerlukan proses restart manual.

## Referensi
- Morrison, J. P., *Flow-Based Programming: A New Approach to Application Development*, 2nd Edition, CreateSpace, 2010.
- OpenJS Foundation, *Node-RED Programming Guide & Node Architecture*, Official Documentation.

1. OpenJS Foundation. *Node-RED Official Documentation & Core Concepts*. https://nodered.org/docs/
2. Morrison, J. P. *Flow-Based Programming: A New Approach to Application Development*. Van Nostrand Reinhold.
3. Cantelon, M., et al. *Node.js in Action*. Manning Publications.
