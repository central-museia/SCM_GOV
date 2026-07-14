"""
Oportunidades

Licitações recomendadas para a SCM.

Autor: SCM Engenharia
"""

import streamlit as st
import pandas as pd

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Oportunidades | SCM_GOV",
    page_icon="⭐",
    layout="wide"
)

# ==============================================================================
# CABEÇALHO
# ==============================================================================

st.title("⭐ Oportunidades")

st.caption(
    "Licitações que merecem análise da SCM."
)

st.divider()

# ==============================================================================
# RESUMO
# ==============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Oportunidades",
        "0"
    )

with col2:
    st.metric(
        "Score Médio",
        "0"
    )

with col3:
    st.metric(
        "Órgãos",
        "0"
    )

with col4:
    st.metric(
        "Municípios",
        "0"
    )

st.divider()

# ==============================================================================
# FILTROS
# ==============================================================================

st.subheader("Filtros")

col1, col2, col3 = st.columns(3)

with col1:

    score = st.slider(
        "Score mínimo",
        min_value=0,
        max_value=100,
        value=70
    )

with col2:

    classificacao = st.selectbox(
        "Classificação",
        [
            "Todas",
            "Excelente",
            "Alta",
            "Média",
            "Baixa"
        ]
    )

with col3:

    municipio = st.selectbox(
        "Município",
        [
            "Todos",
            "Rio de Janeiro",
            "Niterói",
            "Duque de Caxias",
            "Nova Iguaçu",
            "Belford Roxo",
            "São João de Meriti",
            "Nilópolis",
            "Mesquita"
        ]
    )

st.divider()

# ==============================================================================
# TABELA
# ==============================================================================

st.subheader("Licitações Recomendadas")

colunas = [
    "Score",
    "Classificação",
    "Objeto",
    "Órgão",
    "Município",
    "Modalidade",
    "Prazo"
]

df = pd.DataFrame(columns=colunas)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.info(
    "Nenhuma oportunidade encontrada."
)

st.divider()

# ==============================================================================
# AÇÕES
# ==============================================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.button(
        "📑 Ver Detalhes",
        use_container_width=True,
        disabled=True
    )

with col2:

    st.button(
        "📤 Exportar Excel",
        use_container_width=True,
        disabled=True
    )

with col3:

    st.button(
        "🔄 Atualizar",
        use_container_width=True,
        disabled=True
    )

st.divider()

# ==============================================================================
# OBSERVAÇÕES
# ==============================================================================

st.subheader("Como funciona o Score SCM?")

st.write(
    """
As oportunidades apresentadas nesta página são classificadas
automaticamente com base nas regras definidas pela SCM,
considerando critérios como região de atuação,
compatibilidade com os serviços prestados e aderência
ao perfil da empresa.

O objetivo é facilitar a tomada de decisão sobre quais
licitações merecem investimento na preparação da proposta.
"""
)
