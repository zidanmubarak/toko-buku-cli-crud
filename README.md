# Toko Buku CRUD Application

Aplikasi berbasis Python untuk mengelola data barang, pegawai, dan transaksi pembeli di toko buku menggunakan database MySQL.

## 📋 Fitur
- CRUD (Create, Read, Update, Delete) untuk data barang dan pegawai.
- Sistem login dengan animasi terminal.
- Transaksi pembelian dengan struk pembelian.
- Tampilan tabel dengan pewarnaan stok barang.

## 🛠️ Teknologi yang Digunakan
- **Python**
- **MySQL**


## 🔧 Cara Instalasi dan Menjalankan
1. Clone repositori ini:
   ```bash
   git clone https://github.com/username/project_name.git
   cd project_name

2. Instal library yang diperlukan:
    ```bash
    pip install -r requirements.txt

3. Konfigurasikan database:
    - Buka phpMyAdmin atau alat pengelolaan database MySQL favorit Anda.
    - Buat database baru dengan nama `toko_buku`.
    - Import file SQL yang disediakan di folder database/ (misalnya, toko_buku.sql):
        - Klik tab Import di phpMyAdmin.
        - Pilih file `toko_buku.sql` dari repositori ini.
        - Klik tombol Go untuk menyelesaikan proses impor.

4. Jalankan aplikasi:
    ```bash
    python src/main.py


