"""
SCM_GOV
Radar Estratégico de Licitações Públicas
Autor: Deise Maria de Oliveira a serviço da SCM Engenharia
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Adiciona o caminho absoluto da pasta raiz
sys.path.insert(0, os.path.abspath(os.getcwd()))

import streamlit as st
from database.migrations import inicializar_banco
from api.contratacoes import propostas_abertas
from services.estatistica_service import EstatisticaService

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
# LÓGICA DE DADOS (Integração Direta)
# ==============================================================================
@st.cache_data(ttl=3600)
def carregar_dados_reais():
    # Define o período da busca (ex: últimos 30 dias)
    hoje = datetime.now()
    inicio = (hoje - timedelta(days=30)).strftime("%Y%m%d")
    fim = hoje.strftime("%Y%m%d")
    
    # Busca dados usando a função importada corretamente
    dados_brutos = propostas_abertas(data_inicial=inicio, data_final=fim)
    
    # Processa via EstatisticaService
    if dados_brutos:
        return EstatisticaService.resumo(dados_brutos)
    return None

resumo = carregar_dados_reais()

# Fallback
if not resumo:
    resumo = {"total": 0, "oportunidades": 0, "orgaos": {}, "score_medio": 0}

# ==============================================================================
# CARREGAR CSS
# ==============================================================================
def carregar_css():
    css_path = Path("assets/styles.css")
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

carregar_css()

# ==============================================================================
# CABEÇALHO
# ==============================================================================
st.markdown("<div class='titulo'>🏛️ SCM_GOV</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>Radar Estratégico de Licitações Públicas</div>", unsafe_allow_html=True)
st.write("Identifique rapidamente quais licitações abertas merecem que a SCM Reformas e Engenharia invista tempo na preparação de uma proposta.")
st.divider()

# ==============================================================================
# INDICADORES (Dinâmicos)
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

# ==============================================================================
# MÓDULOS
# ==============================================================================

st.markdown("## 🚀 Módulos da Plataforma")

col1, col2, col3 = st.columns(3)

with col1:

    st.info("""
### 🔍 Radar de Licitações

Consulta das oportunidades abertas no PNCP.
""")

    st.info("""
### ⭐ Oportunidades

Classificação automática utilizando o Score SCM.
""")

    st.info("""
### 📑 Detalhes

Análise completa de cada licitação.
""")

with col2:

    st.info("""
### 🏛️ Órgãos

Órgãos públicos contratantes.
""")

    st.info("""
### 📅 Atas de Registro

Consulta das Atas vigentes.
""")

    st.info("""
### 📋 Contratos

Consulta de contratos públicos.
""")

with col3:

    st.info("""
### 📊 Estatísticas

Indicadores e gráficos.
""")

    st.info("""
### ⚙️ Configurações

Preferências da plataforma.
""")

    st.info("""
### 🤖 Inteligência SCM

Filtros inteligentes, Score SCM e futuras análises por IA.
""")

# ==============================================================================
# ROADMAP
# ==============================================================================

st.markdown("## 🛣️ Roadmap")

st.progress(20)

st.markdown("""
- ✅ Estrutura do projeto

- 🔄 Integração com a API do PNCP

- 🔄 Implementação do Radar de Licitações

- 🔄 Score SCM

- 🔄 Dashboard Inteligente

- ⏳ Inteligência Artificial
""")

# ==============================================================================
# RODAPÉ
# ==============================================================================

st.divider()

st.markdown(
    """
<div class='footer'>

SCM_GOV • Radar Estratégico de Licitações Públicas

Versão 1.0.0

Desenvolvido para SCM Reformas e Engenharia

</div>
""",
    unsafe_allow_html=True
)
