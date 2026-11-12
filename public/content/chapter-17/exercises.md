# Exercises — Chapter 17: Bluetooth Low Energy (BLE)

## A. Pertanyaan Konseptual

1. Jelaskan mengapa 3 kanal *advertising* BLE (`37, 38, 39`) ditempatkan di $2402\text{ MHz}$, $2426\text{ MHz}$, dan $2480\text{ MHz}$ dibanding diletakkan berurutan di satu ujung pita $2{,}4\text{ GHz}$.
2. Bedakan peran **GAP Peripheral vs Central** dengan peran **GATT Server vs Client**. Bisakah sebuah *Central* sekaligus bertindak sebagai *GATT Server*? Berikan contoh singkatnya!
3. Mengapa *Characteristic* dengan properti `NOTIFY` membutuhkan *Descriptor* `0x2902` (CCCD), sementara *Characteristic* `WRITE` saja tidak membutuhkannya?

## B. Analisis Protokol & Daya (`ble_gatt_sim.py`)

4. Sebuah node kesehatan mengirim paket telemetri biner sepanjang **$92\text{ byte}$**. Hitung berapa PDU notifikasi ATT yang diperlukan apabila:
   - a) `ATT_MTU = 23` (default)
   - b) `ATT_MTU = 65`
   - c) `ATT_MTU = 247`
5. Pada karakteristik standar `0x2A6E` (*Temperature*, resolusi $0{,}01\,^\circ\text{C}$, bertanda *little-endian*), byte mentah yang diterima adalah `4A 0B`. Tentukan nilai suhu dalam $^\circ\text{C}$! Bagaimana jika byte yang diterima adalah `9C FF` (bilangan *two's complement* 16-bit bertanda)?
6. Modifikasi parameter pada [`ble_gatt_sim.py`](content/chapter-17/src/ble_gatt_sim.py) untuk baterai LiPo $1000\text{ mAh}$ dengan *Advertising Interval* $250\text{ ms}$ dan $1500\text{ ms}$, lalu bandingkan estimasi umur baterainya.

## C. Latihan Pemrograman ESP32 (`ble_gatt_sensor.ino`)

7. Buka [`ble_gatt_sensor.ino`](content/chapter-17/src/ble_gatt_sensor/ble_gatt_sensor.ino). Tambahkan **Characteristic ketiga** untuk kelembapan relatif (`UUID 0x2A6F`, tipe `uint16` skala $0{,}01\%$, properti `READ | NOTIFY` + `BLE2902`) di dalam *Service* `0x181A`.
8. Ubah properti karakteristik suhu dari `NOTIFY` menjadi `INDICATE` pada sketsa uji lokal (ubah flag properti dan ganti pemanggilan `notify()` menjadi `indicate()`), lalu jelaskan dampak latensi *handshake* jika interval dipercepat ke `100 ms`.

## Expected Output Acuan

Saat menjalankan [`ble_gatt_sim.py`](content/chapter-17/src/ble_gatt_sim.py) tanpa modifikasi, hasil keluarannya harus persis seperti pada [`outputs.md`](content/chapter-17/outputs.md):

- `temp=27.85 C -> bytes=e1 0a -> decoded=27.85 C`
- `ATT_MTU=23 -> packets_needed=4`, `ATT_MTU=65 -> packets_needed=2`, `ATT_MTU=247 -> packets_needed=1`
- `adv_interval=100.0 ms -> 27.2 days`, `adv_interval=1000.0 ms -> 239.8 days`, `adv_interval=2000.0 ms -> 424.1 days`.

