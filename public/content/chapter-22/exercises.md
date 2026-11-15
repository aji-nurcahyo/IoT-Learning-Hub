# Latihan Soal & Praktik — Chapter 22

## Bagian A — Soal Konseptual

1. **Perbandingan Topologi Jaringan**:
   Mengapa pada lingkungan pabrik dengan ratusan sensor getaran mesin, penggunaan gerbang *Edge Gateway* lokal lebih disukai dibandingkan membiarkan setiap sensor menghubungkan diri langsung ke server cloud melalui Wi-Fi?
2. **Karakteristik Serial Linux**:
   Jelaskan perbedaan antara antarmuka `/dev/ttyUSB0` dan `/dev/ttyAMA0` pada Raspberry Pi. Jika adapter USB dicabut lalu dipasang kembali, mengapa penamaan port dapat berubah menjadi `/dev/ttyUSB1`, dan bagaimana aturan *udev rules* dapat digunakan untuk membuat symlink port persisten (misal: `/dev/iot-sensor`)?
3. **Supervisi systemd**:
   Pada file unit `iot-gateway.service`, terdapat baris:
   ```ini
   Restart=always
   RestartSec=5s
   ```
   Jelaskan apa yang terjadi jika sensor fisik terus-menerus mengirimkan data sampah (*noise burst*) sehingga program gateway mengalami *uncaught exception* dan keluar dengan kode error `1`.

## Bagian B — Soal Praktik Komputasi

1. **Implementasi Checksum Framing**:
   Diberikan sebuah string frame serial mentah:
   `$DATA,ESP32-LAB,201,31.20,55.80,3300`
   Gunakan fungsi `calculate_lrc_checksum()` dari skrip [`serial_mqtt_gateway.py`](content/chapter-22/src/serial_mqtt_gateway.py) untuk menghasilkan nilai LRC heksadesimal yang valid, kemudian susun frame lengkap yang siap dikirimkan melalui kabel serial.
2. **Uji Penanganan Sinyal Graceful**:
   Jalankan skrip `serial_mqtt_gateway.py` pada terminal. Modifikasi skrip agar melakukan simulasi pembacaan terus-menerus (`time.sleep(1)`), kemudian kirimkan sinyal `SIGINT` (Ctrl+C). Amati pesan keluaran di layar dan pastikan jumlah frame yang berhasil diproses tercetak sebelum proses berhenti.
