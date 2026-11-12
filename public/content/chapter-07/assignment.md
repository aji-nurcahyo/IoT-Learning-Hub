# Tugas & Rubrik — Chapter 07

## Skenario Tugas: Akuisisi Sinyal Analog Terfilter & Kontrol PWM Dual-Channel

Rancang *Firmware* (dan skema Wokwi atau analisis Python) untuk `ESP32-DevKitC V4` yang membaca tegangan input analog dari potensiometer (`GPIO 34`, `ADC1_CH6`) dan mengendalikan **dua LED komplementer** melalui PWM `LEDC` ($5\text{ kHz}$, 10-bit):
- `LED_WARM` (`GPIO 25`, + $220\,\Omega$): kecerahan berbanding lurus dengan tegangan ($0\% \rightarrow 100\%$).
- `LED_COOL` (`GPIO 26`, + $220\,\Omega$): kecerahan berbanding terbalik ($100\% \rightarrow 0\%$).

## Persyaratan Teknis

1. Gunakan `analogReadMilliVolts()` pada kanal **`ADC1`** dengan atenuasi `ADC_11db`.
2. Terapkan filter *moving average* non-blocking (`N >= 8` sampel tiap $25\text{--}50\text{ ms}$) menggunakan *circular buffer* $O(1)$.
3. Lakukan *clamping* nilai tegangan agar aman pada batas `0..3300 mV` sebelum dipetakan ke `0..1023` duty PWM.
4. Sertakan analisis tertulis singkat tentang batas Nyquist jika sinyal analog diganti oleh sinyal AC berfluktuasi $25\text{ Hz}$, serta jelaskan perbedaan kurva linier vs *gamma* pada persepsi LED.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Pemilihan pin ADC1 & perhitungan kuantisasi** | **25** | Menggunakan pin ADC1 aman Wi-Fi, `ADC_11db`, `analogReadMilliVolts()`, serta hitungan LSB tepat. |
| **Desain filter noise & analisis sampling** | **25** | *Moving average* circular buffer bebas `delay()` serta analisis kriteria Nyquist akurat. |
| **Konfigurasi LEDC PWM & pemetaan duty cycle** | **30** | API `ledcAttach`/`ledcWrite` benar, dua channel komplementer akurat dengan *clamping* aman. |
| **Dokumentasi, simulasi & kejujuran bukti** | **20** | Wiring table jelas, log uji/simulasi terdokumentasi tanpa klaim hardware palsu. |

