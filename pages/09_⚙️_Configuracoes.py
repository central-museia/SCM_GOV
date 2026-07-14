"""
Configurações

Preferências do SCM_GOV.

Autor: SCM Engenharia
"""

import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Configurações | SCM_GOV",
    page_icon="⚙️",
    layout="wide"
)

# ==============================================================================
# CABEÇALHO
# ==============================================================================

st.title("⚙️ Configurações")

st.caption(
    "Personalize o funcionamento do SCM_GOV."
)

st.divider()

# ==============================================================================
# CONSULTAS
# ==============================================================================

st.subheader("🔍 Consultas")

col1, col2 = st.columns(2)

with col1:

    dias_consulta = st.number_input(
        "Período padrão da consulta (dias)",
        min_value=1,
        max_value=365,
        value=30
    )

with col2:

    atualizar = st.checkbox(
        "Atualizar automaticamente ao abrir o sistema",
        value=False
    )

st.divider()

# ==============================================================================
# REGIÃO DE ATUAÇÃO
# ==============================================================================

st.subheader("📍 Região de Atuação")

municipios = st.multiselect(

    "Municípios monitorados",

    [
        "Rio de Janeiro",
        "Niterói",
        "Duque de Caxias",
        "Nova Iguaçu",
        "São João de Meriti",
        "Belford Roxo",
        "Nilópolis",
        "Mesquita"
    ],

    default=[
        "Rio de Janeiro",
        "Niterói"
    ]
)

st.divider()

# ==============================================================================
# SCORE SCM
# ==============================================================================

st.subheader("⭐ Score SCM")

score = st.slider(

    "Score mínimo para considerar oportunidade",

    min_value=0,

    max_value=100,

    value=70
)

st.divider()

# ==============================================================================
# CNAES
# ==============================================================================

st.subheader("🏗️ CNAEs")

st.info(
    "Os CNAEs são carregados automaticamente do arquivo assets/cnaes.json."
)

st.divider()

# ==============================================================================
# PALAVRAS-CHAVE
# ==============================================================================

st.subheader("🔑 Palavras-chave")

st.info(
    "As palavras-chave são carregadas automaticamente do arquivo assets/palavras_chave.json."
)

st.divider()

# ==============================================================================
# EXPORTAÇÃO
# ==============================================================================

st.subheader("📤 Exportação")

formato = st.selectbox(

    "Formato padrão",

    [
        "Excel (.xlsx)",
        "CSV (.csv)",
        "JSON (.json)"
    ]
)

st.divider()

# ==============================================================================
# SOBRE
# ==============================================================================

st.subheader("ℹ️ Sobre")

st.write(
    """
**SCM_GOV**

Radar Estratégico de Licitações Públicas.

Sistema desenvolvido para apoiar a SCM Engenharia
na identificação de oportunidades em licitações públicas,
utilizando os dados do Portal Nacional de Contratações Públicas (PNCP).
"""
)

st.divider()

# ==============================================================================
# BOTÕES
# ==============================================================================

col1, col2 = st.columns(2)

with col1:

    st.button(
        "💾 Salvar Configurações",
        use_container_width=True,
        disabled=True
    )

with col2:

    st.button(
        "🔄 Restaurar Padrões",
        use_container_width=True,
        disabled=True
    )
