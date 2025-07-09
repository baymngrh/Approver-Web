# Dashboard Monitoring Produksi Tisu Basah

Aplikasi web berbasis Flask untuk monitoring produksi tisu basah mingguan.

## Fitur Utama

- **Form Input Produksi**: Input data produksi dengan perhitungan otomatis kebutuhan material
- **Dashboard Monitoring**: Visualisasi data produksi dengan pie chart dan tabel
- **Alert Pengiriman**: Notifikasi jika stok produk tidak mencukupi target pengiriman
- **Running Text Progress**: Informasi real-time tentang progress produksi
- **Ekspor Data**: Cetak hasil atau ekspor ke Excel

## Persyaratan Sistem

- Python 3.8 atau lebih baru
- Dependensi lain (lihat `requirements.txt`)

## Instalasi

1. Clone repositori ini atau download sebagai ZIP
2. Buat virtual environment (opsional tapi direkomendasikan):
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Install dependensi:
   ```
   pip install -r requirements.txt
   ```
4. Inisialisasi database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## Penggunaan

1. Jalankan aplikasi:
   ```
   python app.py
   ```
2. Buka browser dan akses `http://localhost:5000`

## Struktur Data CSV

File CSV untuk komposisi material harus memiliki format berikut:
- Nama Produk
- Nama Material
- Jenis
- Kelompok
- Jumlah Per Pack
- Satuan

Contoh:
```
Nama Produk,Nama Material,Jenis,Kelompok,Jumlah Per Pack,Satuan
WETKINS 50S,Spunlace,Bahan Baku,Kain,3.5,gram
WETKINS 50S,Parfum,Bahan Baku,Kimia,0.2,ml
```

## Panduan Penggunaan

### Import Data Material
1. Klik menu "Import CSV"
2. Upload file CSV dengan format yang sesuai
3. Klik "Upload & Import"

### Input Produksi Baru
1. Klik menu "Input Produksi"
2. Pilih produk dari dropdown
3. Isi jumlah sheet per pack, pack per karton, dan target produksi
4. Klik "Hitung & Simpan"
5. Lihat hasil perhitungan dan kebutuhan material

### Monitoring Dashboard
1. Klik menu "Dashboard"
2. Lihat pie chart distribusi produksi mingguan
3. Pantau progress produksi aktif

### Update Progress Produksi
1. Di halaman beranda, klik "Update Progress" pada produksi yang ingin diupdate
2. Masukkan jumlah karton yang sudah diproduksi
3. Klik "Simpan"

## Pengembangan Lebih Lanjut

Beberapa ide untuk pengembangan lebih lanjut:
- Integrasi dengan sistem inventory
- Notifikasi email/SMS untuk alert stok
- Laporan produksi bulanan/tahunan
- Dashboard untuk analisis tren produksi

## Lisensi

© 2025 Dashboard Monitoring Produksi Tisu Basah
