-- Membuat tabel barang
CREATE TABLE barang (
    buku_id CHAR(10) PRIMARY KEY,
    nama_buku VARCHAR(255) NOT NULL,
    type_buku VARCHAR(255) NOT NULL,
    stok_buku INT NOT NULL,
    harga FLOAT NOT NULL
);

-- Membuat tabel pegawai
CREATE TABLE pegawai (
    pegawai_id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pegawai VARCHAR(255) NOT NULL,
    alamat VARCHAR(255) NOT NULL,
    no_hp VARCHAR(15) NOT NULL
);

-- Membuat tabel pembeli
CREATE TABLE pembeli (
    id_pembeli INT AUTO_INCREMENT PRIMARY KEY,
    nama_pembeli VARCHAR(255) NOT NULL,
    alamat VARCHAR(255) NOT NULL
);

-- Membuat tabel transaksi
CREATE TABLE transaksi (
    id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
    id_pembeli INT NOT NULL,
    buku_id CHAR(10),
    jumlah_buku INT NOT NULL,
    harga_per_buku FLOAT NOT NULL,
    total_harga FLOAT NOT NULL,
    tanggal DATE NOT NULL,
    waktu TIME NOT NULL,
    FOREIGN KEY (id_pembeli) REFERENCES pembeli(id_pembeli),
    FOREIGN KEY (buku_id) REFERENCES barang(buku_id)
);

-- Insert data ke tabel barang
INSERT INTO barang (buku_id, nama_buku, type_buku, stok_buku, harga) VALUES
('B001', 'Aldebaran', 'Novel', 10, 150000);

-- Insert data ke tabel pegawai
INSERT INTO pegawai (nama_pegawai, alamat, no_hp) VALUES
('Samsul Siregar', 'Jl. Merdeka No. 10', '081234567890');
