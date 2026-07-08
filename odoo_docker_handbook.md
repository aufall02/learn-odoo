# 🐳 Odoo Docker & Docker Compose Developer Handbook (Bahasa Indonesia)

Buku panduan ini ditulis khusus sebagai referensi belajar mandiri untuk menguasai konsep Docker dan Docker Compose dari dasar (nol) hingga mahir, dengan studi kasus langsung pada ekosistem **Odoo ERP** dan **PostgreSQL**.

---

## 1. Pengenalan Konsep Dasar Docker (Analogi Sederhana)

Jika Anda baru pertama kali belajar Docker, bayangkan Docker seperti **sistem pengiriman peti kemas (kontainer) di pelabuhan laut internasional**.

```text
+-------------------------------------------------------------+
|                      ANALOGI PELABUHAN                      |
|                                                             |
|  [ Resep Makanan ]    ------->  [ Makanan Instan Box ]       |
|    (Dockerfile)                   (Docker Image)            |
|                                         |                   |
|                                         v                   |
|                                 [ Makanan Siap Saji ]       |
|                                   (Docker Container)        |
+-------------------------------------------------------------+
```

### 1. Docker Image
* **Analogi**: Resep masakan tertulis atau cetak biru (*blueprint*) pabrik.
* **Penjelasan**: File *read-only* (tidak bisa diubah) yang berisi semua file sistem, aplikasi, pustaka (libraries), dan konfigurasi yang diperlukan untuk menjalankan suatu aplikasi.
* **Contoh**: Image `postgres:16-alpine` adalah file installer mentah yang berisi OS Linux Alpine dan software PostgreSQL 16 yang sudah siap dipasang.

### 2. Docker Container
* **Analogi**: Masakan yang dibuat berdasarkan resep, atau kotak kontainer fisik yang diturunkan di pelabuhan.
* **Penjelasan**: Instance hidup (*running instance*) dari sebuah Docker Image. Jika Image adalah aplikasinya, maka Container adalah aplikasi tersebut yang sedang aktif berjalan di memori RAM komputer Anda. Anda bisa membuat banyak container dari satu image yang sama.

### 3. Volume
* **Analogi**: Gudang eksternal di luar pelabuhan.
* **Penjelasan**: Tempat penyimpanan data khusus di luar siklus hidup container. Secara default, jika container dihapus, semua file baru di dalamnya akan hilang. Volume digunakan agar data (seperti file database) tetap aman dan tidak ikut terhapus saat container dihancurkan.

### 4. Bind Mount
* **Analogi**: Jembatan langsung antara folder di komputer Anda dengan folder di dalam container.
* **Penjelasan**: Metode menghubungkan folder fisik di komputer Anda langsung ke dalam folder di dalam container. Jika Anda mengedit file di folder komputer Anda, file di dalam container akan ikut berubah secara instan. Sangat cocok untuk menulis kode source code (addons) Odoo.

### 5. Network
* **Analogi**: Kabel LAN virtual atau sistem telepon internal pelabuhan.
* **Penjelasan**: Jaringan virtual yang dibuat Docker agar container-container Anda (misalnya container Odoo dan container PostgreSQL) bisa saling berkomunikasi dengan aman tanpa bisa diakses oleh aplikasi luar yang tidak berkepentingan.

### 6. Port
* **Analogi**: Nomor loket pelayanan di kantor pelabuhan.
* **Penjelasan**: Gerbang masuk untuk mengakses layanan di dalam container. Odoo berjalan di dalam container pada port `8069`. Agar browser laptop Anda bisa membukanya, kita harus memetakan port laptop ke port container tersebut.

### 7. Environment Variable
* **Analogi**: Kertas catatan instruksi khusus sebelum koki mulai memasak.
* **Penjelasan**: Nilai-nilai konfigurasi dinamis yang dilewatkan ke dalam container saat container dinyalakan (misalnya: username database, password, atau nama database).

### 8. Dockerfile
* **Analogi**: Kertas resep masak langkah demi langkah.
* **Penjelasan**: File teks berisi instruksi otomatis untuk membuat Docker Image kustom Anda sendiri (misal: install dependency Python tambahan).

### 9. Docker Compose
* **Analogi**: Mandor pelabuhan yang mengkoordinasikan banyak kontainer sekaligus.
* **Penjelasan**: Alat untuk mendefinisikan dan menjalankan aplikasi multi-container. Cukup menggunakan satu file konfigurasi (`docker-compose.yml`), Anda bisa menghidupkan Odoo dan database PostgreSQL sekaligus secara otomatis.

---

## 2. Struktur Dasar Docker Compose (Format YAML)

Docker Compose menggunakan format file **YAML** (*Yet Another Markup Language*). Karakteristik utama YAML adalah menggunakan **Indentasi Spasi (bukan Tab!)** untuk menentukan hierarki (struktur tingkat) datanya.

```yaml
version: '3'          # <-- Tingkat 1: Versi skema docker compose

services:             # <-- Tingkat 1: Daftar container yang akan dibuat
  odoo:               # <-- Tingkat 2: Nama service container pertama
    image: odoo:18.0  # <-- Tingkat 3: Properti service odoo

volumes:              # <-- Tingkat 1: Daftar penyimpanan persistent
  odoo-db-data:       # <-- Tingkat 2: Nama volume yang didaftarkan
```

⚠️ **Aturan Emas YAML**:
* Selalu gunakan tombol spasi (biasanya 2 atau 4 spasi) untuk menggeser teks ke dalam.
* **Jangan pernah menggunakan tombol TAB**, karena akan membuat Docker Compose error saat dibaca.

---

## 3. Penjelasan Detail Properti Docker Compose

Berikut penjelasan baris per baris properti yang sering dipakai di file `docker-compose.yml`.

### 1. `image`
* **Definisi**: Menentukan image docker mana yang akan diunduh dari *Docker Hub* untuk dijadikan container.
* **Cara Kerja**: Docker akan mencari image di memori laptop Anda terlebih dahulu. Jika tidak ada, Docker akan mendownloadnya secara otomatis dari internet.
* **Best Practice**: Selalu tentukan versi spesifik (tag), jangan gunakan tag `latest`. Contoh: `postgres:16-alpine` lebih aman dibanding `postgres`.

### 2. `build`
* **Definisi**: Digunakan jika Anda ingin membuat image kustom sendiri menggunakan file `Dockerfile` lokal daripada mengunduh image mentah.
* **Kapan digunakan**: Saat modul Odoo Anda membutuhkan library Python tambahan yang tidak ada di image standar Odoo resmi.

### 3. `container_name`
* **Definisi**: Nama unik yang diberikan kepada container yang aktif berjalan.
* **Efek Jika Dihapus**: Docker akan memberikan nama acak secara otomatis (misalnya: `project_odoo_1`).
* **Best Practice**: Selalu tentukan nama container secara jelas (misal: `container_name: odoo-dev`) agar mudah saat Anda memanggil perintah terminal.

### 4. `restart`
* **Pilihan Nilai**:
  * `no` (Default): Container tidak akan menyala lagi jika mati atau laptop di-restart.
  * `always`: Container akan selalu menyala kembali secara otomatis.
  * `unless-stopped`: Container akan menyala otomatis, **kecuali** jika Anda mematikannya secara manual menggunakan perintah `docker stop`.
* **Kapan digunakan**: Gunakan `unless-stopped` untuk kenyamanan development agar database dan Odoo otomatis menyala saat laptop Anda dihidupkan.

### 5. `ports`
* **Definisi**: Memetakan port di laptop Anda (Host) ke port di dalam container.
* **Format**: `- [PORT_LAPTOP] : [PORT_CONTAINER]`
* **Contoh**: `- "8069:8069"` artinya: saat Anda membuka `localhost:8069` di browser laptop, Docker akan meneruskan request tersebut ke port `8069` di dalam container Odoo.
* **Efek Jika Diubah**: Jika Anda ubah menjadi `- "8888:8069"`, maka Anda harus mengakses Odoo di browser laptop dengan alamat `localhost:8888`.

### 6. `expose`
* **Definisi**: Membuka port container hanya untuk container lain yang berada dalam satu jaringan virtual, **tanpa** membukanya ke laptop luar.
* **Kapan digunakan**: Untuk database PostgreSQL. Database hanya boleh diakses oleh Odoo (sesama container), bukan oleh aplikasi luar laptop secara bebas. Jadi gunakan `expose` atau tidak usah di-map sama sekali port database ke luar untuk alasan keamanan.

### 7. `environment`
* **Definisi**: Mendefinisikan variabel lingkungan (environment variables) secara langsung di dalam file YAML.
* **Kapan digunakan**: Untuk settingan cepat yang nilainya jarang berubah.

### 8. `env_file`
* **Definisi**: Membaca variabel lingkungan dari file teks terpisah (biasanya bernama `.env`).
* **Fungsi**: Memisahkan data rahasia (seperti password database) dari file `docker-compose.yml` utama agar password tidak ikut ter-upload ke Git.
* **Best Practice**: Masukkan file `.env` ke dalam berkas `.gitignore`.

### 9. `depends_on`
* **Definisi**: Mengatur urutan startup antar container.
* **Cara Kerja**: Odoo membutuhkan database untuk berjalan. Properti `depends_on` memastikan container PostgreSQL dinyalakan terlebih dahulu sebelum container Odoo dinyalakan.
* **Kelemahan Tanpa Healthcheck**: Secara default, `depends_on` hanya menunggu container PostgreSQL *menyala*, bukan menunggu database di dalamnya *siap menerima koneksi*. Makanya harus digabung dengan status `condition: service_healthy`.

### 10. `tty` & `stdin_open`
* **Definisi**: Membuka terminal interaktif di dalam container.
* **Kapan digunakan**: Diaktifkan (`tty: true`) saat development agar log keluaran Odoo tampil dengan format warna yang rapi dan interaktif di terminal Anda.

---

## 4. Deep Dive: Healthcheck (Dokter Virtual Docker)

### Analogi Sederhana
Bayangkan sebuah rumah sakit (Docker). Ada pasien (Container PostgreSQL) baru saja masuk ruangan. `depends_on` biasa hanya memastikan pasien sudah "masuk kamar", tapi dokter (Healthcheck) bertugas mengecek apakah pasien tersebut "sudah sadar dan siap diajak bicara" sebelum memanggil perawat (Container Odoo).

```text
[ PostgreSQL Start ] ──(10 detik proses internal)──> [ Database Siap ]
        │                                                     │
        ▼                                                     ▼
 depends_on biasa                                     depends_on + Healthcheck
 (Odoo langsung start -> Error!)                      (Odoo menunggu hingga database siap)
```

### Bedah Sintaks Healthcheck PostgreSQL

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-odoo} -d ${POSTGRES_DB:-postgres}"]
  interval: 10s
  timeout: 5s
  retries: 5
```

1. **`test`**: Perintah uji yang dijalankan secara berkala di dalam container.
2. **`CMD-SHELL`**: Menginstruksikan Docker untuk menjalankan perintah menggunakan shell internal container.
3. **`pg_isready`**: Tool bawaan PostgreSQL untuk mengecek apakah server database aktif menerima koneksi.
4. **`interval: 10s`**: Docker akan menjalankan tes kesehatan ini setiap 10 detik sekali.
5. **`timeout: 5s`**: Jika tes kesehatan membutuhkan waktu lebih dari 5 detik untuk merespon, tes tersebut dianggap gagal (*fail*).
6. **`retries: 5`**: Jika tes gagal sebanyak 5 kali berturut-turut, Docker akan menandai container tersebut sebagai **Unhealthy** (Sakit).
7. **Bagaimana Odoo memanfaatkannya?**
   Di bagian Odoo, kita menulis:
   ```yaml
   depends_on:
     postgres:
       condition: service_healthy # Hanya start Odoo jika status Postgres sudah Healthy
   ```

---

## 5. Volume & Persistence (Penyimpanan Data)

### Mengapa Data Database Tidak Boleh Disimpan di Dalam Container?
Container Docker bersifat **Ephemeral** (sementara/sekali pakai). Container didesain agar bisa dihapus, diganti versi barunya, dan dibuat ulang kapan saja tanpa memikirkan data di dalamnya.
Jika Anda menyimpan data transaksi penjualan Odoo di dalam container PostgreSQL secara langsung tanpa Volume, maka saat container tersebut Anda matikan dan hapus, **seluruh data transaksi bisnis Anda akan hilang permanen!**

### Perbandingan Penyimpanan: Named Volume vs Bind Mount

| Fitur | Named Volume | Bind Mount |
|---|---|---|
| **Sintaks** | `odoo-db-data:/var/lib/...` | `./addons:/mnt/extra-addons` |
| **Lokasi Fisik** | Dikelola internal oleh Docker (di folder aman root Linux). | Folder biasa yang Anda buat sendiri di laptop Anda. |
| **Kemudahan Edit** | Sulit diakses langsung oleh user biasa. | Sangat mudah dibuka/diedit lewat VSCode. |
| **Tujuan Utama** | Untuk menyimpan data sistem/database (Aman & Cepat). | Untuk menulis source code / kustom modul. |

---

## 6. Workflow Development Odoo dengan Docker

Untuk develop modul Odoo, kita menggunakan **Bind Mount** pada folder `addons/`.

### 1. Sinkronisasi Folder (Host ↔ Container)
Anda menulis kode Python/XML di laptop Anda dalam folder `./addons/my_module`. Karena folder `./addons` di-mount ke container pada path `/mnt/extra-addons`, maka container Odoo akan melihat modul baru tersebut secara instan.

### 2. Cara Kerja Hot Reload (Auto-Update Kode)
Di file `odoo.conf` Anda, baris berikut sangat penting untuk development:
```ini
dev_mode = reload,qweb,xml
```
* **Python Auto-reload**: Jika Anda mengubah file Python, Odoo akan mendeteksi perubahan dan melakukan restart internal secara otomatis tanpa Anda perlu mengetik `docker compose restart odoo`.
* **XML Auto-reload**: Perubahan file XML tampilan akan langsung diperbarui saat Anda me-refresh browser (tanpa perlu upgrade modul secara manual melalui menu Apps Odoo).

---

## 7. Referensi Cepat Perintah Docker Terminal

Berikut adalah daftar perintah terminal yang wajib diketahui oleh developer Odoo:

| Perintah | Fungsi Utama | Efek Samping |
|---|---|---|
| `docker ps` | Melihat daftar container yang sedang aktif berjalan. | Menampilkan ID, nama container, port, dan status kesehatan. |
| `docker ps -a` | Melihat semua container (baik yang aktif maupun yang mati). | Membantu melacak container yang mati karena error. |
| `docker logs -f odoo-dev` | Menampilkan log output Odoo secara real-time. | Membantu melihat error Python/traceback secara langsung di layar terminal. |
| `docker exec -it odoo-dev bash` | Masuk ke dalam terminal/shell container Odoo. | Anda bisa menjelajahi file sistem internal Linux di dalam Odoo. |
| `docker compose up -d` | Menyalakan semua container di background. | Mengunduh image jika belum ada dan membuat container baru. |
| `docker compose down` | Mematikan dan menghapus seluruh container project. | Data persistent aman di named volume, tetapi container dihancurkan. |
| `docker compose down -v` | Mematikan container **sekaligus menghapus seluruh data database**. | ⚠️ **Semua data database terhapus total dan bersih kembali.** |

---

## 8. Studi Kasus: Bedah File `docker-compose.yml` Baris Per Baris

Mari kita bedah konfigurasi lengkap yang telah disiapkan untuk Anda:

```yaml
services:
  # ============================================
  # SERVICE 1: Odoo Web Server
  # ============================================
  odoo:
    image: odoo:18.0                         # Menggunakan OS Odoo versi 18 resmi
    container_name: odoo-dev                 # Menamai container menjadi "odoo-dev"
    env_file: .env                           # Membaca variabel database dari file .env
    depends_on:
      postgres:
        condition: service_healthy           # Start Odoo hanya jika Postgres benar-benar siap
    ports:
      - "8069:8069"                          # Akses web Odoo via localhost:8069
      - "8072:8072"                          # Akses jalur chatting realtime Odoo
    volumes:
      - odoo-filestore:/var/lib/odoo         # Menyimpan attachment gambar/dokumen user
      - ./addons:/mnt/extra-addons           # Jembatan folder custom addons di laptop
      - ./config/odoo.conf:/etc/odoo/odoo.conf:ro # Menggunakan file config odoo (Read-Only)
    restart: unless-stopped                  # Selalu hidupkan kembali jika tidak dimatikan manual
    tty: true                                # Mengaktifkan log warna interaktif di terminal

  # ============================================
  # SERVICE 2: PostgreSQL Database
  # ============================================
  postgres:
    image: postgres:16-alpine                # Menggunakan Postgres 16 berbasis Linux Alpine (ringan)
    container_name: odoo-db                  # Menamai container database menjadi "odoo-db"
    env_file: .env                           # Membaca username & password dari file .env
    volumes:
      - odoo-db-data:/var/lib/postgresql/data/pgdata # Menyimpan data tabel database agar aman
    restart: unless-stopped                  # Selalu restart otomatis jika mati
    healthcheck:                             # Dokter virtual untuk cek kesiapan database
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-odoo} -d ${POSTGRES_DB:-postgres}"]
      interval: 10s                          # Cek setiap 10 detik sekali
      timeout: 5s                            # Maksimal toleransi waktu cek 5 detik
      retries: 5                             # Toleransi kegagalan cek hingga 5 kali

# ============================================
# DEKLARASI PENYIMPANAN DATA (VOLUMES)
# ============================================
volumes:
  odoo-filestore:
    name: odoo-dev-filestore                 # Mendaftarkan volume odoo-filestore secara resmi
  odoo-db-data:
    name: odoo-dev-db                        # Mendaftarkan volume database odoo-db secara resmi
```

---

## 9. Panduan Praktis & Best Practice untuk Pemula

### 1. Struktur Folder Ideal
Selalu simpan file konfigurasi Docker di root project, dan letakkan modul kustom di dalam folder terpisah (misalnya folder `addons/`). Jangan mencampuradukkan file docker dengan folder addons bawaan Odoo.

### 2. Penanganan Error Izin Akses Folder (Linux)
Jika Anda menggunakan bind mount folder lokal Linux (seperti `./addons` atau jika Anda memaksakan menyimpan database di `./pgdata`), selalu ingat bahwa user di dalam Docker berbeda dengan user laptop Anda. Jika terjadi error *Permission Denied*, jalankan:
```bash
sudo chmod -R 777 ./addons
```

### 3. Cara Mengamankan Password Database
Jangan pernah menulis password database langsung di file `docker-compose.yml`. Gunakan file `.env` dan tambahkan nama file `.env` tersebut ke file `.gitignore` agar password rahasia Anda tidak terunggah ke repositori Github publik saat Anda melakukan commit kode.

---

## 10. Deep Dive: Dockerfile (Membuat Image Odoo Kustom)

### Apa itu Dockerfile?
Jika `docker-compose.yml` adalah file untuk menyusun dan menghubungkan container yang sudah ada, **`Dockerfile`** adalah resep langkah demi langkah untuk membuat **Docker Image kustom sendiri**.

### Kapan Odoo Membutuhkan Dockerfile?
Secara default, image resmi `odoo:18.0` hanya dibekali library standar bawaan Odoo. Namun, dalam dunia nyata, custom module/addons Odoo yang Anda buat sering kali membutuhkan:
1. **Library Python Tambahan**: Misalnya `pandas` untuk analisis data, `num2words` untuk konversi angka ke kata terbilang, atau `phonenumbers` untuk validasi nomor telepon.
2. **Library Sistem OS (Debian)**: Misalnya tool `git` untuk download module github luar, atau libssl-dev.

### Contoh Implementasi Dockerfile Kustom
Buat file bernama `Dockerfile` (tanpa ekstensi apa pun) di root directory project Anda:

```dockerfile
# ============================================
# 1. Tentukan Base Image (Image Dasar)
# ============================================
FROM odoo:18.0

# ============================================
# 2. Ganti ke User 'root' (Hak Akses Administrator)
# ============================================
# Secara default, image Odoo berjalan dengan user biasa bernama 'odoo'.
# Kita harus beralih ke 'root' agar diperbolehkan menginstal paket-paket baru.
USER root

# ============================================
# 3. Install Dependensi Sistem OS (Debian)
# ============================================
# RUN digunakan untuk menjalankan perintah bash di dalam container selama fase build.
# --no-install-recommends & rm -rf /var/lib/apt/lists/* digunakan untuk menjaga ukuran image tetap kecil.
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# 4. Copy File requirements.txt dari Laptop ke Container
# ============================================
# Buat file requirements.txt yang berisi daftar library Python yang Anda inginkan.
COPY ./requirements.txt /etc/odoo/requirements.txt

# ============================================
# 5. Install Library Python via pip
# ============================================
RUN pip3 install --no-cache-dir -r /etc/odoo/requirements.txt

# ============================================
# 6. Kembalikan User ke 'odoo' (Best Practice Keamanan)
# ============================================
# Sangat tidak direkomendasikan menjalankan container Odoo aktif sebagai root.
# Oleh karena itu, di akhir file kita harus mengembalikan user ke 'odoo'.
USER odoo
```

### Cara Memakainya di `docker-compose.yml`
Ubah bagian service `odoo` Anda dari semula membaca `image` langsung menjadi melakukan proses `build`:

```yaml
services:
  odoo:
    # Hapus atau beri tanda komentar pada baris image resmi
    # image: odoo:18.0 
    
    # Ganti dengan baris build berikut:
    build:
      context: .              # Folder tempat file Dockerfile berada (titik artinya saat ini)
      dockerfile: Dockerfile  # Nama file Dockerfile-nya
    
    container_name: odoo-dev
    # ... konfigurasi lainnya tetap sama ...
```

### Cara Menjalankannya
Jika Anda membuat perubahan pada `Dockerfile` atau file `requirements.txt`, jalankan perintah berikut agar Docker melakukan kompilasi ulang (rebuild) pada image kustom Anda:

```bash
docker compose up -d --build
```
Properti `--build` memaksa Docker untuk membaca kembali berkas `Dockerfile` dan menginstal dependensi baru yang Anda daftarkan.

---

## 11. Panduan Command Line Odoo (Odoo CLI) di Docker

Selain perintah Docker dasar, Odoo memiliki program Command Line Interface (CLI) sendiri di dalam container yang sangat penting untuk development sehari-hari (seperti membuat modul, menginstall, atau mengupdate modul).

### Kenapa Kata `odoo` Ditulis 2 Kali?
Saat menjalankan perintah CLI Odoo melalui Docker Compose, Anda akan melihat pola perintah seperti ini:
```bash
docker compose exec odoo odoo <perintah_lanjutan>
```
* **`odoo` Pertama**: Merujuk pada **Nama Service** di dalam file `docker-compose.yml` Anda (agar Docker tahu container mana yang dituju).
* **`odoo` Kedua**: Merujuk pada **Nama Perintah Executable** (`/usr/bin/odoo`) di dalam Linux container Odoo untuk menjalankan aplikasi Odoo CLI.

---

### A. Sub-Command Utama Odoo CLI

#### 1. `scaffold` (Membuat Modul Baru)
Membuat kerangka (boilerplate) folder dan file standar untuk modul kustom baru Anda.
* **Perintah**:
  ```bash
  docker compose exec odoo odoo scaffold nama_modul /mnt/extra-addons
  ```
* **Solusi Error Permission (Linux)**: Jika Anda menemui error *Permission Denied*, jalankan perintah tersebut dengan user root (`-u root`) kemudian ganti hak milik foldernya di laptop Anda:
  ```bash
  docker compose exec -u root odoo odoo scaffold nama_modul /mnt/extra-addons && sudo chown -R $USER:$USER addons/nama_modul
  ```

#### 2. `shell` (Terminal Interaktif Odoo & Database)
Membuka shell interaktif Python (REPL) yang sudah ter-load dengan environment Odoo dan koneksi database.
* **Perintah**:
  ```bash
  docker compose exec odoo odoo shell -d odoo_dev
  ```
  *(Ganti `odoo_dev` dengan nama database Odoo Anda)*.
* **Kegunaan**: Berguna untuk melakukan query langsung ke database menggunakan ORM Odoo, membuat data dummy, atau melakukan testing logic sederhana menggunakan objek `self` atau `env` (misal: `self.env['res.partner'].search([])`).

---

### B. Flag/Parameter Odoo Server yang Sering Digunakan

Saat Anda ingin menjalankan proses instalasi atau pembaruan modul secara langsung dari terminal tanpa melalui browser:

#### 1. `-i` atau `--init` (Menginstal Modul Baru)
Digunakan untuk memasang modul kustom atau modul bawaan pertama kali ke database.
* **Perintah**:
  ```bash
  docker compose exec odoo odoo -i nama_modul -d odoo_dev --stop-after-init
  ```

#### 2. `-u` atau `--update` (Meng-upgrade Modul) ⭐
Sangat penting! Jika Anda memodifikasi file XML (views/tampilan), Python (models), atau file security CSV, Anda harus memicu upgrade modul agar perubahan tersebut disimpan ke database.
* **Perintah**:
  ```bash
  docker compose exec odoo odoo -u nama_modul -d odoo_dev --stop-after-init
  ```

#### 3. `--stop-after-init`
Digunakan bersamaan dengan `-i` atau `-u`. Flag ini memerintahkan server Odoo untuk mati secara otomatis begitu proses instalasi/update selesai, agar terminal Anda bebas kembali.

#### 4. `--dev=all` (Auto-Reload & Hot-Reload) ⭐
Sangat disarankan saat Anda sedang aktif menulis kode!
* **Perintah**:
  ```bash
  docker compose exec odoo odoo --dev=all
  ```
* **Kegunaan**: 
  * Jika file Python diubah dan disimpan, Odoo akan me-restart server internalnya secara otomatis.
  * Jika file XML/QWeb diubah dan disimpan, Odoo akan memuat ulang tampilannya saat Anda me-refresh browser (tidak perlu melakukan `-u` manual lagi).


