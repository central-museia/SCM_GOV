import streamlit as st
import os
from pathlib import Path

st.set_page_config(page_title="Auditoria Estrutural", layout="wide")

st.title("📂 Auditoria Estrutural do SCM_GOV")
st.write("Mapeamento das pastas do sistema (ignorando arquivos e funções).")

# Lista das pastas principais da sua estrutura
pastas_raiz = [
    "pages", 
    "api", 
    "services", 
    "models", 
    "database", 
    "assets"
]

def listar_pastas(diretorio_raiz):
    estrutura = {}
    for pasta in diretorio_raiz:
        caminho = Path(pasta)
        if caminho.exists() and caminho.is_dir():
            # Lista subpastas dentro da pasta principal
            subpastas = [d.name for d in caminho.iterdir() if d.is_dir()]
            estrutura[pasta] = subpastas
    return estrutura

estrutura_atual = listar_pastas(pastas_raiz)

# Exibição da Auditoria
for pasta, subpastas in estrutura_atual.items():
    st.subheader(f"📁 Pasta: {pasta}")
    if subpastas:
        for sub in subpastas:
            st.write(f"└─ 📂 {sub}")
    else:
        st.caption("Nenhuma subpasta encontrada.")
    st.divider()

st.info("Esta página mostra apenas a árvore de diretórios do seu projeto, sem analisar nenhum arquivo ou código.")
