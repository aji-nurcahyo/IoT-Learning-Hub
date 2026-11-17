# Panduan Implementasi: Matter & Thread Fundamentals

Dokumen ini menjelaskan implementasi teknis pemodelan topologi jaringan nirkabel Thread dan protokol *commissioning* standar Matter.

## 1. Modul Simulasi Matter & Thread Python

Modul [matter_thread_sim.py](file:///d:/Workstation/Repo%20My%20Corses/Internet%20Of%20Things/public/content/chapter-34/src/matter_thread_sim.py) memverifikasi:
1. `ThreadMeshSimulator`: memodelkan keterhubungan node Thread (*Leader*, *Router*, *Border Router*, dan *End Device*) serta algoritma perutean multihop berbasis *Breadth-First Search* (BFS).
2. `MatterCommissioningSimulator`: memvalidasi proses verifikasi kode PIN penyiapan (*Setup PIN Code*) melalui mekanisme PASE serta penerbitan kredensial Fabric dan sertifikat operasional *Node Operational Certificate* (NOC).

Jalankan pengujian menggunakan:

```bash
python public/content/chapter-34/src/matter_thread_sim.py
```

### Hasil Verifikasi Eksekusi:
```text
=== CHAPTER 34: MATTER & THREAD SIMULATION ===
Thread Multihop Route (DoorLock -> LightSensor): DoorLock -> Router1 -> Leader -> BorderRouter -> LightSensor
Matter Commissioning Complete: Fabric=FABRIC_01, NodeId=NODE_42, Session=CASE_READY
STATUS: VERIFIED (Semua pengujian Thread Mesh routing dan Matter Commissioning lulus 100%)
```

## 2. Alur Transisi Keamanan Matter

- **Fase PASE (Password-Authenticated Session Establishment)**: Berlangsung saat perangkat pertama kali dinyalakan. Pengguna memasukkan kode PIN setup atau memindai kode QR. Pertukaran kunci kurva eliptik berbasis SPAKE2+ membentuk enkripsi awal tanpa memaparkan PIN melintasi transmisi radio.
- **Penerbitan NOC**: Komisioner (misal smartphone) memasukkan perangkat ke dalam *Fabric* rumah tangga dengan menerbitkan sertifikat digital unik *Node Operational Certificate*.
- **Fase CASE (Certificate-Authenticated Session Establishment)**: Digunakan untuk seluruh komunikasi harian berikutnya. Perangkat saling memverifikasi sertifikat digital secara timbal balik, sehingga perangkat tidak lagi memerlukan PIN setup dan dapat dikendalikan secara lokal bahkan saat koneksi internet global padam.
