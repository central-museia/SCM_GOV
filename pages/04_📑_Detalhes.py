"""
Detalhes da Licitação

Análise completa da oportunidade.

Autor: SCM Engenharia
"""

import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Detalhes | SCM_GOV",
    page_icon="📑",
    layout="wide"
)

# ==============================================================================
# CABEÇALHO
# ==============================================================================

st.title("📑 Detalhes da Licitação")

st.caption(
    "Análise completa da oportunidade selecionada."
)

st.divider()

# ==============================================================================
# DADOS GERAIS
# ==============================================================================

st.subheader("Informações Gerais")

col1, col2 = st.columns(2)

with col1:

    st.text_input(
        "Número da Licitação",
        value="",
        disabled=True
    )

    st.text_input(
        "Órgão",
        value="",
        disabled=True
    )

    st.text_input(
        "Município",
        value="",
        disabled=True
    )

    st.text_input(
        "Modalidade",
        value="",
        disabled=True
    )

with col2:

    st.text_input(
        "Data de Publicação",
        value="",
        disabled=True
    )

    st.text_input(
        "Prazo Final",
        value="",
        disabled=True
    )

    st.text_input(
        "Valor Estimado",
        value="",
        disabled=True
    )

    st.text_input(
        "Situação",
        value="",
        disabled=True
    )

st.divider()

# ==============================================================================
# OBJETO
# ==============================================================================

st.subheader("Objeto da Contratação")

st.text_area(
    "",
    value="",
    height=180,
    disabled=True
)

st.divider()

# ==============================================================================
# SCORE SCM
# ==============================================================================

st.subheader("Score SCM")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Score",
        "0"
    )

with col2:

    st.metric(
        "Classificação",
        "-"
    )

with col3:

    st.metric(
        "Recomendação",
        "-"
    )

st.divider()

# ==============================================================================
# DOCUMENTOS
# ==============================================================================

st.subheader("Documentos")

st.info(
    "Os documentos da contratação serão exibidos nesta área."
)

st.divider()

# ==============================================================================
# OBSERVAÇÕES SCM
# ==============================================================================

st.subheader("Observações")

st.text_area(
    "Anotações da análise",
    value="",
    height=180
)

st.divider()

# ==============================================================================
# AÇÕES
# ==============================================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.button(
        "⬅️ Voltar",
        use_container_width=True
    )

with col2:

    st.button(
        "📤 Exportar",
        use_container_width=True,
        disabled=True
    )

with col3:

    st.button(
        "🔄 Atualizar Dados",
        use_container_width=True,
        disabled=True
    )
