"""
Oportunidades

Licitações recomendadas para a SCM.

Autor: SCM Engenharia
"""

from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from api.contratacoes import consultar_todas_propostas
from api.parser import PNCPParser
from services.oportunidade_service import OportunidadeService
from services.exportacao_service import ExportacaoService

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
# CARREGAMENTO DE DADOS (PNCP + Score SCM)
# ==============================================================================

@st.cache_data(ttl=3600)
def carregar_oportunidades(dias=30):

    hoje = datetime.now()
    data_inicial = (hoje - timedelta(days=dias)).strftime("%Y%m%d")
    data_final = hoje.strftime("%Y%m%d")

    resposta = consultar_todas_propostas(
        data_inicial=data_inicial,
        data_final=data_final
    )

    if not resposta.get("success"):
        return [], resposta.get("message", "Erro ao consultar o PNCP.")

    brutos = resposta.get("data", [])

    normalizados = PNCPParser.parse_contratacoes(brutos)

    servico = OportunidadeService()

    for item in normalizados:

        analise = servico.analisar(item)

        item["score"] = analise["score"]
        item["classificacao"] = analise["classificacao"]
        item["oportunidade"] = analise["oportunidade"]
        item["motivos"] = ", ".join(analise["motivos"]) if analise["motivos"] else ""

    return normalizados, None


with st.spinner("Consultando oportunidades no PNCP..."):
    dados, erro = carregar_oportunidades()

if erro:
    st.warning(f"⚠️ Não foi possível consultar o PNCP agora: {erro}")

# Considera apenas o que o Score SCM classificou como oportunidade real
oportunidades = [item for item in dados if item.get("oportunidade")]

st.divider()

# ==============================================================================
# FILTROS
# ==============================================================================

st.subheader("Filtros")

col1, col2, col3 = st.columns(3)

with col1:

    score_min = st.slider(
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

    municipios_disponiveis = sorted({
        item.get("municipio", "")
        for item in oportunidades
        if item.get("municipio")
    })

    municipio = st.selectbox(
        "Município",
        ["Todos"] + municipios_disponiveis
    )

st.divider()

# ==============================================================================
# APLICAÇÃO DOS FILTROS
# ==============================================================================

filtrados = [
    item for item in oportunidades
    if item.get("score", 0) >= score_min
]

if classificacao != "Todas":
    filtrados = [
        item for item in filtrados
        if item.get("classificacao") == classificacao
    ]

if municipio != "Todos":
    filtrados = [
        item for item in filtrados
        if item.get("municipio") == municipio
    ]

# Ordena pelas melhores oportunidades primeiro
filtrados = sorted(
    filtrados,
    key=lambda item: item.get("score", 0),
    reverse=True
)

# ==============================================================================
# RESUMO
# ==============================================================================

total_oportunidades = len(filtrados)

score_medio = (
    round(sum(item.get("score", 0) for item in filtrados) / total_oportunidades, 1)
    if total_oportunidades else 0
)

orgaos_unicos = len({item.get("orgao") for item in filtrados if item.get("orgao")})

municipios_unicos = len({item.get("municipio") for item in filtrados if item.get("municipio")})

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Oportunidades", total_oportunidades)

with col2:
    st.metric("Score Médio", score_medio)

with col3:
    st.metric("Órgãos", orgaos_unicos)

with col4:
    st.metric("Municípios", municipios_unicos)

st.divider()

# ==============================================================================
# TABELA
# ==============================================================================

st.subheader("Licitações Recomendadas")

if not filtrados:

    st.info(
        "Nenhuma oportunidade encontrada com os filtros selecionados."
    )

else:

    tabela = pd.DataFrame([
        {
            "Score": item.get("score", 0),
            "Classificação": item.get("classificacao", ""),
            "Objeto": item.get("objeto", ""),
            "Órgão": item.get("orgao", ""),
            "Município": item.get("municipio", ""),
            "Modalidade": item.get("modalidade", ""),
            "Prazo": item.get("encerramento_proposta", ""),
            "Número PNCP": item.get("numero_pncp", ""),
        }
        for item in filtrados
    ])

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ==============================================================================
# AÇÕES
# ==============================================================================

col1, col2, col3 = st.columns(3)

with col1:

    numero_selecionado = st.selectbox(
        "Selecionar para ver detalhes",
        [item.get("numero_pncp") for item in filtrados] or ["-"],
        label_visibility="collapsed"
    )

    if st.button(
        "📑 Ver Detalhes",
        use_container_width=True,
        disabled=not filtrados
    ):
        st.session_state["licitacao_selecionada"] = next(
            (item for item in filtrados if item.get("numero_pncp") == numero_selecionado),
            None
        )
        st.switch_page("pages/04_📑_Detalhes.py")

with col2:

    if filtrados:

        caminho_excel = ExportacaoService.excel(
            filtrados,
            arquivo="oportunidades_scm.xlsx"
        )

        with open(caminho_excel, "rb") as arquivo:

            st.download_button(
                "📤 Exportar Excel",
                data=arquivo,
                file_name="oportunidades_scm.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    else:

        st.button(
            "📤 Exportar Excel",
            use_container_width=True,
            disabled=True
        )

with col3:

    if st.button(
        "🔄 Atualizar",
        use_container_width=True
    ):
        carregar_oportunidades.clear()
        st.rerun()

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
