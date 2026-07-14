import streamlit as st
import pandas as pd
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
    dados_brutos = consultar_todas_propostas(data_inicial, data_final)
    # 2. Filtra pelo balizador (CNAEs/Palavras-chave)
    return FiltroService.filtrar_por_especificacoes_scm(dados_brutos)

# Carrega os dados filtrados
oportunidades = carregar_oportunidades()

if not oportunidades:
    st.info("Nenhuma oportunidade encontrada com os critérios atuais.")
else:
    # Transformar em DataFrame para exibição amigável
    # Nota: Ajuste as chaves (ex: 'objeto', 'orgao') conforme o retorno real do seu JSON do PNCP
    df = pd.DataFrame(oportunidades)
    
    # Seleção de colunas para tomada de decisão
    colunas_exibicao = {
        "objeto": "Objeto",
        "nomeOrgao": "Órgão",
        "municipioNome": "Município",
        "modalidadeNome": "Modalidade",
        "valorEstimado": "Preço Estimado",
        "dataAberturaProposta": "Data Abertura"
    }
    
    # Filtra apenas colunas existentes no DataFrame
    df_exibicao = df[[c for c in colunas_exibicao.keys() if c in df.columns]]
    df_exibicao = df_exibicao.rename(columns=colunas_exibicao)

    # Componente de seleção (Checkboxes na tabela)
    st.write(f"Total de oportunidades encontradas: {len(df_exibicao)}")
    
    # Editor de dados interativo (o usuário pode selecionar linhas)
    selecionadas = st.data_editor(
        df_exibicao,
        column_config={"Selecionar": st.column_config.CheckboxColumn(default=False)},
        use_container_width=True,
        hide_index=True
    )

    # Botão de Ação
    if st.button("Gerar Plano de Atuação para Selecionadas"):
        st.success(f"Você selecionou {len(selecionadas)} licitações para análise.")
        # Aqui você futuramente chamará o ia_service para analisar os editais
