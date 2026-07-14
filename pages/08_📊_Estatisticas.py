"""
Estatísticas

Indicadores e gráficos das licitações consultadas.

Autor: SCM Engenharia
"""

import pandas as pd
import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Estatísticas | SCM_GOV",
    page_icon="📊",
    layout="wide"
)

# ==============================================================================
# CABEÇALHO
# ==============================================================================

st.title("📊 Estatísticas")

st.caption(
    "Indicadores gerenciais das consultas realizadas no PNCP."
)

st.divider()

# ==============================================================================
# INDICADORES
# ==============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Licitações",
        "0"
    )

with col2:
    st.metric(
        "Oportunidades",
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
# GRÁFICOS
# ==============================================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📍 Licitações por Município")

    st.info(
        "Os dados serão exibidos após a primeira consulta."
    )

with col2:

    st.subheader("🏛️ Licitações por Órgão")

    st.info(
        "Os dados serão exibidos após a primeira consulta."
    )

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("📋 Licitações por Modalidade")

    st.info(
        "Os dados serão exibidos após a primeira consulta."
    )

with col2:

    st.subheader("⭐ Distribuição do Score SCM")

    st.info(
        "Os dados serão exibidos após a primeira consulta."
    )

st.divider()

# ==============================================================================
# TABELA RESUMO
# ==============================================================================

st.subheader("Resumo Geral")

df = pd.DataFrame(
    columns=[
        "Indicador",
        "Quantidade"
    ]
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.info(
    "Nenhum indicador disponível."
)

st.divider()

# ==============================================================================
# AÇÕES
# ==============================================================================

col1, col2 = st.columns(2)

with col1:

    st.button(
        "🔄 Atualizar",
        use_container_width=True,
        disabled=True
    )

with col2:

    st.button(
        "📤 Exportar Estatísticas",
        use_container_width=True,
        disabled=True
    )

st.divider()

# ==============================================================================
# INFORMAÇÕES
# ==============================================================================

st.subheader("Sobre as Estatísticas")

st.write(
    """
Esta página consolida os principais indicadores das consultas realizadas
ao Portal Nacional de Contratações Públicas (PNCP).

As estatísticas auxiliam a SCM na identificação de padrões de contratação,
municípios com maior volume de oportunidades, órgãos mais ativos e
distribuição das licitações por modalidade, apoiando o planejamento
estratégico da empresa.
"""
)
