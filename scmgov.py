"""
SCM_GOV

Radar Estratégico de Licitações Públicas

Autor: SCM Engenharia
"""

from pathlib import Path

import streamlit as st

from database.migrations import inicializar_banco

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================

st.set_page_config(
    page_title="SCM_GOV",
    page_icon="assets/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# INICIALIZAÇÃO DO SISTEMA
# ==============================================================================

inicializar_banco()

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

st.markdown(
    "<div class='titulo'>🏛️ SCM_GOV</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class='subtitulo'>
Radar Estratégico de Licitações Públicas
</div>
""",
    unsafe_allow_html=True
)

st.write(
    """
Identifique rapidamente quais licitações abertas merecem que a
SCM Reformas e Engenharia invista tempo na preparação de uma proposta.
"""
)

st.divider()

# ==============================================================================
# INDICADORES
# ==============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔍 Licitações Abertas", "0")

with col2:
    st.metric("⭐ Oportunidades", "0")

with col3:
    st.metric("🏛️ Órgãos", "0")

with col4:
    st.metric("📅 Atas Vigentes", "0")

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
