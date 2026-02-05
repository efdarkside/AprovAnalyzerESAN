import streamlit as st
import os
from agents import diretor_coordenacao
from knowledge import knowledge_base, inicializar_base
from utils import extrair_texto_pdf

st.set_page_config(page_title="AprovAnalyzer ESAN", layout="wide")

# --- LÓGICA DE AUTO-INDEXAÇÃO ---
# Verifica se a base já foi carregada nesta sessão ou se a pasta existe no disco
if 'base_pronta' not in st.session_state:
    db_path = os.path.join(os.path.dirname(__file__), "data/lancedb/ementas_federais.lance")
    if not os.path.exists(db_path):
        with st.spinner("🤖 Inicializando sistema e carregando ementas da ESAN..."):
            sucesso = inicializar_base()
            if sucesso:
                st.session_state['base_pronta'] = True
            else:
                st.error("Erro ao carregar base automática.")
    else:
        st.session_state['base_pronta'] = True

st.title("🏛️ Sistema de Aproveitamento de Estudos - ESAN")
st.markdown("---")

# Sidebar simplificada
with st.sidebar:
    st.header("⚙️ Status do Sistema")
    if st.session_state.get('base_pronta'):
        st.success("✅ Base de Ementas Ativa")
    else:
        st.warning("⚠️ Base em carregamento...")
    
    if st.button("🔄 Forçar Reindexação"):
        with st.spinner("Reindexando base de dados..."):
            inicializar_base()
            st.success("Base atualizada!")

# Interface Principal
st.subheader("Análise de Estudante")
st.info("Suba o ementário externo para comparar com a base da ESAN.")

uploaded_file = st.file_uploader("Escolher arquivo PDF", type="pdf")

if uploaded_file:
    if st.button("🔍 Iniciar Comparação Acadêmica"):
        with st.spinner("Os agentes estão analisando... Isso pode levar até 1 minuto."):
            try:
                # Extração do texto
                texto_estudante = extrair_texto_pdf(uploaded_file)
                
                # Execução da equipe de agentes (RAG)
                prompt = f"Realize a análise de aproveitamento para este conteúdo: {texto_estudante}"
                response = diretor_coordenacao.run(prompt)
                
                st.markdown("### 📋 Resultado da Análise Multiagente")
                st.markdown(response.content)
            except Exception as e:
                st.error(f"Erro no processamento: {e}")
                st.info("Dica: Tente clicar em 'Forçar Reindexação' na barra lateral.")

st.markdown("---")
st.caption("AprovAnalyzer v1.1 - ESAN/UFMS")
