import os
from agno.knowledge.pdf_knowledge import PDFKnowledgeBase
from agno.knowledge.pdf_reader import PDFReader
from agno.vectordb.lancedb import LanceDb, SearchType

knowledge_base = PDFKnowledgeBase(
    path="ementarios_universidade/",
    vector_db=LanceDb(
        table_name="ementas_federais",
        uri=db_uri,
        search_type=SearchType.vector,
    ),
    reader=PDFReader(chunk=True),
)

def inicializar_base():
    if not os.path.exists(db_uri):
        print("🚀 Primeira execução detectada. Criando base de dados...")
        knowledge_base.load(recreate=True)
    else:
        print("✅ Base de dados já existente.")

if __name__ == "__main__":
    inicializar_base()
