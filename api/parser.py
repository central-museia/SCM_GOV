"""
Parser da API PNCP

Responsável por padronizar os retornos da API.

Autor: SCM_GOV
"""

from datetime import datetime


class PNCPParser:

    # ==========================================================
    # DATA
    # ==========================================================

    @staticmethod
    def formatar_data(data):

        if not data:
            return ""

        try:
            return datetime.fromisoformat(
                data.replace("Z", "")
            ).strftime("%d/%m/%Y")
        except Exception:
            return data

    # ==========================================================
    # BOOLEAN
    # ==========================================================

    @staticmethod
    def sim_nao(valor):

        return "Sim" if valor else "Não"

    # ==========================================================
    # VALOR
    # ==========================================================

    @staticmethod
    def moeda(valor):

        if valor is None:
            return ""

        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # ==========================================================
    # PAGINAÇÃO
    # ==========================================================

    @staticmethod
    def paginacao(resposta):

        return {
            "total_registros": resposta.get("totalRegistros", 0),
            "total_paginas": resposta.get("totalPaginas", 0),
            "pagina": resposta.get("numeroPagina", 0),
            "paginas_restantes": resposta.get("paginasRestantes", 0),
            "vazio": resposta.get("empty", True)
        }

    # ==========================================================
    # ATA
    # ==========================================================

    @staticmethod
    def parse_ata(ata):

        return {

            "numero_pncp": ata.get("numeroControlePNCPAta"),

            "ata": ata.get("numeroAtaRegistroPreco"),

            "ano": ata.get("anoAta"),

            "objeto": ata.get("objetoContratacao"),

            "orgao": ata.get("nomeOrgao"),

            "cnpj": ata.get("cnpjOrgao"),

            "unidade": ata.get("nomeUnidadeOrgao"),

            "vigencia_inicio": PNCPParser.formatar_data(
                ata.get("vigenciaInicio")
            ),

            "vigencia_fim": PNCPParser.formatar_data(
                ata.get("vigenciaFim")
            ),

            "assinatura": PNCPParser.formatar_data(
                ata.get("dataAssinatura")
            ),

            "publicacao": PNCPParser.formatar_data(
                ata.get("dataPublicacaoPncp")
            ),

            "cancelada": PNCPParser.sim_nao(
                ata.get("cancelado")
            ),

            "adesao": PNCPParser.sim_nao(
                ata.get("possibilidadeAdesao")
            )
        }

    # ==========================================================
    # LISTA DE ATAS
    # ==========================================================

    @staticmethod
    def parse_atas(resposta):

        dados = resposta.get("data", [])

        return [
            PNCPParser.parse_ata(item)
            for item in dados
        ]

    # ==========================================================
    # LICITAÇÃO / CONTRATAÇÃO
    # ==========================================================

    @staticmethod
    def parse_licitacao(item):
        """
        Normaliza um registro de contratação retornado pelo endpoint
        /v1/contratacoes/proposta (ou /publicacao) do PNCP para um
        formato simples, usado pelos serviços de Score, Filtro e
        pela página de Oportunidades.
        """

        orgao_entidade = item.get("orgaoEntidade", {}) or {}

        unidade_orgao = item.get("unidadeOrgao", {}) or {}

        situacao = item.get("situacaoCompraNome", "") or ""

        return {

            "numero_pncp": item.get("numeroControlePNCP"),

            "numero_compra": item.get("numeroCompra"),

            "ano_compra": item.get("anoCompra"),

            "processo": item.get("processo"),

            "objeto": item.get("objetoCompra", "") or "",

            "orgao": orgao_entidade.get("razaoSocial"),

            "cnpj_orgao": orgao_entidade.get("cnpj"),

            "esfera": orgao_entidade.get("esferaId"),

            "poder": orgao_entidade.get("poderId"),

            "unidade": unidade_orgao.get("nomeUnidade"),

            "codigo_unidade": unidade_orgao.get("codigoUnidade"),

            "municipio": unidade_orgao.get("municipioNome"),

            "uf": unidade_orgao.get("ufSigla"),

            "modalidade": item.get("modalidadeNome"),

            "modo_disputa": item.get("modoDisputaNome"),

            "situacao": situacao,

            "valor_estimado": item.get("valorTotalEstimado"),

            "data_publicacao": item.get("dataPublicacaoPncp"),

            "data_publicacao_fmt": PNCPParser.formatar_data(
                item.get("dataPublicacaoPncp")
            ),

            "data_abertura_proposta": item.get("dataAberturaProposta"),

            "data_abertura_proposta_fmt": PNCPParser.formatar_data(
                item.get("dataAberturaProposta")
            ),

            "data_encerramento_proposta": item.get("dataEncerramentoProposta"),

            "data_encerramento_proposta_fmt": PNCPParser.formatar_data(
                item.get("dataEncerramentoProposta")
            ),

            "link": item.get("linkSistemaOrigem"),

            "cancelado": "cancelad" in situacao.lower(),

            "recebimento_proposta": True,

        }

    # ==========================================================
    # LISTA DE LICITAÇÕES
    # ==========================================================

    @staticmethod
    def parse_licitacoes(resposta):

        dados = resposta.get("data", [])

        return [
            PNCPParser.parse_licitacao(item)
            for item in dados
        ]

    # ==========================================================
    # RESPOSTA PADRÃO
    # ==========================================================

    @staticmethod
    def resposta(resposta):

        return {
            "dados": resposta.get("data", []),
            "paginacao": PNCPParser.paginacao(resposta)
        }
