"""
Órgãos Públicos

Informações sobre os órgãos contratantes.

Autor: SCM Engenharia
"""

import pandas as pd
import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Órgãos | SCM_GOV",
    page_icon="🏛️",
    layout="wide"
)

# ==============================================================================
# CABEÇALHO
# ==============================================================================

st.title("🏛️ Órgãos Públicos")

st.caption(
    "Consulte os órgãos públicos que possuem licitações abertas."
)

st.divider()

# ==============================================================================
# INDICADORES
# ==============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Órgãos Encontrados",
        "0"
    )

with col2:
    st.metric(
        "Licitações",
        "0"
    )

with col3:
    st.metric(
        "Municípios",
        "0"
    )

with col4:
    st.metric(
        "Atas",
        "0"
    )

st.divider()

# ==============================================================================
# FILTROS
# ==============================================================================

st.subheader("Filtros")

col1, col2 = st.columns(2)

with col1:

    orgao = st.text_input(
        "Nome do Órgão",
        placeholder="Digite parte do nome..."
    )

with col2:

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

st.subheader("Órgãos Contratantes")

df = pd.DataFrame(
    columns=[
        "Órgão",
        "CNPJ",
        "Município",
        "UF",
        "Licitações",
        "Atas"
    ]
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.info(
    "Nenhum órgão encontrado."
)

st.divider()

# ==============================================================================
# RANKING
# ==============================================================================

st.subheader("Ranking dos Órgãos")

st.info(
    "O ranking será exibido após a primeira consulta ao PNCP."
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
        "📤 Exportar",
        use_container_width=True,
        disabled=True
    )

st.divider()

# ==============================================================================
# OBSERVAÇÕES
# ==============================================================================

st.subheader("Sobre esta página")

st.write(
    """
Esta página apresenta os órgãos públicos identificados nas consultas
realizadas ao Portal Nacional de Contratações Públicas (PNCP).

As informações auxiliam a SCM na identificação dos órgãos
que mais publicam oportunidades relacionadas aos seus serviços.
"""
)
