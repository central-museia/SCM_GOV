import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from api.contratacoes import consultar_todas_propostas
from api.contratos import publicados
from api.atas import consultar as consultar_atas
from api.parser import PNCPParser
from services.filtro_service import FiltroService

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================
st.set_page_config(page_title="Dashboard SCM_GOV", layout="wide")

st.title("🏠 Dashboard")
st.write(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

hoje = datetime.now()
data_inicial = (hoje - timedelta(days=30)).strftime("%Y%m%d")
data_final = hoje.strftime("%Y%m%d")

# ==========================================================
# CARREGAMENTO DE DADOS
# ==========================================================

@st.cache_data(ttl=3600)
def carregar_kpis():

    erros = []

    # 1. LICITAÇÕES (todas as páginas, dados brutos do PNCP)
    resp_licitacoes = consultar_todas_propostas(
        data_inicial=data_inicial,
        data_final=data_final
    )

    if not resp_licitacoes.get("success"):
        erros.append(f"Licitações: {resp_licitacoes.get('message')}")
        licitacoes_norm = []
    else:
        brutos = resp_licitacoes.get("data", [])
        licitacoes_norm = PNCPParser.parse_contratacoes(brutos)

    # 2. FILTRO SCM (agora funciona, pois os dados têm "objeto")
    dados_scm = FiltroService.filtrar_por_especificacoes_scm(licitacoes_norm)

    # 3. CONTRATOS
    resp_contratos = publicados(data_inicial=data_inicial, data_final=data_final)

    if resp_contratos.get("success"):
        total_con = len(resp_contratos["data"].get("data", []))
    else:
        erros.append(f"Contratos: {resp_contratos.get('message')}")
        total_con = 0

    # 4. ATAS
    resp_atas = consultar_atas(data_inicial=data_inicial, data_final=data_final)

    if resp_atas.get("success"):
        total_atas = len(resp_atas["data"].get("data", []))
    else:
        erros.append(f"Atas: {resp_atas.get('message')}")
        total_atas = 0

    valor_total = sum(item.get("valor", 0) or 0 for item in dados_scm)

    return dados_scm, total_con, total_atas, valor_total, erros


dados_scm, total_con, total_atas, valor_total, erros = carregar_kpis()

if erros:
    for erro in erros:
        st.warning(f"⚠️ Falha ao consultar PNCP — {erro}")

# ==========================================================
# KPIs
# ==========================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Licitações SCM", len(dados_scm))
with col2:
    st.metric("Atas Vigentes", total_atas)
with col3:
    st.metric("Contratações", total_con)
with col4:
    st.metric("Valor Total", PNCPParser.moeda(valor_total))

st.divider()

# ==========================================================
# GRÁFICOS
# ==========================================================
st.subheader("Análise de Mercado")

df = pd.DataFrame(dados_scm)

tab1, tab2, tab3 = st.tabs(["Por Estado", "Por Modalidade", "Evolução Diária"])

with tab1:
    if not df.empty and "uf" in df:
        contagem_uf = df["uf"].value_counts()
        st.bar_chart(contagem_uf)
    else:
        st.info("Sem dados de licitações no período para agrupar por estado.")

with tab2:
    if not df.empty and "modalidade" in df:
        contagem_mod = df["modalidade"].value_counts()
        st.bar_chart(contagem_mod)
    else:
        st.info("Sem dados de licitações no período para agrupar por modalidade.")

with tab3:
    if not df.empty and "data_publicacao" in df:
        contagem_dia = df["data_publicacao"].value_counts().sort_index()
        st.bar_chart(contagem_dia)
    else:
        st.info("Sem dados suficientes para evolução diária.")

st.divider()

# ==========================================================
# OUTROS INDICADORES
# ==========================================================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Municípios com mais oportunidades")
    if not df.empty and "municipio" in df:
        st.bar_chart(df["municipio"].value_counts().head(10))
    else:
        st.info("Sem dados no período.")

with col_b:
    st.subheader("Órgãos mais ativos")
    if not df.empty and "orgao" in df:
        st.dataframe(
            df["orgao"].value_counts().head(5).rename("Licitações"),
            use_container_width=True
        )
    else:
        st.info("Sem dados no período.")
