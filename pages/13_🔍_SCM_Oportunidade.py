"""
SCM_GOV
Licitações em Aberto
"""

import streamlit as st
import pandas as pd

from services.consulta_service import consultar_licitacoes

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="SCM_GOV | Licitações",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Licitações em Aberto")

st.caption("Licitações abertas encontradas no Portal Nacional de Contratações Públicas")

st.divider()

# ==============================================================================
# FILTROS
# ==============================================================================

col1, col2, col3 = st.columns(3)

with col1:
    estado = st.selectbox(
        "Estado",
        [
            "RJ"
        ]
    )

with col2:
    palavra = st.text_input(
        "Palavra-chave",
        placeholder="ex: reforma"
    )

with col3:
    quantidade = st.number_input(
        "Quantidade",
        min_value=10,
        max_value=500,
        value=50,
        step=10
    )

# ==============================================================================
# BOTÃO
# ==============================================================================

if st.button("🔍 Buscar Licitações", use_container_width=True):

    with st.spinner("Consultando PNCP..."):

        df = consultar_licitacoes(
            estado=estado,
            palavra_chave=palavra,
            quantidade=quantidade
        )

    if df.empty:

        st.warning("Nenhuma licitação encontrada.")

    else:

        st.success(f"{len(df)} licitações encontradas.")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
