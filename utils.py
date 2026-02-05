import pypdf

def extrair_texto_pdf(pdf_file):
    reader = pypdf.PdfReader(pdf_file)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text()
    return texto

# Nota: O agente LLM fará a anonimização lógica,
# mas você pode adicionar RegEx aqui para reforçar CPFs.