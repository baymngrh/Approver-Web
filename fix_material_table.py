from app import create_app
from app.models import db, Material
import sqlalchemy as sa

def fix_material_table():
    """Corrigir a estrutura da tabela Material para adicionar o campo Satuan"""
    app = create_app()
    
    with app.app_context():
        print("Verificando estrutura da tabela Material...", flush=True)
        
        # Verificar estrutura atual
        inspector = sa.inspect(db.engine)
        columns = inspector.get_columns('material')
        column_names = [col['name'] for col in columns]
        
        print("Colunas atuais:", column_names, flush=True)
        
        # Verificar se o campo Satuan existe
        if 'Satuan' not in column_names:
            print("Campo 'Satuan' não encontrado. Adicionando...", flush=True)
            
            # Adicionar campo Satuan ao modelo Material
            if not hasattr(Material, 'Satuan'):
                Material.Satuan = sa.Column(sa.String(20), nullable=True)
                print("Campo 'Satuan' adicionado ao modelo Material", flush=True)
            
            # Recriar tabela
            print("Recriando tabela Material...", flush=True)
            db.session.execute(sa.text('DROP TABLE IF EXISTS material_produk'))
            db.session.execute(sa.text('DROP TABLE IF EXISTS material'))
            db.session.commit()
            
            # Criar tabela novamente
            db.create_all()
            print("Tabela Material recriada com sucesso!", flush=True)
            
            # Verificar nova estrutura
            inspector = sa.inspect(db.engine)
            columns = inspector.get_columns('material')
            column_names = [col['name'] for col in columns]
            print("Novas colunas:", column_names, flush=True)
            
            if 'Satuan' in column_names:
                print("Campo 'Satuan' adicionado com sucesso!", flush=True)
            else:
                print("ERRO: Campo 'Satuan' ainda não existe na tabela!", flush=True)
        else:
            print("Campo 'Satuan' já existe na tabela Material", flush=True)
        
        # Verificar se há dados na tabela Material
        materials = Material.query.all()
        print(f"Total de registros na tabela Material: {len(materials)}", flush=True)
        
        # Verificar alguns registros
        if materials:
            for i, material in enumerate(materials[:5]):
                print(f"Material #{i+1}: id={material.id}, nome={material.nama}", flush=True)
                
                # Verificar atributos
                attrs = vars(material)
                print(f"  Atributos: {attrs.keys()}", flush=True)
                
                # Verificar se tem o atributo satuan
                if hasattr(material, 'satuan'):
                    print(f"  satuan: {material.satuan}", flush=True)
                else:
                    print("  ERRO: Material não tem atributo 'satuan'!", flush=True)
                
                # Verificar se tem o atributo Satuan
                if hasattr(material, 'Satuan'):
                    print(f"  Satuan: {material.Satuan}", flush=True)
                else:
                    print("  ERRO: Material não tem atributo 'Satuan'!", flush=True)

if __name__ == '__main__':
    fix_material_table()
