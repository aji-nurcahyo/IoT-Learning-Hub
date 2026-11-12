# Standar kurikulum

Metadata `content/catalog.json` adalah sumber utama. Empat level masing-masing memuat sepuluh chapter; chapter 10, 20, 30, dan 40 menjadi capstone. Daftar lengkap ada pada CURRICULUM.md, dihasilkan dari metadata. Lima specialization tracks merupakan modul tambahan, bukan level wajib atau syarat membuka chapter.

Platform adalah perpustakaan terbuka. Tidak ada akun, tracking progress, persentase completion, gamification, unlocking, atau LMS dashboard. Prasyarat bersifat saran belajar dan tidak mengunci navigasi.

Setiap chapter lengkap harus mencakup modul bacaan, tujuan terukur, prasyarat, konsep/teori, rumus/diagram jika relevan, slide Reveal.js, latihan bertingkat, tugas atau mini project, rubrik 100 poin, ringkasan, serta referensi/atribusi. Source code, notebook, telemetry/dataset, dan output harus sesuai relevansi. Target awal 15–25 slide dan sekitar 5–8 contoh kode, dengan pengecualian yang dijelaskan secara pedagogis. Template fondasi berisi enam slide demo kemampuan; bukan chapter lengkap.

Resource tersedia hanya jika file benar-benar ada dan tidak kosong. File bacaan chapter berada di `public/content/.../*.md`; deck dalam JSON. Resource yang tidak relevan menyimpan alasan, bukan file palsu. File yang masih direncanakan menghalangi publikasi. Notebook tidak wajib pada semua topik.

Praktik hardware wajib memiliki BOM, model dan revisi board, pin mapping, wiring diagram, electrical limits berdasarkan datasheet komponen, driver/protection, versi toolchain/library, prosedur build/flash/run, kondisi uji, dan bukti. Mulai dari low-voltage DC. Jika tidak ada board, label verifikasi tetap sesuai bukti compile/simulator; catat bahwa hardware belum diuji.

Publication guard memeriksa schema, tujuan, keterkaitan level/prasyarat, resource nyata, rubrik 100 poin, laporan reviewer bertanggal, referensi, dokumen hardware, label verifikasi, dan hash bukti. Review manusia tetap diperlukan untuk kebenaran, orisinalitas, kualitas pedagogis, dan keselamatan. Hash membuktikan integritas file, bukan kebenaran eksperimen.
