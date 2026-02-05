import os
from agno.vectordb.lancedb import LanceDb, SearchType

try:
    from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
except ImportError:
    try:
        from agno.knowledge.pdf_knowledge import PDFKnowledgeBase
        from agno.knowledge.pdf_reader import PDFReader
    except ImportError:
        try:
            from agno.pdf import PDFKnowledgeBase, PDFReader
        except ImportError:
            raise ImportError("Não foi possível localizar os módulos PDFKnowledgeBase/PDFReader no pacote agno. Verifique o requirements.txt.")

base_path = os.path.dirname(os.path.abspath(__file__))
ementarios_path = os.path.join(base_path, "ementarios_universidade")
db_uri = os.path.join(base_path, "data/lancedb")

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
    Pode ser chamada pelo main.py ou via script direto.
    """
    if not os.path.exists(ementarios_path):
        print(f"Erro: A pasta {ementarios_path} não foi encontrada.")
        return
    
    print(f"🚀 Carregando ementários de: {ementarios_path}")
    knowledge_base.load(recreate=True)
    print("✅ Base de dados LanceDB atualizada com sucesso!")

if __name__ == "__main__":
    inicializar_base()
