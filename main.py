import streamlit as st
from knowledge import knowledge_base
from agents import diretor_coordenacao
from utils import extrair_texto_pdf
import os

st.sidebar.title("Configurações do Sistema")
if st.sidebar.button("Atualizar Base de Ementas (Admin)"):
    with st.spinner("Lendo PDFs e indexando no LanceDB..."):
        knowledge_base.load(recreate=True)
        st.sidebar.success("Base de dados atualizada!")

st.set_page_config(page_title="Automação de Aproveitamento de Estudos ESAN", layout="wide")

st.title("🏛️ Sistema de Análise de Aproveitamento de Estudos da ESAN")
st.subheader("Coordenação de Curso de Graduação - Universidade Federal de Mato Grosso do Sul")

col1, col2 = st.columns(2)

with col1:
    st.info("Ementário da Disciplina Interna")
    file_interno = st.file_uploader("Upload PDF (ESAN)", type="pdf", key="interno")

with col2:
    st.info("Ementário do Estudante (Externo)")
    file_externo = st.file_uploader("Upload PDF (Estudante)", type="pdf", key="externo")

if st.button("Iniciar Análise Multiagente"):
    if file_interno and file_externo:
        with st.spinner("Agentes trabalhando na análise..."):
            # Extração simples para passar aos agentes
            texto_interno = extrair_texto_pdf(file_interno)
            texto_externo = extrair_texto_pdf(file_externo)

            # Input para o Agente Diretor iniciar a cadeia
            prompt = f"""
            Analise o pedido de aproveitamento:
            CONTEÚDO INTERNO (REFERÊNCIA): {texto_interno}
            CONTEÚDO EXTERNO (SOLICITADO): {texto_externo}

            Por favor, passe pela anonimização, verifique a similaridade e dê o veredito.
            """

            response = diretor_coordenacao.run(prompt)
            st.markdown(response.content)
    else:

        st.error("Por favor, faça o upload de ambos os arquivos.")
