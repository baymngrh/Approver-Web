from app import create_app
from app.utils.material import baca_csv_material
from app.models.models import db, KomposisiMaterial, Produk, Material, Produksi

app = create_app()
with app.app_context():
    # Cek data di database
    print("\nData di database:")
    produk_count = Produk.query.count()
    material_count = Material.query.count()
    komposisi_count = KomposisiMaterial.query.count()
    print(f"Jumlah Produk: {produk_count}")
    print(f"Jumlah Material: {material_count}")
    print(f"Jumlah Komposisi Material: {komposisi_count}")
    
    # Cari produk yang muncul di API kebutuhan material
    print("\nMencari produk 'WIP ALFA KUROMI HAND & MOUTH 20S'...")
    produk = Produk.query.filter(Produk.nama.like('%ALFA KUROMI HAND & MOUTH%')).first()
    if produk:
        print(f"Produk ditemukan: ID={produk.id}, Nama={produk.nama}")
        
        # Cek komposisi material untuk produk ini
        komposisi_list = KomposisiMaterial.query.filter_by(produk_id=produk.id).all()
        print(f"Jumlah komposisi material untuk produk ini: {len(komposisi_list)}")
        
        print("\nDetail komposisi material:")
        for k in komposisi_list:
            material = Material.query.get(k.material_id)
            print(f"Material: {material.nama}, Jumlah per pack: {k.jumlah_per_pack}, Satuan: {k.satuan}")
        
        # Cek produksi yang menggunakan produk ini
        produksi_list = Produksi.query.filter_by(produk_id=produk.id).all()
        print(f"\nJumlah produksi untuk produk ini: {len(produksi_list)}")
        for p in produksi_list:
            print(f"Produksi ID: {p.id}, Tanggal: {p.tanggal}, Jumlah Karton: {p.jumlah_karton}, Pack per Karton: {p.pack_per_karton}")
    else:
        print("Produk tidak ditemukan")
        
        # Cari produk lain yang mungkin digunakan
        print("\nMencari produk lain yang mungkin digunakan di API kebutuhan material...")
        produksi = Produksi.query.order_by(Produksi.id.desc()).first()
        if produksi:
            produk = Produk.query.get(produksi.produk_id)
            print(f"Produksi terakhir: ID={produksi.id}, Produk={produk.nama}, Jumlah Karton: {produksi.jumlah_karton}")
            
            # Cek komposisi material untuk produk ini
            komposisi_list = KomposisiMaterial.query.filter_by(produk_id=produk.id).all()
            print(f"Jumlah komposisi material untuk produk ini: {len(komposisi_list)}")
            
            print("\nDetail komposisi material:")
            for k in komposisi_list:
                material = Material.query.get(k.material_id)
                print(f"Material: {material.nama}, Jumlah per pack: {k.jumlah_per_pack}, Satuan: {k.satuan}")
        else:
            print("Tidak ada data produksi")

