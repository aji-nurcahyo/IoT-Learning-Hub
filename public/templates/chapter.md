# Template modul IoT

**Template penulisan, bukan chapter selesai.** Isi contoh di sini hanya memperlihatkan kemampuan renderer. Penulis harus mengganti instruksi dengan materi dan bukti yang nyata sebelum publikasi.

## Tujuan pembelajaran

1. Rumuskan kemampuan yang dapat diamati: menghitung, membandingkan, merancang, atau menguji.
2. Tentukan artefak yang menunjukkan keberhasilan dan batasan evaluasinya.

## Prasyarat

- Tautkan chapter pendukung melalui metadata.
- Jelaskan kebutuhan tool, matematika, atau hardware; sediakan jalur alternatif bila memungkinkan.

## Konsep dan teori

Bedakan sistem fisik, Firmware, konektivitas, dan aplikasi. Diagram konseptual di bawah tidak merupakan wiring:

```text
Sensor -> Microcontroller -> Gateway -> Aplikasi
              ^                            |
              +-------- Command -----------+
```

Rumus ilustratif hukum Ohm adalah $V = IR$. Ini bukan hasil pengukuran board.

$$
P = VI
$$

| Simbol | Besaran | Unit |
| --- | --- | --- |
| V | Tegangan | volt |
| I | Arus | ampere |
| R | Resistansi | ohm |

## Diagram, wiring, dan Bill of materials

Untuk praktik hardware, lengkapi model/revisi board, BOM, pin mapping, wiring diagram, datasheet, supply voltage, batas current, driver/protection, versi toolchain/library, serta instruksi build/flash/run. Jangan memberi instruksi wiring generik untuk seluruh varian ESP32.

## Source code dan output

Contoh format JSON berikut adalah **data sintetis**, bukan pembacaan Sensor:

```json
{
  "device_id": "demo-device",
  "source": "synthetic",
  "unit": "example"
}
```

Code fence berikut menguji daftar isi. Baris di dalamnya tidak boleh menjadi heading:

```markdown
# Ini bukan heading daftar isi
```

Sertakan sekitar 5–8 contoh kode bila topik memerlukannya; jangan menambah contoh demi jumlah. Notebook dan dataset bersifat kondisional. Resource yang tidak relevan harus memiliki alasan metadata.

## Bukti pengujian

Status template: **Belum diuji** untuk eksperimen hardware. Penulis harus mencatat command, lingkungan, versi, tanggal, kondisi, hasil asli, dan keterbatasan. Simpan hash bukti agar perubahan log terdeteksi. Compile berhasil bukan Hardware-verified.

## Latihan

1. Dasar: identifikasi komponen dan jelaskan perannya pada diagram.
2. Menengah: bandingkan dua pilihan komunikasi untuk kebutuhan yang diberikan.
3. Lanjutan: rancang skenario kegagalan dan bukti yang diperlukan untuk mengevaluasinya.

Latihan ini merupakan contoh bentuk soal. Tambahkan data, batasan, dan kriteria jawaban untuk chapter yang sebenarnya.

## Tugas

Rancang mini project yang menghasilkan artefak, instruksi reproduksi, dan laporan batasan. Contoh distribusi rubrik berikut berjumlah 100; kriteria rinci harus disesuaikan dengan tugas nyata dan disimpan di metadata.

| Kriteria | Poin | Bukti yang diminta |
| --- | --- | --- |
| Analisis kebutuhan | 20 | Alasan pemilihan dan batasan |
| Implementasi | 30 | Source code dan konfigurasi |
| Pengujian | 30 | Prosedur, log asli, dan analisis |
| Dokumentasi | 20 | Reproduksi, keselamatan, dan atribusi |

## Ringkasan

Hubungkan kembali konsep dengan tujuan. Nyatakan apa yang sudah dibuktikan dan apa yang belum. Target awal presentasi adalah 15–25 slide saat penulisan chapter; deck template pendek tidak menggantikan materi tersebut.

## Referensi dan atribusi

Gunakan sumber primer, simpan tanggal pemeriksaan serta versi dokumen. Contoh sumber: [Espressif ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/index.html) dan [NIST Cybersecurity for IoT](https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program). Tautan bukan endorsement. Catat lisensi setiap diagram, snippet, dataset, dan materi yang digunakan kembali.
