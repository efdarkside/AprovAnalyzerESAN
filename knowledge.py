import os
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.lancedb import LanceDb, SearchType

knowledge_base = PDFKnowledgeBase(
    path="ementarios_universidade/", # Pasta onde você colocará os PDFs dos 6 cursos
    vector_db=LanceDb(
        table_name="ementas_federais",
        uri=db_uri,
        search_type=SearchType.vector,
    ),
    reader=PDFReader(chunk=True), # Divide o PDF em pedaços para melhor busca
)

# Comando para carregar os dados (você executará isso uma vez ou via interface)
# knowledge_base.load(recreate=True)
