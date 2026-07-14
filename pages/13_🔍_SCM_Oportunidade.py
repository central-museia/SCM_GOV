import sys
import os

# Força o Python a olhar na raiz do projeto, garantindo que ele ache a pasta 'services'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from api.contratacoes import propostas_abertas
from services.filtro_service import filtrar_por_especificacoes_scm # Importa direto a função

st.title("⭐ Oportunidades para Atuação")

@st.cache_data(ttl=3600)
def carregar_dados():
    # 1. Busca os dados brutos da API
    hoje = datetime.now()
    data_inicial = (hoje - timedelta(days=30)).strftime("%Y%m%d")
    data_final = hoje.strftime("%Y%m%d")
    
    resposta = propostas_abertas(data_inicial=data_inicial, data_final=data_final, tamanho_pagina=100)
    dados_brutos = resposta.get("data", []) if resposta.get("success") else []
    
    # 2. VALIDAÇÃO MESTRE: Somente o que está de acordo com a empresa passa
    return filtro_service.filtrar_por_especificacoes_scm(dados_brutos)

# Executa o fluxo de validação
oportunidades = carregar_dados()

if not oportunidades:
    st.info("Nenhuma oportunidade encontrada que atenda aos critérios da SCM.")
else:
    df = pd.DataFrame(oportunidades)
    
    # Mapeamento para exibição
    colunas_exibicao = {
        "objeto": "Objeto",
        "nomeOrgao": "Órgão",
        "municipioNome": "Município",
        "modalidadeNome": "Modalidade",
        "valorEstimado": "Preço Estimado",
        "dataAberturaProposta": "Data Abertura"
    }
    
    # Filtra e renomeia
    df_exibicao = df[[c for c in colunas_exibicao.keys() if c in df.columns]].copy()
    df_exibicao = df_exibicao.rename(columns=colunas_exibicao)
    df_exibicao.insert(0, "Selecionar", False)

    # Exibição
    df_editado = st.data_editor(
        df_exibicao,
        column_config={"Selecionar": st.column_config.CheckboxColumn(default=False)},
        use_container_width=True,
        hide_index=True
    )

    if st.button("Gerar Plano de Atuação"):
        selecionadas = df_editado[df_editado["Selecionar"] == True]
        if not selecionadas.empty:
            st.success(f"Análise iniciada para {len(selecionadas)} licitações.")
        else:
            st.warning("Selecione pelo menos uma licitação.")
