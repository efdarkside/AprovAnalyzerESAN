import os
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.lancedb import LanceDb, SearchType

# Configuração de caminhos para o Render
base_path = os.path.dirname(os.path.abspath(__file__))
ementarios_path = os.path.join(base_path, "ementarios_universidade")
db_uri = os.path.join(base_path, "data/lancedb")

# Inicialização da Base de Conhecimento usando Phidata
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
        return
    
    print(f"🚀 Carregando ementários de: {ementarios_path}")
    # O Phidata criará a pasta 'data' automaticamente se não existir
    knowledge_base.load(recreate=True)
    print("✅ Base de dados LanceDB atualizada com sucesso!")

if __name__ == "__main__":
    inicializar_base()
