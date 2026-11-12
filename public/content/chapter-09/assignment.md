# Tugas & Rubrik — Chapter 09

## Skenario Tugas: Sistem Pengendali Pendingin & Interlock Low-Voltage DC

Rancang *Firmware* dan skema rangkaian *low-voltage DC* untuk pengendalian **2 tahap aktuator** (misal kipas pendingin PWM pada `GPIO 25` + indikator/buzzer alarm pada `GPIO 26`, serta *safety interlock* pada `GPIO 27`) berbasis pembacaan sensor suhu analog pada `GPIO 34` (`ADC1`). *Catatan: Tidak diperbolehkan menggunakan beban AC PLN.*

## Persyaratan Teknis

1. **Skema Driver Low-Voltage DC**: Gambarkan atau susun tabel koneksi lengkap *low-side MOSFET/NPN driver* dengan resistor *gate/base*, resistor *pull-down* $10\text{ k}\Omega$, *flyback diode* antiparalel, suplai eksternal $5\text{ V}/12\text{ V}$, dan *common* `GND` ke ESP32.
2. **Kontrol Histeresis**: Terapkan minimal 2 batas suhu ($T_{\text{low}}, T_{\text{high}}$) dengan *deadband* yang jelas untuk mencegah *chattering*.
3. **Safety Interlock & Fail-Safe**: Interlock terbuka atau pembacaan sensor `NaN` harus langsung mematikan aktuator PWM (`duty = 0`) dan menyalakan alarm dalam waktu $< 500\text{ ms}$.
4. **Verifikasi & Simulasi**: Sertakan skrip uji/simulasi Python atau konfigurasi Wokwi serta nyatakan status verifikasi secara jujur.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Desain rangkaian driver & proteksi induktif** | **30** | Driver MOSFET/BJT tepat, *flyback diode*, resistor gate/base, *pull-down* fail-safe, dan *common GND* lengkap. |
| **Implementasi kontrol histeresis & PWM** | **25** | *Deadband* tepat bebas *chattering*, aktuasi PWM LEDC benar dan non-blocking. |
| **Safety interlock & prinsip fail-safe** | **25** | Penanganan sensor `NaN`, *interlock* darurat prioritas tertinggi, serta inisialisasi boot aman. |
| **Dokumentasi, simulasi & kejujuran bukti** | **20** | BOM low-voltage DC lengkap, log simulasi/expected output terdokumentasi tanpa klaim palsu. |

