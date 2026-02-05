import streamlit as st
import os
from agents import diretor_coordenacao
from knowledge import knowledge_base
from utils import extrair_texto_pdf

# Configuração de limite de upload e layout
st.set_page_config(
    page_title="AprovAnalyzer ESAN", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS para garantir que o upload não falhe por timeout visual
st.markdown("""
    <style>
    .stDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ Sistema de Aproveitamento de Estudos - ESAN")
st.markdown("---")

# Sidebar para administração da base
with st.sidebar:
    st.header("Painel Administrativo")
    st.write("Use este botão apenas quando adicionar novos ementários na pasta do GitHub.")
    if st.button("🔄 Atualizar Base de Ementas"):
        with st.spinner("Indexando PDFs no LanceDB..."):
            try:
                knowledge_base.load(recreate=True)
                st.success("Base atualizada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao atualizar base: {e}")

# Área principal de upload do estudante
st.info("Suba aqui o ementário enviado pelo estudante (IES Externa) para análise.")

# Definindo um limite claro de 20MB para evitar erro 400 no Render
uploaded_file = st.file_uploader("Escolher arquivo PDF", type="pdf", help="Limite de 20MB por arquivo")

if uploaded_file is not None:
    # Mostra progresso de leitura
    st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")
    
    if st.button("🚀 Iniciar Análise Multiagente"):
        with st.spinner("Os agentes estão analisando os documentos e comparando com a base da ESAN..."):
            try:
                # Extração do texto do PDF enviado usando a função utilitária
                texto_estudante = extrair_texto_pdf(uploaded_file)
                
                if not texto_estudante or len(texto_estudante.strip()) < 50:
                    st.warning("O PDF parece estar vazio ou é uma imagem (necessário OCR).")
                else:
                    # Execução da equipe de agentes
                    prompt = f"Analise este pedido de aproveitamento vindo de outra instituição: {texto_estudante}"
                    response = diretor_coordenacao.run(prompt)
                    
                    st.markdown("### 📋 Parecer Final da Coordenação")
                    st.markdown(response.content)
            except Exception as e:
                st.error(f"Ocorreu um erro durante a análise: {e}")

st.markdown("---")
st.caption("Desenvolvido para automação de processos acadêmicos - Unidade ESAN.")

