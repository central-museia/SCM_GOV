"""
Dashboard SCM_GOV

Radar Estratégico de Licitações

Autor: SCM Engenharia
"""

import streamlit as st
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Dashboard | SCM_GOV",
    page_icon="🏠",
    layout="wide"
)

# ==============================================================================
# CABEÇALHO
# ==============================================================================

st.title("🏠 Dashboard")

st.caption("Radar Estratégico de Licitações Públicas")

st.divider()

# ==============================================================================
# INDICADORES
# ==============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🔍 Licitações Abertas",
        value="0"
    )

with col2:
    st.metric(
        label="⭐ Oportunidades SCM",
        value="0"
    )

with col3:
    st.metric(
        label="🏛️ Órgãos Encontrados",
        value="0"
    )

with col4:
    st.metric(
        label="📅 Atas Vigentes",
        value="0"
    )

st.divider()

# ==============================================================================
# GRÁFICOS
# ==============================================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 Licitações por Município")

    st.info(
        "Os dados serão exibidos após a primeira consulta ao PNCP."
    )

with col2:

    st.subheader("📈 Licitações por Modalidade")

    st.info(
        "Os dados serão exibidos após a primeira consulta ao PNCP."
    )

st.divider()

# ==============================================================================
# RANKINGS
# ==============================================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏛️ Órgãos que mais publicam")

    st.info(
        "Nenhum dado disponível."
    )

with col2:

    st.subheader("⭐ Ranking Score SCM")

    st.info(
        "Nenhum dado disponível."
    )

st.divider()

# ==============================================================================
# RESUMO
# ==============================================================================

st.subheader("📌 Resumo")

st.write(
    """
O SCM_GOV consulta o Portal Nacional de Contratações Públicas (PNCP)
e organiza as licitações abertas para apoiar a decisão da SCM Engenharia
sobre quais oportunidades merecem investimento na preparação de propostas.
"""
)

# ==============================================================================
# STATUS
# ==============================================================================

st.divider()

col1, col2 = st.columns([3, 1])

with col1:

    st.success("Sistema inicializado com sucesso.")

with col2:

    st.caption(
        f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
