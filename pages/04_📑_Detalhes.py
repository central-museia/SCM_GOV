"""
Detalhes da Licitação

Análise completa da oportunidade.

Autor: SCM Engenharia
"""

import streamlit as st

from services.score_service import ScoreService
from services.exportacao_service import ExportacaoService
from api.parser import PNCPParser

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Detalhes | SCM_GOV",
    page_icon="📑",
    layout="wide"
)

# ==============================================================================
# CABEÇALHO
# ==============================================================================

st.title("📑 Detalhes da Licitação")

st.caption(
    "Análise completa da oportunidade selecionada."
)

st.divider()

# ==============================================================================
# VALIDAÇÃO — precisa vir de "Oportunidades" com um item selecionado
# ==============================================================================

licitacao = st.session_state.get("licitacao_selecionada")

if not licitacao:

    st.warning(
        "Nenhuma licitação selecionada. Volte para a página de "
        "Oportunidades e clique em '📑 Ver Detalhes' em um item da lista."
    )

    if st.button("⬅️ Ir para Oportunidades"):
        st.switch_page("pages/03_⭐_Oportunidades.py")

    st.stop()

# ==============================================================================
# DADOS GERAIS
# ==============================================================================

st.subheader("Informações Gerais")

col1, col2 = st.columns(2)

with col1:

    st.text_input(
        "Número da Licitação",
        value=licitacao.get("numero_pncp", ""),
        disabled=True
    )

    st.text_input(
        "Órgão",
        value=licitacao.get("orgao", ""),
        disabled=True
    )

    st.text_input(
        "Município",
        value=licitacao.get("municipio", ""),
        disabled=True
    )

    st.text_input(
        "Modalidade",
        value=licitacao.get("modalidade", ""),
        disabled=True
    )

with col2:

    st.text_input(
        "Data de Publicação",
        value=PNCPParser.formatar_data(licitacao.get("data_publicacao", "")) or licitacao.get("data_publicacao", ""),
        disabled=True
    )

    st.text_input(
        "Prazo Final",
        value=PNCPParser.formatar_data(licitacao.get("encerramento_proposta", "")) or licitacao.get("encerramento_proposta", ""),
        disabled=True
    )

    st.text_input(
        "Valor Estimado",
        value=PNCPParser.moeda(licitacao.get("valor")),
        disabled=True
    )

    st.text_input(
        "Situação",
        value="Cancelada" if licitacao.get("cancelado") else "Vigente",
        disabled=True
    )

st.divider()

# ==============================================================================
# OBJETO
# ==============================================================================

st.subheader("Objeto da Contratação")

st.text_area(
    "",
    value=licitacao.get("objeto", ""),
    height=180,
    disabled=True,
    label_visibility="collapsed"
)

st.divider()

# ==============================================================================
# SCORE SCM
# ==============================================================================

st.subheader("Score SCM")

col1, col2, col3 = st.columns(3)

score = licitacao.get("score", 0)
classificacao = licitacao.get("classificacao", "-")

recomendacao = (
    "Investir na proposta" if licitacao.get("oportunidade")
    else "Não recomendado"
)

with col1:
    st.metric("Score", score)

with col2:
    st.metric("Classificação", classificacao)

with col3:
    st.metric("Recomendação", recomendacao)

if licitacao.get("motivos"):
    st.caption(f"⚠️ Motivos de atenção: {licitacao['motivos']}")

with st.expander("Como esse score foi calculado?"):

    score_service = ScoreService()

    texto = licitacao.get("objeto", "")
    municipio = licitacao.get("municipio", "")
    proposta_aberta = licitacao.get("recebimento_proposta", False)

    st.write(f"- Região (município monitorado): **{score_service.score_regiao(municipio)} pts**")
    st.write(f"- Palavras-chave SCM no objeto: **{score_service.score_palavras(texto)} pts**")
    st.write(f"- Aderência a CNAE da SCM: **{score_service.score_cnae(texto)} pts**")
    st.write(f"- Proposta em aberto: **{score_service.score_proposta(proposta_aberta)} pts**")

st.divider()

# ==============================================================================
# DOCUMENTOS
# ==============================================================================

st.subheader("Documentos")

link = licitacao.get("link", "")

if link:
    st.link_button("🔗 Acessar edital no sistema de origem", link, use_container_width=True)
else:
    st.info(
        "Nenhum link de documento disponível para esta licitação."
    )

st.divider()

# ==============================================================================
# OBSERVAÇÕES SCM
# ==============================================================================

st.subheader("Observações")

chave_obs = f"obs_{licitacao.get('numero_pncp', 'sem_numero')}"

observacao = st.text_area(
    "Anotações da análise",
    value=st.session_state.get(chave_obs, ""),
    height=180
)

if observacao != st.session_state.get(chave_obs, ""):
    st.session_state[chave_obs] = observacao

st.caption(
    "⚠️ As observações são mantidas apenas durante esta sessão do navegador. "
    "Para persistir entre sessões, é necessário integrar com o banco de dados."
)

st.divider()

# ==============================================================================
# AÇÕES
# ==============================================================================

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "⬅️ Voltar",
        use_container_width=True
    ):
        st.switch_page("pages/03_⭐_Oportunidades.py")

with col2:

    caminho_excel = ExportacaoService.excel(
        [licitacao],
        arquivo=f"licitacao_{licitacao.get('numero_pncp', 'detalhe')}.xlsx"
    )

    with open(caminho_excel, "rb") as arquivo:

        st.download_button(
            "📤 Exportar",
            data=arquivo,
            file_name=f"licitacao_{licitacao.get('numero_pncp', 'detalhe')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

with col3:

    if st.button(
        "🔄 Atualizar Dados",
        use_container_width=True
    ):
        st.info(
            "Para atualizar, volte a Oportunidades e clique em 'Atualizar' — "
            "isso reconsulta o PNCP e recalcula o Score SCM."
        )
