# Latihan Chapter 32: RTOS, Concurrency & Scheduling

## Latihan Konseptual

1. **Analisis Algoritma Preemptive**:
   Jelaskan bagaimana kernel FreeRTOS menangani kondisi di mana sebuah Task berprioritas 3 beralih dari status *Blocked* ke *Ready* tepat saat Task berprioritas 1 sedang menjalankan instruksi di dalam CPU. Sebutkan tahapan penyimpanan dan pemulihan konteks register prosesor (*Context Switch*).

2. **Diferensiasi Mutex vs Binary Semaphore**:
   Meskipun keduanya tampak serupa sebagai token bernilai 0 atau 1, jelaskan mengapa *Binary Semaphore* tidak boleh digunakan untuk memproteksi sumber daya bersama (*shared resource*), serta jelaskan bagaimana mekanisme *Priority Inheritance* pada Mutex mencegah terjadinya *Priority Inversion*.

3. **Perhitungan Stack High Water Mark**:
   Jika sebuah task dialokasikan stack sebesar 2048 Word (8192 byte) dan pemanggilan `uxTaskGetStackHighWaterMark()` menghasilkan nilai 450 Word, berapa byte memori stack terkecil yang pernah tersisa selama task berjalan? Apakah alokasi ini tergolong aman atau perlu dioptimasi?

## Latihan Praktik & Perhitungan

1. **Simulasi Diagram Gantt Eksekusi RTOS**:
   Diberikan sistem dengan 3 Task independen:
   - **Task Jaringan (NetTx)**: Prioritas = 1, Tiba = Tick 0, Burst Time = 4 Tick.
   - **Task Sensor (SensRead)**: Prioritas = 2, Tiba = Tick 2, Burst Time = 2 Tick.
   - **Task Pengawas (Watchdog)**: Prioritas = 3, Tiba = Tick 3, Burst Time = 1 Tick.
   
   *Instruksi*:
   - Tuliskan urutan eksekusi CPU tick demi tick dari Tick 0 hingga Tick 7.
   - Hitung nilai *Turnaround Time* dan *Waiting Time* untuk masing-masing task.
   - Verifikasi apakah Task Watchdog mengalami penundaan eksekusi saat tiba pada Tick 3.

2. **Perancangan Multi-Producer Single-Consumer Queue**:
   Rancang struktur data C++ dan potongan kode FreeRTOS di mana dua task pembacaan sensor yang berbeda (Sensor Suhu dan Sensor Tekanan) mengirim paket data terpadu ke satu `QueueHandle_t` yang sama, lengkap dengan penanda *sensor_id* dan nilai pembacaan analog.
