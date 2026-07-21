"""
Oportunidades SCM

Lista todas as licitações abertas no PNCP compatíveis com os CNAEs
e as palavras-chave cadastradas pela SCM, com os dados necessários
para uma decisão rápida sobre participar ou não.

Autor: SCM Engenharia
"""

from datetime import datetime, date, timedelta

import pandas as pd
import streamlit as st

from api.contratacoes import consultar_todas_propostas
from api.parser import PNCPParser
from services.filtro_service import FiltroService
from services.score_service import ScoreService
from services.exportacao_service import ExportacaoService

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Oportunidades SCM | SCM_GOV",
    page_icon="🎯",
    layout="wide"
)

if "favoritos" not in st.session_state:
    st.session_state["favoritos"] = set()

# ==============================================================================
# CABEÇALHO
# ==============================================================================

st.title("🎯 Oportunidades SCM")

st.caption(
    "Licitações abertas no PNCP filtradas automaticamente pelos CNAEs "
    "e palavras-chave cadastrados, com Score SCM para apoiar a decisão "
    "de participar ou não."
)

st.divider()

# ==============================================================================
# FUNÇÕES DE APOIO
# ==============================================================================


@st.cache_resource
def carregar_score_service():
    return ScoreService()


@st.cache_data(ttl=3600, show_spinner=False)
def buscar_licitacoes(data_inicial: str, data_final: str):

    resposta = consultar_todas_propostas(
        data_inicial=data_inicial,
        data_final=data_final,
    )

    if not resposta.get("success"):
        return [], resposta.get("message", "Erro desconhecido ao consultar o PNCP.")

    brutos = resposta.get("data", [])

    licitacoes = [
        PNCPParser.parse_licitacao(item)
        for item in brutos
    ]

    licitacoes = FiltroService.remover_cancelados(licitacoes)

    return licitacoes, None


def dias_restantes(data_encerramento):

    if not data_encerramento:
        return None

    try:
        data = datetime.fromisoformat(
            data_encerramento.replace("Z", "")
        ).date()
    except Exception:
        return None

    return (data - date.today()).days


def estrelas(score):

    cheias = round(score / 20)

    return "★" * cheias + "☆" * (5 - cheias)


def cor_classificacao(classificacao):

    return {
        "Excelente": "🟢",
        "Alta": "🟢",
        "Média": "🟡",
        "Baixa": "🟠",
        "Descartar": "🔴",
    }.get(classificacao, "⚪")


# ==============================================================================
# FILTROS DE BUSCA
# ==============================================================================

st.subheader("Período da Consulta")

col1, col2 = st.columns(2)

with col1:

    data_inicial = st.date_input(
        "Publicado a partir de",
        value=date.today() - timedelta(days=30)
    )

with col2:

    data_final = st.date_input(
        "Publicado até",
        value=date.today()
    )

buscar = st.button(
    "🔍 Buscar Oportunidades no PNCP",
    use_container_width=True,
    type="primary"
)

st.divider()

if buscar:
    st.session_state["oportunidades_buscadas"] = True

if not st.session_state.get("oportunidades_buscadas"):

    st.info(
        "Clique em **Buscar Oportunidades no PNCP** para consultar as "
        "licitações com propostas em aberto no período selecionado."
    )

    st.stop()

# ==============================================================================
# BUSCA E PROCESSAMENTO
# ==============================================================================

with st.spinner("Consultando o PNCP e calculando o Score SCM..."):

    licitacoes, erro = buscar_licitacoes(
        data_inicial.strftime("%Y%m%d"),
        data_final.strftime("%Y%m%d"),
    )

    if erro:
        st.error(f"Não foi possível consultar o PNCP: {erro}")
        st.stop()

    score_service = carregar_score_service()

    oportunidades = []

    for lic in licitacoes:

        palavras = score_service.palavras_compativeis(lic["objeto"])
        cnaes = score_service.cnaes_compativeis(lic["objeto"])

        # Só entra na lista se houver aderência real a CNAE OU palavra-chave
        if not palavras and not cnaes:
            continue

        score = score_service.calcular(lic)
        fatores = score_service.fatores(lic)
        classificacao = score_service.classificacao(score)

        lic["score"] = score
        lic["classificacao"] = classificacao
        lic["fatores"] = fatores
        lic["palavras_compativeis"] = palavras
        lic["cnaes_compativeis"] = cnaes
        lic["dias_restantes"] = dias_restantes(lic["data_encerramento_proposta"])

        oportunidades.append(lic)

if not oportunidades:

    st.warning(
        "Nenhuma licitação aberta no período corresponde aos CNAEs ou "
        "às palavras-chave cadastradas."
    )

    st.stop()

# ==============================================================================
# FILTROS SOBRE O RESULTADO
# ==============================================================================

st.subheader("Filtros")

col1, col2, col3, col4 = st.columns(4)

municipios_disponiveis = sorted({
    lic["municipio"] for lic in oportunidades if lic["municipio"]
})

modalidades_disponiveis = sorted({
    lic["modalidade"] for lic in oportunidades if lic["modalidade"]
})

with col1:

    score_minimo = st.slider(
        "Score mínimo",
        min_value=0,
        max_value=100,
        value=30
    )

with col2:

    classificacao_filtro = st.selectbox(
        "Compatibilidade SCM",
        ["Todas", "Excelente", "Alta", "Média", "Baixa"]
    )

with col3:

    municipio_filtro = st.selectbox(
        "Município",
        ["Todos"] + municipios_disponiveis
    )

with col4:

    modalidade_filtro = st.selectbox(
        "Modalidade",
        ["Todas"] + modalidades_disponiveis
    )

ordenar_por = st.radio(
    "Ordenar por",
    ["Score (maior primeiro)", "Valor estimado (maior primeiro)", "Prazo (mais urgente primeiro)"],
    horizontal=True
)

filtradas = [
    lic for lic in oportunidades
    if lic["score"] >= score_minimo
    and (classificacao_filtro == "Todas" or lic["classificacao"] == classificacao_filtro)
    and (municipio_filtro == "Todos" or lic["municipio"] == municipio_filtro)
    and (modalidade_filtro == "Todas" or lic["modalidade"] == modalidade_filtro)
]

if ordenar_por == "Score (maior primeiro)":
    filtradas.sort(key=lambda x: x["score"], reverse=True)
elif ordenar_por == "Valor estimado (maior primeiro)":
    filtradas.sort(key=lambda x: x["valor_estimado"] or 0, reverse=True)
else:
    filtradas.sort(key=lambda x: (x["dias_restantes"] if x["dias_restantes"] is not None else 9999))

st.divider()

# ==============================================================================
# RESUMO
# ==============================================================================

valor_total = sum(lic["valor_estimado"] or 0 for lic in filtradas)
score_medio = round(sum(lic["score"] for lic in filtradas) / len(filtradas), 1) if filtradas else 0
orgaos_unicos = len({lic["orgao"] for lic in filtradas if lic["orgao"]})

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Oportunidades", len(filtradas))

with col2:
    st.metric("Score Médio", score_medio)

with col3:
    st.metric("Órgãos", orgaos_unicos)

with col4:
    st.metric("Valor Total Estimado", f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.divider()

# ==============================================================================
# EXPORTAÇÃO
# ==============================================================================

col1, col2 = st.columns([3, 1])

with col2:

    if st.button("📤 Exportar Excel", use_container_width=True):

        caminho = ExportacaoService.excel(
            filtradas,
            arquivo="oportunidades_scm.xlsx"
        )

        st.success(f"Exportado para {caminho}")

st.subheader(f"📋 {len(filtradas)} Oportunidade(s) Encontrada(s)")

# ==============================================================================
# CARTÕES DE OPORTUNIDADE
# ==============================================================================

for lic in filtradas:

    numero_pncp = lic["numero_pncp"] or "sem-numero"

    with st.container(border=True):

        # ------------------------------------------------------------
        # NÍVEL 1 - DECISÃO RÁPIDA
        # ------------------------------------------------------------

        col_score, col_info, col_extra = st.columns([1, 3, 2])

        with col_score:

            st.markdown(f"### {cor_classificacao(lic['classificacao'])} {lic['score']} pontos")
            st.markdown(estrelas(lic["score"]))
            st.caption(lic["classificacao"])

        with col_info:

            st.markdown(f"**{lic['objeto'][:160]}{'...' if len(lic['objeto']) > 160 else ''}**")
            st.caption(f"🏛️ {lic['orgao'] or 'Órgão não informado'}")
            st.caption(
                f"📍 {lic['municipio'] or '-'} / {lic['uf'] or '-'}  •  "
                f"📄 {lic['modalidade'] or 'Modalidade não informada'}  •  "
                f"🟢 {lic['situacao'] or 'Aberta'}"
            )

            if lic["cnaes_compativeis"]:
                badges = " ".join(f"`{c['codigo']}`" for c in lic["cnaes_compativeis"][:5])
                st.caption(f"CNAEs compatíveis: {badges}")

        with col_extra:

            valor = lic["valor_estimado"]
            st.metric(
                "Valor Estimado",
                f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if valor else "Não informado"
            )

            dias = lic["dias_restantes"]

            if dias is None:
                st.caption("⏳ Prazo não informado")
            elif dias < 0:
                st.caption("⚫ Prazo encerrado")
            elif dias <= 3:
                st.caption(f"🔴 URGENTE — faltam {dias} dia(s)")
            elif dias <= 7:
                st.caption(f"🟡 Faltam {dias} dias")
            else:
                st.caption(f"🟢 Faltam {dias} dias")

            st.caption(f"Sessão: {lic['data_abertura_proposta_fmt'] or lic['data_encerramento_proposta_fmt'] or '-'}")

        # ------------------------------------------------------------
        # AÇÕES RÁPIDAS
        # ------------------------------------------------------------

        acoes = st.columns(6)

        with acoes[0]:
            if lic["link"]:
                st.link_button("📄 Ver Edital", lic["link"], use_container_width=True)
            else:
                st.button("📄 Ver Edital", disabled=True, use_container_width=True, key=f"edital_{numero_pncp}")

        with acoes[1]:
            st.button("🤖 Analisar com IA", disabled=True, use_container_width=True, key=f"ia_{numero_pncp}",
                       help="Em breve: leitura automática do edital pela IA")

        with acoes[2]:
            st.button("📊 Ver Riscos", disabled=True, use_container_width=True, key=f"riscos_{numero_pncp}",
                       help="Em breve: extração de riscos do edital")

        with acoes[3]:
            st.button("📁 Checklist Docs", disabled=True, use_container_width=True, key=f"docs_{numero_pncp}",
                       help="Em breve: checklist de documentos exigidos")

        with acoes[4]:
            st.button("📈 Estimar Custos", disabled=True, use_container_width=True, key=f"custos_{numero_pncp}",
                       help="Em breve: estimativa de custos da proposta")

        with acoes[5]:
            favoritado = numero_pncp in st.session_state["favoritos"]
            label = "⭐ Favoritado" if favoritado else "☆ Favoritar"
            if st.button(label, use_container_width=True, key=f"fav_{numero_pncp}"):
                if favoritado:
                    st.session_state["favoritos"].discard(numero_pncp)
                else:
                    st.session_state["favoritos"].add(numero_pncp)
                st.rerun()

        # ------------------------------------------------------------
        # NÍVEL 2 E 3 - DETALHES ESTRATÉGICOS
        # ------------------------------------------------------------

        with st.expander("🔎 Ver detalhes estratégicos e Score SCM"):

            col_a, col_b = st.columns(2)

            with col_a:

                st.markdown("**Objeto completo**")
                st.write(lic["objeto"] or "Não informado")

                st.markdown("**Escopo identificado (palavras-chave)**")
                if lic["palavras_compativeis"]:
                    for palavra in lic["palavras_compativeis"]:
                        st.write(f"✔ {palavra}")
                else:
                    st.write("Nenhuma palavra-chave identificada no objeto.")

                st.markdown("**Local**")
                st.write(f"{lic['municipio'] or '-'} / {lic['uf'] or '-'}")

                st.markdown("**Processo / Compra**")
                st.write(
                    f"Nº {lic['numero_compra'] or '-'}/{lic['ano_compra'] or '-'}  •  "
                    f"Processo: {lic['processo'] or '-'}"
                )

                st.markdown("**Modo de Disputa**")
                st.write(lic["modo_disputa"] or "Não informado")

            with col_b:

                st.markdown("**Score SCM — detalhamento**")

                for fator, pontos in lic["fatores"].items():
                    maximo = {"Região de atuação": 30, "Palavras-chave": 40, "CNAE": 20, "Proposta em aberto": 10}.get(fator, 100)
                    st.progress(
                        min(pontos / maximo, 1.0) if maximo else 0,
                        text=f"{fator}: {pontos}/{maximo}"
                    )

                st.markdown("**CNAEs compatíveis**")
                if lic["cnaes_compativeis"]:
                    for c in lic["cnaes_compativeis"]:
                        st.write(f"✔ {c['codigo']} — {c['descricao']}")
                else:
                    st.write("Nenhum CNAE compatível identificado no objeto.")

                st.markdown("**Alertas automáticos**")

                if lic["cnaes_compativeis"] or lic["palavras_compativeis"]:
                    st.write("🟢 Objeto compatível com o perfil da SCM")
                else:
                    st.write("🔴 Nenhuma aderência direta identificada")

                if lic["dias_restantes"] is not None and lic["dias_restantes"] <= 3:
                    st.write("🟡 Prazo muito curto para preparação da proposta")

                if not lic["valor_estimado"]:
                    st.write("🟡 Valor estimado não informado pelo órgão")

            st.info(
                "📌 **Riscos, documentação exigida, garantia contratual, critério de "
                "julgamento e regime de execução** dependem da leitura do edital "
                "completo e serão exibidos aqui quando o módulo de **Análise de "
                "Edital com IA** (roadmap Versão 3) estiver disponível.",
                icon="🤖"
            )

st.divider()

st.caption(
    "Fonte: Portal Nacional de Contratações Públicas (PNCP). "
    "Score SCM calculado com base em região de atuação, palavras-chave e "
    "CNAEs cadastrados em Configurações."
)
