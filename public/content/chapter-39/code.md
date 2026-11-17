# Panduan Implementasi: Privacy, Threat Modeling & IoT Governance

Dokumen ini menjelaskan implementasi teknis pemodelan ancaman keamanan siber sistem tertanam berbasis taksonomi STRIDE, kuantifikasi risiko DREAD, dan modul sanitasi privasi data.

## 1. Modul Registri Ancaman & Sanitasi Privasi Python

Modul [threat_model_governance_sim.py](file:///d:/Workstation/Repo%20My%20Corses/Internet%20Of%20Things/public/content/chapter-39/src/threat_model_governance_sim.py) memverifikasi:
1. `ThreatModelRegistry`: mencatat ancaman dalam taksonomi STRIDE dan menghitung skor risiko kuantitatif DREAD:
   $$\text{Risk Score} = \frac{\text{Damage} + \text{Reproducibility} + \text{Exploitability} + \text{Affected Users} + \text{Discoverability}}{5}$$
2. `PrivacyDataMinimizer`: menyaring payload telemetri sebelum ditransmisikan, secara otonom membuang atribut *Personally Identifiable Information* (PII) seperti nama penghuni, email, dan koordinat tempat tinggal.

Jalankan pengujian menggunakan:

```bash
python public/content/chapter-39/src/threat_model_governance_sim.py
```

### Hasil Verifikasi Eksekusi:
```text
=== CHAPTER 39: STRIDE THREAT MODEL & PRIVACY SIMULATION ===
Ancaman 1: THREAT-01 [Spoofing] -> Skor DREAD: 8.0 (CRITICAL)
Ancaman 2: THREAT-02 [Information Disclosure] -> Skor DREAD: 6.0 (HIGH)

Payload Mentah Berbahaya: ['device_id', 'temperature', 'humidity', 'occupant_name', 'occupant_email', 'gps_exact_home']
Payload Higienis Privasi: {'device_id': 'sensor-room-101', 'temperature': 24.5, 'humidity': 55.0}
STATUS: VERIFIED (Semua pengujian model ancaman STRIDE, DREAD, dan sanitasi privasi lulus 100%)
```

## 2. Kepatuhan Regulasi & Privacy by Design

Penerapan `PrivacyDataMinimizer` menjamin sistem memenuhi amanat:
- **UU PDP No. 27/2022**: Memastikan tidak ada data pribadi mentah yang diproses tanpa dasar hukum dan relevansi fungsional.
- **GDPR Article 5(1)(c)**: Penegakan prinsip *Data Minimisation* (data memadai, relevan, dan terbatas pada apa yang diperlukan).
