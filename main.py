import streamlit as st
import os
from agents import diretor_coordenacao
from knowledge import knowledge_base
from utils import extrair_texto_pdf

st.set_page_config(page_title="AprovAnalyzer ESAN", layout="wide")

st.title("🏛️ Sistema de Aproveitamento de Estudos - ESAN")
st.markdown("---")

# Sidebar para administração da base
with st.sidebar:
    st.header("Painel Administrativo")
    if st.button("🔄 Atualizar Base de Ementas"):
        with st.spinner("Indexando PDFs no LanceDB..."):
            knowledge_base.load(recreate=True)
            st.success("Base atualizada!")

# Área principal de upload do estudante
st.info("Suba aqui o ementário enviado pelo estudante para análise.")
uploaded_file = st.file_uploader("Escolher arquivo PDF", type="pdf")

if uploaded_file:
    if st.button("🚀 Iniciar Análise Multiagente"):
        with st.spinner("Os agentes estão analisando os documentos..."):
            # Extração do texto do PDF enviado
            texto_estudante = extrair_texto_pdf(uploaded_file)
            
            # Execução da equipe de agentes
            prompt = f"Analise este pedido de aproveitamento vindo de outra instituição: {texto_estudante}"
            response = diretor_coordenacao.run(prompt)
            
            st.markdown("### 📋 Parecer Final da Coordenação")
            st.markdown(response.content)

st.markdown("---")
st.caption("Desenvolvido para automação de processos acadêmicos - Universidade Federal.")
