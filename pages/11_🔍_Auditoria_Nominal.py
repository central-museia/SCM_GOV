import streamlit as st
import ast
import os
from pathlib import Path

st.set_page_config(page_title="Auditoria Arquitetural", layout="wide")

st.title("🔍 Auditoria de Relacionamentos (Arquitetura)")
st.write("Mapeamento de quais pastas consomem quais módulos.")

pastas_alvo = ["pages", "api", "services", "models", "database"]

def extrair_imports(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except:
            return []
    
    imports = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
        elif isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name.split('.')[0])
    return list(imports)

# Mapeamento
for pasta in pastas_alvo:
    st.subheader(f"📁 Analisando dependências de: {pasta}")
    path = Path(pasta)
    
    if path.exists():
        for arquivo in path.glob("**/*.py"):
            deps = extrair_imports(arquivo)
            # Filtra apenas imports que são pastas do nosso projeto
            relacoes = [d for d in deps if d in pastas_alvo and d != pasta]
            
            if relacoes:
                with st.expander(f"Arquivo: {arquivo.relative_to(os.getcwd())}"):
                    st.write(f"⚠️ Este arquivo importa de: **{', '.join(relacoes)}**")
    else:
        st.error(f"Pasta {pasta} não encontrada.")

st.divider()
st.info("Esta auditoria ignora imports padrão do Python e foca apenas nas suas pastas de sistema.")
