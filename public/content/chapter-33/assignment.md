# Tugas Terbimbing: Pemodelan & Parsing Protokol Industri Modbus RTU & OPC UA

## Deskripsi Tugas

Dalam tugas ini, Anda diminta membangun sistem simulasi integrasi protokol industri (*IIoT Protocol Gateway*) yang menjembatani komunikasi serial Modbus RTU dengan pemodelan informasi semantik modern OPC Unified Architecture (OPC UA).

Tugas ini mewajibkan:
1. Pembuatan modul *Modbus Slave Simulator* yang mampu menerima permintaan Function Code 03 (*Read Holding Registers*), memverifikasi checksum integritas data *CRC-16*, dan menyusun paket respon biner standar.
2. Pemodelan struktur data semantik berbasis *OPC UA Information Model* yang mengabstraksikan register numerik menjadi variabel berstempel waktu, ber-metadata satuan (*engineering units*), dan berstatus mutu data (*quality*).
3. Verifikasi otomatis melalui eksekusi skrip Python yang membuktikan akurasi decoding dan navigasi pohon node industri.

## Petunjuk Pengumpulan

1. Kode sumber simulasi Python: `public/content/chapter-33/src/industrial_protocol_sim.py`.
2. Laporan analisis teknis yang mencakup uraian decoding frame byte-per-byte, dokumentasi pemetaan register, serta analisis keamanan arsitektur OT/IT.

## Rubrik Penilaian (Total: 100 Poin)

| Kriteria | Bobot | Deskripsi |
|---|:---:|---|
| **Akurasi Framing Modbus & Komputasi CRC-16** | 35 Poin | Logika parsing frame Modbus RTU, penanganan endianness 16-bit, dan implementasi algoritma CRC-16 polinomial 0xA001 terbukti akurat dan sesuai spesifikasi standar Modbus. |
| **Arsitektur Pemodelan Data OPC UA Semantik** | 35 Poin | Pohon node OPC UA memisahkan objek dan variabel secara hirarkis, menyertakan metadata tipe data, satuan teknik (*engineering units*), dan bendera kualitas secara lengkap. |
| **Analisis Keamanan Konvergensi OT/IT & Gateway** | 30 Poin | Pembahasan menyajikan analisis mendalam mengenai mitigasi ancaman pada bus serial legacy, arsitektur isolasi jaringan (DMZ/Dual-NIC), dan proteksi sertifikat X.509. |
