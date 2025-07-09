from app import create_app, db
from app.models import Material
import logging
import sqlalchemy as sa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_material():
    """Debug Material model dan database"""
    app = create_app()
    with app.app_context():
        # Periksa struktur tabel
        inspector = sa.inspect(db.engine)
        columns = inspector.get_columns('material')
        
        logger.info("=== STRUKTUR TABEL MATERIAL ===")
        for col in columns:
            logger.info(f"{col['name']}: {col['type']} (nullable: {col.get('nullable', True)})")
        
        # Periksa apakah kolom 'satuan' ada
        column_names = [col['name'] for col in columns]
        if 'satuan' not in column_names:
            logger.error("KOLOM 'satuan' TIDAK DITEMUKAN DI TABEL MATERIAL!")
            
            # Drop dan recreate tabel
            logger.info("Menghapus dan membuat ulang tabel material...")
            db.session.execute(sa.text('DROP TABLE IF EXISTS material_produk'))
            db.session.execute(sa.text('DROP TABLE IF EXISTS material'))
            db.session.commit()
            
            # Buat ulang tabel
            db.create_all()
            logger.info("Tabel material dibuat ulang.")
            
            # Periksa struktur baru
            columns = inspector.get_columns('material')
            logger.info("=== STRUKTUR TABEL MATERIAL BARU ===")
            for col in columns:
                logger.info(f"{col['name']}: {col['type']} (nullable: {col.get('nullable', True)})")
        
        # Periksa data Material
        materials = Material.query.all()
        logger.info(f"Jumlah Material di database: {len(materials)}")
        
        if materials:
            # Periksa beberapa material pertama
            for i, material in enumerate(materials[:5]):
                logger.info(f"Material #{i+1}: id={material.id}, nama={material.nama}")
                
                # Periksa atribut dengan getattr
                has_satuan = hasattr(material, 'satuan')
                satuan_value = getattr(material, 'satuan', 'TIDAK ADA')
                
                logger.info(f"  - hasattr('satuan'): {has_satuan}")
                logger.info(f"  - satuan value: {satuan_value}")
                
                # Periksa atribut dengan __dict__
                logger.info(f"  - __dict__: {material.__dict__}")
        else:
            logger.warning("Tidak ada data Material di database!")
            
        logger.info("Debug selesai.")

if __name__ == '__main__':
    debug_material()
