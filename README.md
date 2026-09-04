# Aplikasi Pembaca Naskah Dikili Gorontalo

Aplikasi ini merupakan digitalisasi "Naskah D" (milik Mustapa Taha) dari Tradisi Lisan *Dikili* di Gorontalo.
Aplikasi ini menyajikan 17 Sair dan Doa Khatmul Dikili dengan antarmuka yang modern, nyaman dibaca, dan telah dioptimalkan untuk kaligrafi Arab Pegon/Jawi.

## Fitur
- **Pemisahan Teks Cerdas:** Teks Arab, Transliterasi, Terjemahan, dan Catatan (Jābu) dipisahkan dalam blok-blok dengan warna berbeda.
- **Dukungan Arab Pegon:** Menggunakan font *Scheherazade New* yang sangat ideal untuk karakter-karakter spesifik naskah Jawi/Pegon Nusantara.
- **Koreksi Teks Otomatis:** Termasuk perbaikan *bidirectional text* yang bermasalah dari dokumen PDF, dan penggabungan paragraf terjemahan yang kompleks.
- **Tema Gelap & Terang:** Mendukung pengalaman membaca di berbagai kondisi cahaya.
- **Responsif:** Tampilan menyesuaikan dengan layar HP maupun Komputer.

## Menjalankan Aplikasi
Aplikasi ini sepenuhnya statis (Client-side HTML/JS/CSS).
Anda cukup membuka file `index.html` di *browser* (Chrome, Firefox, Safari) atau meng-host repositori ini di GitHub Pages.

## Skrip (*Scripts*)
Di dalam folder `scripts/` terdapat kumpulan kode Python yang digunakan untuk mengekstrak dan memproses teks dari PDF aslinya menjadi file `dikili_final.json` yang disajikan di aplikasi.
- `parse_sairs.py`: Ekstraksi awal dari teks mentah.
- `fix_arabic.py`: Memperbaiki kata-kata Arab yang terekstrak terbalik.
- `rebuild_safe.py`: Skrip *pipeline* utama yang memperbaiki catatan kaki, kutipan Al-Qur'an, dan paragraf terjemahan.
- `generate_final_app.py`: Menyatukan `dikili_final.json` menjadi sebuah `index.html` lengkap.

---
*Digitalisasi ini dibangun untuk memudahkan pelestarian dan pembelajaran Kearifan Lokal Gorontalo.*
