# Panduan Implementasi: Industrial IoT, Modbus & OPC UA

Dokumen ini menjelaskan implementasi teknis parsing frame Modbus RTU dan navigasi Information Model OPC UA menggunakan modul simulasi Python mandiri.

## 1. Modul Simulasi Protokol Industri Python

Modul [industrial_protocol_sim.py](file:///d:/Workstation/Repo%20My%20Corses/Internet%20Of%20Things/public/content/chapter-33/src/industrial_protocol_sim.py) memverifikasi dua protokol otomasi industri utama:
1. `ModbusSlaveSimulator`: menerima request frame biner, menghitung dan memvalidasi CRC-16 Modbus (polinomial `0xA001`), serta mengemas nilai holding registers ke dalam response frame.
2. `OpcUaNodeTreeSimulator`: memodelkan hierarki grafik node OPC UA (`Objects` dan `Variables`) lengkap dengan metadata tipe data, satuan teknik (*engineering units*), dan mutu data (*quality*).

Jalankan pengujian menggunakan:

```bash
python public/content/chapter-33/src/industrial_protocol_sim.py
```

### Hasil Verifikasi Eksekusi:
```text
=== CHAPTER 33: INDUSTRIAL IOT & PROTOCOLS SIMULATION ===
Modbus RTU Request Frame: 010300000002C40B (CRC: 0BC4)
Modbus RTU Response Frame: 01030400FF028CCAC6
Nilai Register 0 (Suhu x10): 255 -> 25.5 C
Nilai Register 1 (Kelembaban x10): 652 -> 65.2 %
OPC UA Read Temp: 25.5 degC (Quality: Good)
OPC UA Read Pressure: 101.3 kPa (Quality: Good)
STATUS: VERIFIED (Semua pengujian Modbus frame dan OPC UA Information Tree lulus 100%)
```

## 2. Arsitektur Komputasi CRC-16 Modbus

Fungsi perhitungan CRC-16 memproses aliran byte biner dengan operasi bitwise deterministik:

```python
def calculate_modbus_crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc
```

Pada frame respon `01 03 04 00 FF 02 8C CA C6`:
- 7 byte pertama (`01 03 04 00 FF 02 8C`) menghasilkan CRC `0xC6CA`.
- Karena Modbus RTU mengirimkan byte LSB terlebih dahulu (Little-Endian), dua byte terakhir dalam frame adalah `0xCA` diikuti `0xC6`.
