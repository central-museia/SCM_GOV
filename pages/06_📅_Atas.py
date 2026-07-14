"""
Atas de Registro de Preços

Consulta de Atas do PNCP.

Autor: SCM Engenharia
"""

from datetime import date

import pandas as pd
import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Atas de Registro | SCM_GOV",
    page_icon="📅",
    layout="wide"
)

# ==============================================================================
# CABEÇALHO
# ==============================================================================

st.title("📅 Atas de Registro de Preços")

st.caption(
    "Consulte Atas de Registro de Preços vigentes publicadas no PNCP."
)

st.divider()

# ==============================================================================
# FILTROS
# ==============================================================================

st.subheader("Filtros")

col1, col2, col3 = st.columns(3)

with col1:

    data_inicial = st.date_input(
        "Vigência Inicial",
        value=date.today().replace(day=1)
    )

with col2:

    data_final = st.date_input(
        "Vigência Final",
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

    adesao = st.selectbox(
        "Possui Adesão",
        [
            "Todos",
            "Sim",
            "Não"
        ]
    )

st.divider()

# ==============================================================================
# CONSULTA
# ==============================================================================

if st.button(
    "📅 Consultar Atas",
    use_container_width=True
):

    with st.spinner("Consultando Atas de Registro de Preços..."):

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
        "Atas Encontradas",
        "0"
    )

with col2:

    st.metric(
        "Com Adesão",
        "0"
    )

with col3:

    st.metric(
        "Órgãos",
        "0"
    )

with col4:

    st.metric(
        "Vigentes",
        "0"
    )

st.divider()

# ==============================================================================
# RESULTADOS
# ==============================================================================

st.subheader("Atas Localizadas")

df = pd.DataFrame(
    columns=[
        "Ata",
        "Ano",
        "Órgão",
        "Município",
        "Objeto",
        "Início",
        "Fim",
        "Adesão"
    ]
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.info(
    "Nenhuma Ata encontrada."
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

st.subheader("Sobre as Atas de Registro de Preços")

st.write(
    """
As Atas de Registro de Preços permitem acompanhar contratações
já realizadas pelos órgãos públicos e identificar oportunidades
de adesão, quando previstas.

As informações são obtidas diretamente do Portal Nacional de
Contratações Públicas (PNCP).
"""
)
