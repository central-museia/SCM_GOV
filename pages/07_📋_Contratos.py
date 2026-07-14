"""
Contratos Públicos

Consulta de contratos publicados no PNCP.

Autor: SCM Engenharia
"""

from datetime import date

import pandas as pd
import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Contratos | SCM_GOV",
    page_icon="📋",
    layout="wide"
)

# ==============================================================================
# CABEÇALHO
# ==============================================================================

st.title("📋 Contratos Públicos")

st.caption(
    "Consulte contratos e empenhos publicados no Portal Nacional de Contratações Públicas."
)

st.divider()

# ==============================================================================
# FILTROS
# ==============================================================================

st.subheader("Filtros")

col1, col2, col3 = st.columns(3)

with col1:

    data_inicial = st.date_input(
        "Data Inicial",
        value=date.today().replace(day=1)
    )

with col2:

    data_final = st.date_input(
        "Data Final",
        value=date.today()
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

col1, col2 = st.columns(2)

with col1:

    palavra = st.text_input(
        "Palavra-chave",
        placeholder="Ex.: reforma, fachada, pintura..."
    )

with col2:

    situacao = st.selectbox(
        "Situação",
        [
            "Todas",
            "Vigente",
            "Encerrado"
        ]
    )

st.divider()

# ==============================================================================
# CONSULTA
# ==============================================================================

if st.button(
    "📋 Consultar Contratos",
    use_container_width=True
):

    with st.spinner("Consultando contratos no PNCP..."):

        st.success("Consulta realizada com sucesso!")

        st.info(
            "A integração com a API do PNCP será implementada na próxima etapa."
        )

st.divider()

# ==============================================================================
# INDICADORES
# ==============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Contratos",
        "0"
    )

with col2:

    st.metric(
        "Órgãos",
        "0"
    )

with col3:

    st.metric(
        "Municípios",
        "0"
    )

with col4:

    st.metric(
        "Valor Total",
        "R$ 0,00"
    )

st.divider()

# ==============================================================================
# RESULTADOS
# ==============================================================================

st.subheader("Contratos Encontrados")

df = pd.DataFrame(
    columns=[
        "Contrato",
        "Órgão",
        "Município",
        "Fornecedor",
        "Objeto",
        "Valor",
        "Início",
        "Fim",
        "Situação"
    ]
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.info(
    "Nenhum contrato encontrado."
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
# INFORMAÇÕES
# ==============================================================================

st.subheader("Sobre os Contratos")

st.write(
    """
Esta página apresenta contratos e empenhos publicados pelos órgãos públicos
no Portal Nacional de Contratações Públicas (PNCP).

A consulta permite conhecer o histórico de contratações, valores praticados
e fornecedores contratados, auxiliando a SCM na análise do mercado e na
preparação de propostas futuras.
"""
)
