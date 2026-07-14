import sys
import os
from datetime import datetime, timedelta

# Força o Python a olhar na raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from api.contratacoes import propostas_abertas
from services.filtro_service import filtrar_por_especificacoes_scm

st.set_page_config(page_title="Oportunidades SCM", layout="wide")

st.title("⭐ Oportunidades para Atuação")

@st.cache_data(ttl=3600)
def carregar_oportunidades_abertas():
    # Período de 30 dias
    hoje = datetime.now()
    data_inicial = (hoje - timedelta(days=30)).strftime("%Y%m%d")
    data_final = hoje.strftime("%Y%m%d")
    
    # Busca da API
    resposta = propostas_abertas(data_inicial=data_inicial, data_final=data_final, tamanho_pagina=100)
    dados = resposta.get("data", []) if resposta.get("success") else []
    
    # Aplica o filtro mestre (Validação SCM)
    return filtrar_por_especificacoes_scm(dados)

# Carrega e exibe
oportunidades = carregar_oportunidades_abertas()

if not oportunidades:
    st.info("Nenhuma oportunidade encontrada que atenda aos critérios da SCM.")
else:
    df = pd.DataFrame(oportunidades)
    
    # Colunas essenciais para decisão rápida
    colunas_map = {
        "objeto": "Objeto",
        "nomeOrgao": "Órgão",
        "municipioNome": "Município",
        "valorEstimado": "Valor",
        "dataAberturaProposta": "Abertura"
    }
    
    # Filtra apenas colunas existentes
    df_exibicao = df[[c for c in colunas_map.keys() if c in df.columns]].rename(columns=colunas_map)
    
    # Exibe tabela rápida
    st.dataframe(
        df_exibicao,
        use_container_width=True,
        hide_index=True
    )
    
    st.write(f"Total de licitações validadas para a SCM: **{len(df_exibicao)}**")
