# 🚀 Odoo 18.0 Development & VoIP Learning Project

Repositori ini dirancang sebagai lingkungan pengembangan (*development environment*) yang praktis untuk mempelajari pembuatan modul kustom **Odoo 18.0** menggunakan **Docker Compose**, sekaligus media belajar integrasi telepon **VoIP** menggunakan **Asterisk PBX**.

---

## 📂 Struktur Project

```text
odoo/
├── docker-compose.yml       # Konfigurasi orkestrasi container Odoo & Postgres
├── .env                     # Kredensial & variabel rahasia database
├── .gitignore               # Daftar file yang diabaikan oleh Git
├── README.md                # Panduan utama project (file ini)
│
├── config/
│   └── odoo.conf            # Konfigurasi server Odoo (Auto-Reload aktif)
│
├── addons/                  # Folder tempat membuat kustom modul Odoo
│   └── my_first_module/     # Modul kustom pertama untuk latihan CRUD
│
├── asterisk/                # Rencana folder konfigurasi Asterisk PBX
│   └── config/              # File *.conf Asterisk (pjsip, http, manager, dll.)
│
└── Dokumen_Panduan/         # Buku panduan belajar yang sudah disiapkan
    ├── odoo_handbook.md     # Panduan umum belajar Odoo (13 Bab)
    ├── odoo_syntax_handbook.md  # Detail sintaks Python ORM & XML View
    └── odoo_docker_handbook.md  # Detail cara kerja Docker, Compose & Dockerfile
```

---

## ⚡ Cara Menjalankan Project (Quick Start)

1. **Jalankan Container**:
   Buka terminal di folder project ini, lalu ketik:
   ```bash
   docker compose up -d
   ```
2. **Akses Odoo**:
   Buka browser laptop Anda dan arahkan ke alamat:
   ```text
   http://localhost:8069
   ```
3. **Matikan Container**:
   Jika ingin menghentikan sementara proses running:
   ```bash
   docker compose down
   ```

---

## 📚 Buku Panduan Belajar yang Tersedia

Anda telah dibekali dengan 3 buku panduan super lengkap dalam Bahasa Indonesia untuk mempercepat proses belajar:

1. [📘 Odoo Handbook & Cheatsheet](odoo_handbook.md)
   * Panduan umum pengembangan Odoo dari arsitektur hingga PDF report.
2. [✍️ Odoo Coding Syntax & Structure](odoo_syntax_handbook.md)
   * Panduan mendalam tentang penulisan logika Python ORM, pembuatan field relasi, dan manipulasi UI menggunakan XML & XPath.
3. [🐳 Odoo Docker & Dockerfile Guide](odoo_docker_handbook.md)
   * Penjelasan detail setiap properti di `docker-compose.yml` baris per baris, analogi Docker, dan cara membuat image Odoo kustom menggunakan Dockerfile.

---

## 📞 Cetak Biru (Blueprint) Integrasi VoIP Asterisk

Proyek selanjutnya adalah mengintegrasikan Odoo Community dengan **Asterisk PBX** untuk fitur telepon internal menggunakan modul **`voip_oca`** berbasis WebRTC.

### Skema Alur Integrasi:
```text
[ Browser User di Odoo ] 
          │ 
          │ (SIP.js via Secure WebSocket)
          ▼ 
[ Port 8088 /ws di Container Asterisk ]
          │
          │ (Dialplan PJSIP)
          ▼
[ Jalur Telepon Luar (VoIP Provider / Sip Trunk) ]
```

### Langkah Konfigurasi Mendatang:
1. **Tambahkan Service Asterisk** di `docker-compose.yml`:
   Menggunakan image `andrius/asterisk` dengan port `5060` (SIP), `5038` (AMI), dan `8088` (WebSocket).
2. **Konfigurasi Asterisk WebRTC**:
   Mengaktifkan WebSocket di `http.conf` and membuat ekstensi WebRTC di `pjsip.conf`.
3. **Instal Modul `voip_oca`**:
   Mendownload modul dari repositori OCA `connector-telephony` ke folder `addons/` dan mengaktifkannya di Odoo.
4. **Pasang HTTPS/SSL**:
   Menggunakan Reverse Proxy (seperti Nginx atau Traefik) agar browser mengizinkan akses mikrofon saat diakses dari luar `localhost`.
