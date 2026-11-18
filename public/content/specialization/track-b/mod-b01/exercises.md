# Latihan Terstruktur: Modul B01

### Soal 1: Pemetaan Aset ke Model Purdue (C2)
Sebuah fasilitas pengolahan air bersih memiliki aset berikut:
1. Pompa distribusi utama $75\text{ kW}$.
2. Sensor tekanan air piezoresistif 4–20 mA.
3. Modul RTU pengendali katup Modbus RTU.
4. Server SCADA penampil animasi aliran fluida.
5. Server basis data Enterprise pengelola tagihan pelanggan.

Petakan kelima aset tersebut ke dalam tingkatan Model Purdue yang tepat (Level 0 hingga Level 4)!

### Soal 2: Analisis Risiko Conduits Lintas Zona (C4)
Sebuah vendor memasang modem 4G langsung ke port Ethernet PLC Level 1 untuk keperluan "pemeliharaan jarak jauh teknisi luar".
Analisis mengapa konfigurasi ini melanggar arsitektur IEC 62443 secara fatal dan bagaimana arsitektur yang benar untuk akses teknisi pihak ketiga melalui Industrial DMZ!

### Soal 3: Kuantifikasi Ketersediaan Sistem Terdistribusi (C3)
Jalur telemetri getaran pompa air melewati 4 tier berurutan:
- Sensor ke PLC ($A_1 = 0{,}9995$)
- PLC ke SCADA ($A_2 = 0{,}9990$)
- SCADA ke Replicated Historian IDMZ ($A_3 = 0{,}9980$)
- IDMZ ke Cloud Dashboard ($A_4 = 0{,}9950$)

Hitung ketersediaan sistem end-to-end $A_{\text{total}}$ dan estimasikan waktu downtime kumulatif tahunan (dalam jam per tahun)!

### Soal 4: Eksperimen Modifikasi Aturan Simulasi (C5)
Buka skrip [purdue_security_sim.py](src/purdue_security_sim.py). Modifikasi aturan conduit sehingga sistem mengizinkan komunikasi protokol `OPC_UA_REPLICATION` dari Level 3 ke IDMZ, namun tetap memblokir segala bentuk permintaan koneksi balik yang diinisiasi dari IDMZ menuju Level 3 (prinsip reverse proxy / un-idirectional pull). Uji perubahan Anda dan catat log keluarannya!

