from pathlib import Path
import streamlit as st

def carregar_css():
    css = Path("assets/styles.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

carregar_css()

st.set_page_config(
    page_title="SCM_GOV",
    page_icon="assets/favicon.ico",
    layout="wide"
)

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="SCM_GOV",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CSS
# -----------------------------------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.titulo {
    font-size:42px;
    font-weight:700;
    color:#0B5394;
}

.subtitulo{
    font-size:20px;
    color:#666666;
}

.card{
    background-color:#F8F9FA;
    border-radius:12px;
    padding:20px;
    border-left:6px solid #0B5394;
    box-shadow:0px 2px 6px rgba(0,0,0,.08);
    margin-bottom:15px;
}

.big{
    font-size:34px;
    font-weight:bold;
    color:#0B5394;
}

.metric{
    text-align:center;
    background:#FFFFFF;
    border-radius:12px;
    padding:20px;
    border:1px solid #DDDDDD;
}

.footer{
    text-align:center;
    color:gray;
    font-size:13px;
    margin-top:40px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CABEÇALHO
# -----------------------------------------------------------------------------

st.markdown(
    "<div class='titulo'>🏛️ SCM_GOV</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitulo'>Plataforma de Inteligência para Licitações Públicas</div>",
    unsafe_allow_html=True
)

st.divider()

# -----------------------------------------------------------------------------
# MÉTRICAS (temporárias)
# -----------------------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Licitações Abertas", "0")

with col2:
    st.metric("Atas Vigentes", "0")

with col3:
    st.metric("Contratos", "0")

with col4:
    st.metric("Órgãos Monitorados", "0")

st.write("")

# -----------------------------------------------------------------------------
# VISÃO GERAL
# -----------------------------------------------------------------------------

st.markdown("## 📊 Visão Geral")

st.markdown("""
<div class="card">

O SCM_GOV foi desenvolvido para apoiar a SCM Reformas e Engenharia na
identificação, análise e priorização de oportunidades em licitações públicas.

A plataforma utilizará dados oficiais do Portal Nacional de Contratações Públicas (PNCP)
para transformar informações públicas em inteligência para tomada de decisão.

</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MÓDULOS
# -----------------------------------------------------------------------------

st.markdown("## 🚀 Módulos da Plataforma")

c1, c2, c3 = st.columns(3)

with c1:

    st.info("""
### 🔍 Radar

Consulta automática de oportunidades abertas.
""")

    st.info("""
### ⭐ Oportunidades

Licitações classificadas pela SCM.
""")

    st.info("""
### 📑 Detalhes

Análise completa da contratação.
""")

with c2:

    st.info("""
### 🏛️ Órgãos

Órgãos públicos monitorados.
""")

    st.info("""
### 📅 Atas

Atas de Registro de Preço.
""")

    st.info("""
### 📋 Contratos

Consulta de contratos publicados.
""")

with c3:

    st.info("""
### 📊 Estatísticas

Indicadores estratégicos.
""")

    st.info("""
### ⚙️ Configurações

Filtros e parâmetros.
""")

    st.info("""
### 🤖 Inteligência SCM

Sistema de Score e IA.
""")

# -----------------------------------------------------------------------------
# ROADMAP
# -----------------------------------------------------------------------------

st.markdown("## 🛣️ Roadmap")

st.progress(5)

st.write("""
- ✅ Estrutura do projeto

- ⏳ Integração com API do PNCP

- ⏳ Dashboard

- ⏳ Score SCM

- ⏳ Inteligência Artificial
""")

# -----------------------------------------------------------------------------
# RODAPÉ
# -----------------------------------------------------------------------------

st.divider()

st.markdown(
"""
<div class='footer'>

SCM_GOV • Plataforma de Inteligência para Licitações Públicas

Versão 1.0.0

Desenvolvido para SCM Reformas e Engenharia

</div>
""",
unsafe_allow_html=True
)
