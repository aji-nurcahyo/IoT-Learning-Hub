# Chapter 32: RTOS, Concurrency & Scheduling

## Tujuan pembelajaran

Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memahami arsitektur *Real-Time Operating System* (FreeRTOS) dan perbedaannya dengan model superloop tradisional (`void loop()`).
2. Menganalisis algoritma penjadwalan *Fixed-Priority Preemptive Scheduling* dan *Round-Robin time slicing*.
3. Mengimplementasikan komunikasi antar-task yang aman menggunakan FreeRTOS *Queues*, *Semaphores*, dan *Mutex*.
4. Mengidentifikasi serta memitigasi bahaya konkurensi umum seperti *race conditions*, *deadlock*, dan *priority inversion* menggunakan mekanisme *Priority Inheritance*.
5. Mengonfigurasi *Hardware & Task Watchdog Timers* (WDT) untuk menjamin determinisme sistem dan pemenuhan *real-time deadlines*.

## Prasyarat

- Pemahaman arsitektur mikrokontroler dan memori (Chapter 04–05).
- Penguasaan bahasa C/C++ (pointer, struktur data `struct`, dan alokasi memori heap/stack).
- Konsep dasar konkurensi (interupsi ISR dan flag volatile).

## Konsep dan teori

### 1. Paradigma Superloop vs Real-Time Operating System

Pada pendekatan tradisional (*bare-metal* superloop), mikrokontroler mengeksekusi serangkaian fungsi secara berurutan dalam loop tak berujung:

```c
void loop() {
  readSensor();     // Jika fungsi ini memblokir 100 ms...
  processData();    
  sendNetwork();    // ...atau koneksi jaringan macet selama 2 detik...
  updateDisplay();  // ...maka display dan respon tombol akan terhenti total!
}
```

Kelemahan fatal superloop adalah ketiadaan isolasi waktu (*temporal isolation*). Jika satu tugas mengalami kelambatan I/O, seluruh tugas lain ikut tertunda.

Sebaliknya, **FreeRTOS** mengabstraksikan CPU menjadi beberapa *Task* independen yang berjalan seolah-olah secara simultan (konkuren). FreeRTOS Kernel menggunakan *SysTick timer* (biasanya berdetak setiap 1 ms pada 1000 Hz) untuk mengevaluasi status task dan melakukan *context switching*.

```
   SysTick Interrupt (1 ms)
         |
         v
+-------------------------------------------------------------+
|                     FreeRTOS Kernel                         |
|   +-----------------------------------------------------+   |
|   |         Preemptive Priority Scheduler               |   |
|   +-----------------------------------------------------+   |
+-------------------------------------------------------------+
       |                         |                       |
       v                         v                       v
+---------------+         +---------------+       +---------------+
| Task High     |         | Task Medium   |       | Task Low      |
| Priority = 3  |         | Priority = 2  |       | Priority = 1  |
| (Watchdog/Net)|         | (Sensor Read) |       | (Display/Log) |
+---------------+         +---------------+       +---------------+
```

### 2. Preemptive Fixed-Priority Scheduling

Algoritma penjadwalan FreeRTOS bekerja dengan aturan ketat:
1. Task yang berada pada status *Ready* dengan nilai prioritas numerik tertinggi akan selalu mendapatkan alokasi waktu CPU.
2. Jika sebuah task dengan prioritas lebih tinggi beralih dari status *Blocked* ke *Ready* (misalnya karena timer habis atau menerima data queue), task prioritas rendah yang sedang berjalan akan langsung dihentikan di tengah jalan (**Preemption**).
3. Jika terdapat beberapa task dengan prioritas yang sama, kernel membagi waktu secara merata melalui *Round-Robin time slicing*.

### 3. Komunikasi Antar-Task: FreeRTOS Queues

Berbagi variabel global antar-task tanpa proteksi menyebabkan *race condition*. FreeRTOS menyediakan primitif **Queue**:
- Beroperasi secara FIFO (*First-In, First-Out*).
- Sepenuhnya *thread-safe* (terlindungi oleh interupsi internal kernel).
- Memungkinkan task penerima masuk ke status *Blocked* tanpa membuang siklus CPU (0% CPU usage saat menunggu data tiba).

### 4. Bahaya Konkurensi & Priority Inversion

Ketika dua task berbagi sumber daya bersama (misalnya port UART Serial atau bus I2C), **Mutex** digunakan untuk menjamin *mutual exclusion*.

Namun, penggunaan Mutex tanpa disiplin dapat memicu **Priority Inversion**:
1. Task Rendah ($T_L$) mengambil Mutex sumber daya.
2. Task Tinggi ($T_H$) tiba dan membutuhkan sumber daya yang sama, sehingga $T_H$ terblokir menunggu $T_L$.
3. Tiba Task Sedang ($T_M$) yang tidak membutuhkan Mutex tersebut. Karena prioritas $T_M > T_L$, kernel menjalankan $T_M$ dan menunda $T_L$.
4. Akibatnya, Task Tinggi ($T_H$) tidak langsung dieksekusi meskipun prioritasnya tertinggi, karena tersandera oleh Task Sedang ($T_M$).

FreeRTOS menyelesaikan masalah ini melalui **Priority Inheritance**: saat $T_H$ terblokir menunggu Mutex yang dipegang oleh $T_L$, prioritas $T_L$ dinaikkan sementara menyamai $T_H$, sehingga $T_L$ tidak dapat direbut oleh $T_M$ dan dapat segera melepaskan Mutex.

## Latihan

1. **Analisis Timeline Eksekusi**: Diberikan tiga task: Task A (Pri 1, burst 4 tick), Task B (Pri 2, burst 2 tick, tiba tick 2), dan Task C (Pri 3, burst 1 tick, tiba tick 3). Gambarkan diagram Gantt eksekusi sistem dari tick 0 hingga tick 8.
2. **Kapasitas Queue & Overflow**: Apa yang terjadi jika sebuah task sensor berkecepatan tinggi mengirim data ke queue berkapasitas 5 elemen dengan timeout 0 tick, sementara task konsumen sibuk memproses inferensi AI? Bagaimana strategi mitigasi data dropping yang tepat?
3. **Konfigurasi Stack Task**: Mengapa penetapan ukuran stack yang terlalu kecil pada `xTaskCreate` menyebabkan *Stack Overflow Exception*, dan bagaimana fungsi `uxTaskGetStackHighWaterMark()` digunakan untuk memantau sisa memori stack?

## Tugas

Kembangkan modul simulasi penjadwal preemptive Python (`rtos_scheduler_sim.py`) yang memverifikasi urutan eksekusi task bertingkat prioritas dan perilaku batas kapasitas queue. Tuliskan pula sketsa C++ ESP32 FreeRTOS (`esp32_freertos_tasks.ino`) yang mendistribusikan pembacaan sensor dan transmisi data telemetri ke dalam dua task terpisah yang disinkronkan oleh Queue dan Mutex.

## Ringkasan

1. FreeRTOS menggantikan arsitektur superloop kaku dengan penjadwalan preemptive berbasis prioritas yang menjamin pemenuhan tenggat waktu *real-time*.
2. Primitif sinkronisasi seperti Queue, Semaphore, dan Mutex wajib digunakan untuk mencegah korupsi memori (*race conditions*).
3. Fenomena *Priority Inversion* dapat mematikan sistem tertanam kritis jika tidak dimitigasi oleh mekanisme *Priority Inheritance*.

## Referensi

1. Real Time Engineers Ltd. *Mastering the FreeRTOS Real Time Kernel - A Hands-On Tutorial Guide*. 2023.
2. Espressif Systems. *ESP-IDF FreeRTOS (SMP) Architecture & API Reference*. Espressif Inc., 2024.
3. Buttazzo, G. C. *Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications*. Springer, 2022.
