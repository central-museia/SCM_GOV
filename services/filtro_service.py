"""
Serviço de filtros

Responsável por aplicar filtros nas licitações retornadas pela API.

Autor: SCM_GOV
"""


class FiltroService:

    # ==========================================================
    # MUNICÍPIO
    # ==========================================================

    @staticmethod
    def por_municipio(dados, municipio):

        if not municipio:
            return dados

        return [
            item for item in dados
            if item.get("municipio", "").lower() == municipio.lower()
        ]

    # ==========================================================
    # ÓRGÃO
    # ==========================================================

    @staticmethod
    def por_orgao(dados, orgao):

        if not orgao:
            return dados

        return [
            item for item in dados
            if orgao.lower() in item.get("orgao", "").lower()
        ]

    # ==========================================================
    # OBJETO
    # ==========================================================

    @staticmethod
    def por_palavra(dados, palavra):

        if not palavra:
            return dados

        return [
            item for item in dados
            if palavra.lower() in item.get("objeto", "").lower()
        ]

    # ==========================================================
    # PERÍODO
    # ==========================================================

    @staticmethod
    def por_periodo(
        dados,
        campo_data,
        data_inicio,
        data_fim,
    ):

        if not data_inicio or not data_fim:
            return dados

        return [
            item for item in dados
            if data_inicio <= item.get(campo_data, "") <= data_fim
        ]

    # ==========================================================
    # STATUS
    # ==========================================================

    @staticmethod
    def por_status(dados, status):

        if status is None:
            return dados

        return [
            item for item in dados
            if item.get("status") == status
        ]

    # ==========================================================
    # VALOR MÍNIMO
    # ==========================================================

    @staticmethod
    def valor_minimo(dados, valor):

        if valor is None:
            return dados

        return [
            item for item in dados
            if item.get("valor", 0) >= valor
        ]

    # ==========================================================
    # VALOR MÁXIMO
    # ==========================================================

    @staticmethod
    def valor_maximo(dados, valor):

        if valor is None:
            return dados

        return [
            item for item in dados
            if item.get("valor", 0) <= valor
        ]

    # ==========================================================
    # REGISTROS CANCELADOS
    # ==========================================================

    @staticmethod
    def remover_cancelados(dados):

        return [
            item for item in dados
            if not item.get("cancelado", False)
        ]
