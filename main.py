import streamlit as st
import os
from agents import diretor_coordenacao
from knowledge import knowledge_base, inicializar_base
from utils import extrair_texto_pdf

st.set_page_config(page_title="AprovAnalyzer ESAN", layout="wide")

st.title("🏛️ Sistema de Aproveitamento de Estudos - ESAN")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuração")
    st.warning("⚠️ Na primeira vez que usar após o deploy, clique no botão abaixo.")
    if st.button("🔄 Indexar Ementas da ESAN"):
        with st.spinner("Lendo arquivos da universidade..."):
            sucesso = inicializar_base()
            if sucesso:
                st.success("Base de dados pronta para uso!")
            else:
                st.error("Falha ao carregar ementários. Verifique a pasta no GitHub.")

# Interface Principal
st.subheader("Análise de Estudante")
uploaded_file = st.file_uploader("Suba o PDF do estudante aqui", type="pdf")

if uploaded_file:
    if st.button("🔍 Iniciar Comparação Acadêmica"):
        # Verificação se o banco existe (evita erro 502 por busca em vazio)
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "data/lancedb")):
            st.error("O banco de dados está vazio. Clique em 'Indexar Ementas' na lateral primeiro!")
        else:
            with st.spinner("Os agentes estão comparando as ementas... Isso pode levar até 1 minuto."):
                try:
                    texto_estudante = extrair_texto_pdf(uploaded_file)
                    
                    # Chamada dos agentes
                    prompt = f"Realize a análise de aproveitamento para este conteúdo: {texto_estudante}"
                    response = diretor_coordenacao.run(prompt)
                    
                    st.markdown("### 📋 Resultado da Análise Multiagente")
                    st.markdown(response.content)
                except Exception as e:
                    st.error(f"Erro no processamento: {e}")
                    st.info("Dica: Tente indexar a base novamente na barra lateral.")

st.markdown("---")
st.caption("AprovAnalyzer v1.0 - ESAN/UFMS")
