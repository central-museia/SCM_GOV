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
    # RESPOSTA PADRÃO
    # ==========================================================

    @staticmethod
    def resposta(resposta):

        return {
            "dados": resposta.get("data", []),
            "paginacao": PNCPParser.paginacao(resposta)
        }
