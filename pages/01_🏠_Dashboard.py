import streamlit as st
from datetime import datetime, timedelta
from api.contratacoes import propostas_abertas
from api.contratos import publicados
from api.atas import consultar as consultar_atas

# ==========================================================
# CONFIGURAÇÃO E DADOS
# ==========================================================
st.set_page_config(page_title="Dashboard SCM_GOV", layout="wide")

st.title("🏠 Dashboard")
st.write(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Definindo datas para busca (últimos 30 dias)
hoje = datetime.now()
data_inicial = (hoje - timedelta(days=30)).strftime("%Y%m%d")
data_final = hoje.strftime("%Y%m%d")

# Carregar dados (simulando cache)
@st.cache_data(ttl=3600)
def carregar_kpis():
    # Chamadas às funções já criadas
    licitacoes = propostas_abertas(data_inicial=data_inicial, data_final=data_final)
    contratos = publicados(data_inicial=data_inicial, data_final=data_final)
    atas = consultar_atas(data_inicial=data_inicial, data_final=data_final)
    
    # Extração simples para exibição nos KPIs
    total_lic = len(licitacoes["data"]) if licitacoes.get("success") else 0
    total_con = len(contratos["data"]) if contratos.get("success") else 0
    total_atas = len(atas["data"]) if atas.get("success") else 0
    
    return total_lic, total_con, total_atas

total_lic, total_con, total_atas = carregar_kpis()

# ==========================================================
# KPIs
# ==========================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Licitações Abertas", total_lic)
with col2:
    st.metric("Atas Vigentes", total_atas)
with col3:
    st.metric("Contratações", total_con)
with col4:
    st.metric("Valor Total", "R$ 0,00") # Aguardando Parser de valor

st.divider()

# ==========================================================
# GRÁFICOS (Estrutura)
# ==========================================================
st.subheader("Análise de Mercado")

tab1, tab2, tab3 = st.tabs(["Por Estado", "Por Modalidade", "Evolução Diária"])

with tab1:
    st.write("Gráfico: Licitações por Estado")
    # Aqui entrará a lógica de agrupamento por UF usando os dados da API
    
with tab2:
    st.write("Gráfico: Licitações por Modalidade")

with tab3:
    st.write("Gráfico: Evolução diária das oportunidades")

# ==========================================================
# OUTROS INDICADORES
# ==========================================================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Estados com mais oportunidades")
    st.bar_chart({"SP": 10, "RJ": 8, "MG": 5}) # Exemplo

with col_b:
    st.subheader("Órgãos mais ativos")
    st.write("Lista dos 5 órgãos com maior volume de contratações no período.")
