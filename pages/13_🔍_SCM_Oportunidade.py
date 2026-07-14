import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from api.contratacoes import propostas_abertas
from services.filtro_service import filtrar_por_especificacoes_scm

st.set_page_config(page_title="Oportunidades SCM", layout="wide")

st.title("⭐ Oportunidades para Atuação")
st.write("Selecione as licitações com propostas abertas para analisar.")

# Datas fixas para o período de 30 dias
hoje = datetime.now()
data_inicial = (hoje - timedelta(days=30)).strftime("%Y%m%d")
data_final = hoje.strftime("%Y%m%d")

@st.cache_data(ttl=3600)
def carregar_dados():
    # Chama a sua função de contratações com propostas abertas
    resposta = propostas_abertas(data_inicial=data_inicial, data_final=data_final, tamanho_pagina=50)
    
    if not resposta.get("success"):
        return []
    
    dados = resposta.get("data", [])
    
    # Aplica o filtro de palavras-chave existente no FiltroService
    with open("assets/palavras_chave.json", "r", encoding="utf-8") as f:
        palavras_chave = json.load(f)
    
    dados_filtrados = []
    for palavra in palavras_chave:
        # Usa sua função existente
        resultado = FiltroService.por_palavra(dados, palavra)
        dados_filtrados.extend(resultado)
        
    # Remove duplicados caso uma licitação contenha mais de uma palavra-chave
    # Assumindo que o item tem um identificador único (ex: 'id' ou 'numeroLicitacao')
    unicos = {item['id']: item for item in dados_filtrados}.values()
    
    return list(unicos)

# Carrega os dados
oportunidades = carregar_dados()

if not oportunidades:
    st.info("Nenhuma oportunidade encontrada no momento.")
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
    
    df_exibicao = df[[c for c in colunas_exibicao.keys() if c in df.columns]].copy()
    df_exibicao = df_exibicao.rename(columns=colunas_exibicao)
    
    # Adiciona coluna para seleção
    df_exibicao.insert(0, "Selecionar", False)

    # Editor de dados interativo
    df_editado = st.data_editor(
        df_exibicao,
        column_config={"Selecionar": st.column_config.CheckboxColumn(default=False)},
        use_container_width=True,
        hide_index=True
    )

    # Captura selecionadas
    selecionadas = df_editado[df_editado["Selecionar"] == True]

    if st.button("Gerar Plano de Atuação"):
        if not selecionadas.empty:
            st.success(f"Licitações selecionadas para análise: {len(selecionadas)}")
            st.write(selecionadas)
        else:
            st.warning("Selecione pelo menos uma licitação.")
