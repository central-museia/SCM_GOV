"""
Radar de Licitações

Responsável pela consulta de licitações abertas no PNCP.

Autor: SCM Engenharia
"""

from datetime import date

import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Radar de Licitações | SCM_GOV",
    page_icon="🔍",
    layout="wide"
)

# ==============================================================================
# CABEÇALHO
# ==============================================================================

st.title("🔍 Radar de Licitações")

st.caption(
    "Consulte as licitações públicas abertas e identifique oportunidades para a SCM."
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
            "São João de Meriti",
            "Belford Roxo",
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

    modalidade = st.selectbox(
        "Modalidade",
        [
            "Todas",
            "Pregão",
            "Concorrência",
            "Dispensa",
            "Inexigibilidade"
        ]
    )

st.divider()

# ==============================================================================
# CONSULTA
# ==============================================================================

if st.button(
    "🔍 Pesquisar Licitações",
    use_container_width=True
):

    with st.spinner("Consultando o Portal Nacional de Contratações Públicas..."):

        # Aqui será chamada futuramente a ConsultaService
        # resultado = ConsultaService.licitacoes(...)

        st.success("Consulta realizada com sucesso!")

        st.info(
            "Integração com a API do PNCP será implementada na próxima etapa."
        )

st.divider()

# ==============================================================================
# RESULTADOS
# ==============================================================================

st.subheader("Resultados")

st.info(
    "Nenhuma consulta realizada."
)

# Futuramente será utilizado:
#
# st.dataframe(...)
#
# contendo:
#
# Número
# Objeto
# Município
# Órgão
# Modalidade
# Score SCM
# Situação
# Botão Detalhes

st.divider()

# ==============================================================================
# RESUMO
# ==============================================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Licitações Encontradas",
        "0"
    )

with col2:

    st.metric(
        "Oportunidades SCM",
        "0"
    )

with col3:

    st.metric(
        "Órgãos Encontrados",
        "0"
    )
