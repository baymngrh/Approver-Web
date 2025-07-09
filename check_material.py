from app import create_app
from app.models import db, Material
import logging

logging.basicConfig(level=logging.INFO)

app = create_app()
with app.app_context():
    # Cek struktur tabel Material
    print("\nStruktur tabel Material:")
    for column in Material.__table__.columns:
        print(f"{column.name}: {column.type} (nullable: {column.nullable})")
    
    # Cek data di tabel Material
    print("\nData di tabel Material:")
    materials = Material.query.limit(5).all()
    for material in materials:
        print(f"ID: {material.id}, Nama: {material.nama}")
        print(f"  Atribut 'satuan' exists: {hasattr(material, 'satuan')}")
        if hasattr(material, 'satuan'):
            print(f"  Nilai 'satuan': {material.satuan}")
        print(f"  Atribut 'kode' exists: {hasattr(material, 'kode')}")
        if hasattr(material, 'kode'):
            print(f"  Nilai 'kode': {material.kode}")
        print(f"  Dir: {dir(material)}")
        print("---")
    
    # Cek jumlah material yang tidak memiliki satuan
    print("\nJumlah material tanpa satuan:")
    try:
        no_satuan = 0
        for material in Material.query.all():
            if not hasattr(material, 'satuan') or material.satuan is None:
                no_satuan += 1
                print(f"Material tanpa satuan: ID={material.id}, Nama={material.nama}")
        print(f"Total: {no_satuan} dari {Material.query.count()}")
    except Exception as e:
        print(f"Error saat memeriksa satuan: {str(e)}")
