import streamlit as st

from services.consulta_service import consultar_licitacoes

st.title("📋 Licitações em Aberto")

col1, col2 = st.columns([1,2])

with col1:
    uf = st.selectbox(
        "UF",
        ["RJ"]
    )

with col2:
    palavra = st.text_input(
        "Objeto",
        placeholder="reforma, engenharia, manutenção..."
    )

if st.button("Buscar"):

    with st.spinner("Consultando PNCP..."):

        df = consultar_licitacoes(
            uf=uf,
            palavra=palavra
        )

    if df.empty:
        st.warning("Nenhuma licitação encontrada.")
    else:

        st.success(f"{len(df)} licitações encontradas.")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
