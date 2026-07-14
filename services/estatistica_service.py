"""
Serviço de Estatísticas

Responsável pela geração de indicadores do SCM_GOV.

Autor: SCM_GOV
"""

from collections import Counter


class EstatisticaService:

    # ==========================================================
    # TOTAL DE REGISTROS
    # ==========================================================

    @staticmethod
    def total(dados):

        return len(dados)

    # ==========================================================
    # TOTAL DE OPORTUNIDADES
    # ==========================================================

    @staticmethod
    def oportunidades(dados):

        return len([
            item
            for item in dados
            if item.get("oportunidade", False)
        ])

    # ==========================================================
    # TOTAL CANCELADAS
    # ==========================================================

    @staticmethod
    def canceladas(dados):

        return len([
            item
            for item in dados
            if item.get("cancelado", False)
        ])

    # ==========================================================
    # SCORE MÉDIO
    # ==========================================================

    @staticmethod
    def score_medio(dados):

        scores = [
            item.get("score", 0)
            for item in dados
            if item.get("score") is not None
        ]

        if not scores:
            return 0

        return round(sum(scores) / len(scores), 2)

    # ==========================================================
    # POR MUNICÍPIO
    # ==========================================================

    @staticmethod
    def municipios(dados):

        contador = Counter()

        for item in dados:

            municipio = item.get("municipio")

            if municipio:
                contador[municipio] += 1

        return dict(contador)

    # ==========================================================
    # POR ÓRGÃO
    # ==========================================================

    @staticmethod
    def orgaos(dados):

        contador = Counter()

        for item in dados:

            orgao = item.get("orgao")

            if orgao:
                contador[orgao] += 1

        return dict(contador)

    # ==========================================================
    # CLASSIFICAÇÃO DO SCORE
    # ==========================================================

    @staticmethod
    def classificacao(dados):

        contador = {
            "Excelente": 0,
            "Alta": 0,
            "Média": 0,
            "Baixa": 0,
            "Descartar": 0
        }

        for item in dados:

            categoria = item.get("classificacao")

            if categoria in contador:
                contador[categoria] += 1

        return contador

    # ==========================================================
    # RESUMO
    # ==========================================================

    @classmethod
    def resumo(cls, dados):

        return {

            "total": cls.total(dados),

            "oportunidades": cls.oportunidades(dados),

            "canceladas": cls.canceladas(dados),

            "score_medio": cls.score_medio(dados),

            "municipios": cls.municipios(dados),

            "orgaos": cls.orgaos(dados),

            "classificacao": cls.classificacao(dados)

        }
