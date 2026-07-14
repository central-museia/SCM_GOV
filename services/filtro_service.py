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

import json

# Adicione isso dentro da sua classe FiltroService
    @staticmethod
    def filtrar_por_especificacoes_scm(dados):
        """
        Filtro mestre: Aplica CNAEs e Palavras-chave dos seus assets
        para retornar apenas o que interessa para a SCM.
        """
        # Carrega assets
        with open("assets/cnaes.json", "r", encoding="utf-8") as f:
            cnaes_scm = [item['codigo'] for item in json.load(f)]
            
        with open("assets/palavras_chave.json", "r", encoding="utf-8") as f:
            palavras_chave = json.load(f)

        def eh_relevante(item):
            objeto = item.get("objeto", "").lower()
            # Verifica se o objeto contém algum CNAE ou palavra-chave
            match_cnae = any(cnae in objeto for cnae in cnaes_scm)
            match_palavra = any(p.lower() in objeto for p in palavras_chave)
            return match_cnae or match_palavra

        return [item for item in dados if eh_relevante(item)]
