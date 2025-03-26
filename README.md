# 📚 Toko Buku CLI CRUD Application

Aplikasi berbasis Python untuk mengelola data barang, pegawai, dan transaksi pembeli di toko buku menggunakan database MySQL dengan antarmuka Command Line Interface (CLI).

![GitHub license](https://img.shields.io/github/license/zidanmubarak/toko-buku-cli-crud)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![MySQL](https://img.shields.io/badge/database-MySQL-orange)

## 📋 Fitur

* ✅ **CRUD** (Create, Read, Update, Delete) untuk data barang dan pegawai
* 🔐 Sistem login dengan animasi terminal
* 💰 Transaksi pembelian dengan struk pembelian
* 🎨 Tampilan tabel dengan pewarnaan stok barang
* 📊 Laporan penjualan dan inventaris

## 🛠️ Teknologi yang Digunakan

* **Python** - Bahasa pemrograman utama
* **MySQL** - Database untuk penyimpanan data
* **Colorama** - Untuk tampilan berwarna di terminal
* **MySQL Connector** - Untuk koneksi ke database MySQL
* **Tabulate** - Untuk tampilan data dalam bentuk tabel

## 🔧 Cara Instalasi dan Menjalankan

### Prasyarat

* Python 3.6 atau lebih tinggi
* MySQL Server
* pip (Python package installer)

### Langkah-langkah Instalasi

1. Clone repositori ini:
<<<<<<< HEAD

```bash
git clone https://github.com/zidanmubarak/toko-buku-cli-crud.git
cd toko-buku-cli-crud
```
=======
   ```bash
   git clone https://github.com/zidanmubarak/CRUD-Project.git
>>>>>>> e233cf7581a3b6ae934df344591c6f98ccb0f7a9

2. Instal library yang diperlukan:

```bash
pip install -r requirements.txt
```

3. Konfigurasikan database:
   * Buka phpMyAdmin atau alat pengelolaan database MySQL favorit Anda
   * Buat database baru dengan nama `toko_buku`
   * Import file SQL yang disediakan di folder `database/` (misalnya, `toko_buku.sql`):
      * Klik tab Import di phpMyAdmin
      * Pilih file `toko_buku.sql` dari repositori ini
      * Klik tombol Go untuk menyelesaikan proses impor

4. Jalankan aplikasi:
<<<<<<< HEAD

```bash
python src/project.py
```

## 🗂️ Struktur Proyek

```
toko-buku-cli-crud/
├── database/             # Folder database
│   └── toko_buku.sql     # Skema dan data awal
├── project.py            # File utama aplikasi
├── requirements.txt      # Daftar dependensi Python
├── .gitignore            # File konfigurasi git untuk mengabaikan file tertentu
├── LICENSE               # Informasi lisensi
└── README.md             # Dokumentasi proyek
```

## 📝 Lisensi

[MIT](LICENSE) © Zidan Mubarak
=======
    ```bash
    python src/project.py
>>>>>>> e233cf7581a3b6ae934df344591c6f98ccb0f7a9
