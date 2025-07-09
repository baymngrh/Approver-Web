from app import create_app, db
from app.models import Produk, Material, KomposisiMaterial, StokProduk, TargetPengiriman, RencanaProduksi, MaterialProduk
from app.utils.material import baca_csv_material
import csv
import os
import datetime
import logging
import sqlalchemy as sa

logging.basicConfig(level=logging.INFO)

def init_db():
    """Inisialisasi database dan import data awal"""
    app = create_app()
    
    # Fungsi print dengan flush
    def print_flush(message):
        print(message, flush=True)
    
    with app.app_context():
        # Buat semua tabel
        db.create_all()
        
        # Verifikasi struktur tabel Material
        inspector = sa.inspect(db.engine)
        columns = inspector.get_columns('material')
        column_names = [col['name'] for col in columns]
        
        print("\nMaterial table structure:", flush=True)
        for col in columns:
            print(f"{col['name']}: {col['type']} (nullable: {col.get('nullable', True)})", flush=True)
        
        # Verifikasi field yang diperlukan
        required_fields = ['id', 'nama', 'kode', 'satuan', 'Satuan', 'stok', 'min_stok', 'status']
        missing_fields = [field for field in required_fields if field not in column_names]
        
        # Selalu recreate tabel Material untuk memastikan field Satuan ada
        print("\nRecreating Material table to ensure 'Satuan' field exists...", flush=True)
        
        # Drop tabel Material dan dependensinya
        db.session.execute(sa.text('DROP TABLE IF EXISTS material_produk'))
        db.session.execute(sa.text('DROP TABLE IF EXISTS material'))
        db.session.commit()
        
        # Tambahkan field Satuan ke model Material jika belum ada
        if not hasattr(Material, 'Satuan'):
            Material.Satuan = db.Column(db.String(20), nullable=True)
            print("Added 'Satuan' field to Material model", flush=True)
        
        # Buat ulang tabel
        db.create_all()
        
        # Verifikasi struktur tabel setelah recreate
        inspector = sa.inspect(db.engine)
        columns = inspector.get_columns('material')
        print("\nUpdated Material table structure:", flush=True)
        for col in columns:
            print(f"{col['name']}: {col['type']} (nullable: {col.get('nullable', True)})", flush=True)
        
        # Pastikan field Satuan ada
        column_names = [col['name'] for col in columns]
        if 'Satuan' not in column_names:
            print("WARNING: 'Satuan' field still missing after recreate!", flush=True)
        else:
            print("SUCCESS: 'Satuan' field added to Material table", flush=True)
        
        # Import data dari MATERIAL 2.csv
        print("Importing data from MATERIAL 2.csv...", flush=True)
        success, message = baca_csv_material('MATERIAL 2.csv')
        
        if not success:
            print(f"Error importing data: {message}")
            return
            
        print("Data import successful")
        
        # Commit changes
        db.session.commit()
        
        # Print summary
        produk_count = Produk.query.count()
        material_count = Material.query.count()
        komposisi_count = KomposisiMaterial.query.count()
        print(f"\nDatabase summary:")
        print(f"Products: {produk_count}")
        print(f"Materials: {material_count}")
        print(f"Material compositions: {komposisi_count}")

        # Simpan semua perubahan
        db.session.commit()
        print("Data contoh berhasil dibuat")

if __name__ == '__main__':
    init_db()
