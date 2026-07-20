"""
SCM_GOV
Radar Estratégico de Licitações Públicas
Autor: Deise Maria de Oliveira a serviço da SCM Engenharia
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.getcwd()))

import streamlit as st
from database.migrations import inicializar_banco

from api.contratacoes import propostas_abertas
from api.parser import PNCPParser
from services.estatistica_service import EstatisticaService
from services.oportunidade_service import OportunidadeService

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="SCM_GOV",
    page_icon="assets/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

inicializar_banco()

# ==============================================================================
# LÓGICA DE DADOS
# ==============================================================================

@st.cache_data(ttl=3600)
def obter_dados_do_pncp():

    hoje = datetime.now().strftime("%Y%m%d")
    inicio = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")

    resposta = propostas_abertas(data_inicial=inicio, data_final=hoje)

    if not resposta.get("success"):
        return [], resposta.get("message", "Erro desconhecido ao consultar o PNCP.")

    # O array real de licitações está em resposta["data"]["data"]
    brutos = resposta["data"].get("data", [])

    # Normaliza os campos (objetoCompra -> objeto, unidadeOrgao -> municipio, etc.)
    normalizados = PNCPParser.parse_contratacoes(brutos)

    # Calcula score / classificação / oportunidade para cada licitação
    servico_oportunidade = OportunidadeService()

    for item in normalizados:
        analise = servico_oportunidade.analisar(item)
        item["score"] = analise["score"]
        item["classificacao"] = analise["classificacao"]
        item["oportunidade"] = analise["oportunidade"]

    return normalizados, None


dados_scm, erro = obter_dados_do_pncp()

if erro:
    st.warning(f"⚠️ Não foi possível consultar o PNCP agora: {erro}")

resumo = EstatisticaService.resumo(dados_scm) if dados_scm else {}

# ==============================================================================
# INDICADORES
# ==============================================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔍 Licitações Abertas", resumo.get("total", 0))
with col2:
    st.metric("⭐ Oportunidades", resumo.get("oportunidades", 0))
with col3:
    st.metric("🏛️ Órgãos", len(resumo.get("orgaos", {})))
with col4:
    st.metric("📅 Score Médio", resumo.get("score_medio", 0))

# ==============================================================================
# VISÃO GERAL
# ==============================================================================

st.markdown("## 📊 Visão Geral")

st.markdown(
    """
<div class="card">

O SCM_GOV consulta automaticamente os dados oficiais do Portal Nacional
de Contratações Públicas (PNCP) e organiza as oportunidades para apoiar
a tomada de decisão da SCM.

O objetivo do sistema não é gerenciar licitações, mas responder uma
pergunta estratégica:

<b>Quais licitações abertas merecem que a SCM invista tempo na preparação
de uma proposta?</b>

</div>
""",
    unsafe_allow_html=True
)

# ... (o restante do arquivo — Módulos, Roadmap, Rodapé — pode ficar exatamente como está)
