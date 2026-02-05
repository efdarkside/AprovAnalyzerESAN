import os
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.lancedb import LanceDb, SearchType

# Configuração de caminhos absolutos para o ambiente Render
base_path = os.path.dirname(os.path.abspath(__file__))
ementarios_path = os.path.join(base_path, "ementarios_universidade")
# Armazenamos na pasta 'data' que o Render pode acessar
db_uri = os.path.join(base_path, "data/lancedb")

# Garante que a pasta de dados exista antes de iniciar o banco
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
    Função para carregar os PDFs no banco vetorial.
    """
    if not os.path.exists(ementarios_path):
        print(f"Erro: A pasta {ementarios_path} não foi encontrada.")
        return False
    
    try:
        print(f"🚀 Iniciando indexação de: {ementarios_path}")
        knowledge_base.load(recreate=True)
        print("✅ LanceDB populado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao carregar base: {e}")
        return False

if __name__ == "__main__":
    inicializar_base()
