import os
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.lancedb import LanceDb, SearchType

# Configuração de caminhos absolutos
base_path = os.path.dirname(os.path.abspath(__file__))
ementarios_path = os.path.join(base_path, "ementarios_universidade")
db_uri = os.path.join(base_path, "data/lancedb")

# Cria a pasta data se não existir para evitar erros de permissão
os.makedirs(os.path.join(base_path, "data"), exist_ok=True)

# Inicialização da Base de Conhecimento
knowledge_base = PDFKnowledgeBase(
    path=ementarios_path,
    vector_db=LanceDb(
        table_name="ementas_federais",
        uri=db_uri,
        search_type=SearchType.vector,
    ),
    reader=PDFReader(chunk=True),
)

def inicializar_base():
    """
    Lê os PDFs da pasta e popula o LanceDB.
    """
    try:
        if not os.path.exists(ementarios_path):
            print(f"Erro: Pasta {ementarios_path} não encontrada.")
            return False
            
        print(f"🚀 Indexando documentos em {db_uri}...")
        knowledge_base.load(recreate=True)
        return True
    except Exception as e:
        print(f"Falha na indexação: {e}")
        return False

if __name__ == "__main__":
    inicializar_base()
