# Latihan Chapter 33: Industrial IoT, Modbus & OPC UA

## Latihan Konseptual

1. **Konvergensi OT vs IT**:
   Bandingkan karakteristik sistem otomasi industri (OT) dengan sistem teknologi informasi korporat (IT) berdasarkan empat dimensi kritis: prioritas keamanan (Kerahasiaan vs Ketersediaan), toleransi latensi komunikasi, siklus hidup perangkat keras, dan dampak kegagalan operasional.

2. **Taksonomi Model Memori Modbus**:
   Lengkapi tabel berikut dengan jenis data yang disimpan, hak akses operasi (Read/Write), dan rentang penomoran alamat standar Modbus:
   - Coils
   - Discrete Inputs
   - Input Registers
   - Holding Registers

3. **Arsitektur Semantik OPC UA**:
   Mengapa pengiriman data sensor melalui OPC UA dianggap jauh lebih aman dan kaya konteks dibandingkan pengiriman melalui Modbus TCP? Jelaskan peranan atribut *DataType*, *EngineeringUnits*, *Timestamp*, dan *Quality* dalam mencegah kesalahan interpretasi data di sistem SCADA/Cloud.

## Latihan Praktik & Perhitungan

1. **Decoding Frame Modbus RTU Biner**:
   Diberikan frame respon biner heksadesimal yang diterima master dari slave sensor daya:
   `01 03 04 00 FF 02 8C CA C6`
   
   *Instruksi*:
   - Tentukan Slave ID dan Function Code yang dieksekusi.
   - Uraikan jumlah byte data payload yang diterima.
   - Konversikan dua register 16-bit ke dalam bilangan desimal integer.
   - Jika register 0 merepresentasikan temperatur dikalikan 10 ($T = \text{Reg}_0 / 10.0$), berapakah suhu aktual yang terukur?
   - Hitung nilai CRC-16 dari 7 byte pertama untuk membuktikan validitas dua byte terakhir (`CA C6`).

2. **Perancangan Pemetaan Register ke Node Tree OPC UA**:
   Rancang dokumen pemetaan data (*Register Mapping Sheet*) yang menghubungkan 4 holding register motor listrik pabrik (Tegangan RMS, Arus RMS, Kecepatan RPM, dan Suhu Bearing) ke dalam struktur hirarkis pohon node OPC UA dengan namespace `ns=2;s=Motors.Induction01.*`.
