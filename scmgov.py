"""
SCM_GOV
Radar Estratégico de Licitações Públicas
Autor: Deise Maria de Oliveira a serviço da SCM Engenharia
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Garante que o Python encontre as pastas locais
sys.path.insert(0, os.path.abspath(os.getcwd()))

import streamlit as st
from database.migrations import inicializar_banco

# IMPORTAÇÃO EXATA DAS SUAS FUNÇÕES
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
# LÓGICA DE DADOS (Chamada direta às suas funções)
# ==============================================================================
@st.cache_data(ttl=3600)
def obter_dados_do_pncp():
    # Define o período (ex: últimos 30 dias)
    hoje = datetime.now().strftime("%Y%m%d")
    inicio = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
    
    # CHAMADA DIRETA DA SUA FUNÇÃO ORIGINAL
    return propostas_abertas(data_inicial=inicio, data_final=hoje)

# Carrega os dados brutos da sua função
dados_brutos = obter_dados_do_pncp()

# Processa com seu serviço de estatística
resumo = EstatisticaService.resumo(dados_brutos) if dados_brutos else {}

# ==============================================================================
# INDICADORES (Usando as chaves do seu EstatisticaService)
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
