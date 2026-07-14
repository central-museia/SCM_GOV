import streamlit as st
import ast
import os
from pathlib import Path

st.set_page_config(page_title="Auditoria Nominal", layout="wide")

st.title("🔍 Auditoria Nominal do SCM_GOV")
st.write("Esta página varre automaticamente todas as pastas do projeto e extrai classes e funções criadas.")

# Pastas que queremos auditar
pastas_para_auditar = ["api", "services", "models", "database"]

def analisar_arquivo(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    
    funcoes = []
    classes = []
    
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            funcoes.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
            # Verifica métodos dentro da classe
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    funcoes.append(f"{node.name}.{item.name}")
                    
    return classes, funcoes

# Interface
for pasta in pastas_para_auditar:
    st.subheader(f"📁 Pasta: {pasta.upper()}")
    path = Path(pasta)
    
    if path.exists():
        arquivos = [f for f in path.glob("*.py") if f.name != "__init__.py"]
        
        for arquivo in arquivos:
            with st.expander(f"📄 {arquivo.name}"):
                classes, funcoes = analisar_arquivo(arquivo)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Classes:**")
                    for c in classes: st.code(c)
                with col2:
                    st.write("**Funções/Métodos:**")
                    for f in funcoes: st.code(f)
    else:
        st.warning(f"Pasta {pasta} não encontrada.")

st.divider()
st.info("Nota: Esta auditoria lê apenas arquivos .py nas pastas raiz de cada domínio.")
