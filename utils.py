import pypdf
import io

def extrair_texto_pdf(pdf_file):
    """
    Lê o conteúdo de um arquivo PDF carregado via Streamlit e extrai o texto.
    """
    try:
        # O Streamlit passa um objeto BytesIO, o pypdf consegue ler diretamente
        reader = pypdf.PdfReader(pdf_file)
        texto_completo = ""
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            texto_completo += page.extract_text() + "\n"
            
        return texto_completo
    except Exception as e:
        print(f"Erro ao extrair PDF: {e}")
        return ""
