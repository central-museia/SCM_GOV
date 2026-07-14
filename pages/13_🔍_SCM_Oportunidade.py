import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from api.contratacoes import consultar_todas_propostas
from services.filtro_service import FiltroService

st.set_page_config(page_title="Oportunidades SCM", layout="wide")

st.title("⭐ Oportunidades para Atuação")
st.write("Selecione as licitações que deseja analisar ou atuar.")

# Definição de período para busca
hoje = datetime.now()
data_inicial = (hoje - timedelta(days=30)).strftime("%Y%m%d")
data_final = hoje.strftime("%Y%m%d")

@st.cache_data(ttl=3600)
def carregar_oportunidades():
    # 1. Busca tudo da API
    dados = consultar_todas_propostas(data_inicial, data_final)
    
    # 2. Aplica o filtro de palavras-chave usando a função existente 'por_palavra'
    # Como você tem uma lista de palavras-chave, vamos iterar sobre elas:
    with open("assets/palavras_chave.json", "r", encoding="utf-8") as f:
        palavras_chave = json.load(f)
    
    dados_filtrados = []
    for palavra in palavras_chave:
        # Usa sua função existente
        resultado = FiltroService.por_palavra(dados, palavra)
        dados_filtrados.extend(resultado)
        
    # Remove duplicados (caso a mesma licitação atenda a duas palavras-chave)
    dados_unicos = {item['id']: item for item in dados_filtrados}.values()
    
    return list(dados_unicos)

# Carrega os dados
oportunidades = carregar_oportunidades()

if not oportunidades:
    st.info("Nenhuma oportunidade encontrada com os critérios atuais.")
else:
    df = pd.DataFrame(oportunidades)
    
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
    
    # Adicionando a coluna de seleção necessária para o st.data_editor
    df_exibicao.insert(0, "Selecionar", False)

    st.write(f"Total de oportunidades encontradas: {len(df_exibicao)}")
    
    # Editor de dados interativo
    df_editado = st.data_editor(
        df_exibicao,
        column_config={"Selecionar": st.column_config.CheckboxColumn(default=False)},
        use_container_width=True,
        hide_index=True
    )

    # Filtrar apenas as linhas selecionadas pelo usuário
    selecionadas = df_editado[df_editado["Selecionar"] == True]

    if st.button("Gerar Plano de Atuação para Selecionadas"):
        if not selecionadas.empty:
            st.success(f"Você selecionou {len(selecionadas)} licitações para análise.")
        else:
            st.warning("Selecione pelo menos uma licitação.")
