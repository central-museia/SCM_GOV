"""
Consultas de Contratações - API PNCP

Autor: SCM_GOV
"""

from api.client import pncp
from api.endpoints import (
    CONTRATACAO,
    CONTRATACOES_PUBLICACAO,
    CONTRATACOES_PROPOSTA,
    CONTRATACOES_ATUALIZACAO,
)


# ==========================================================
# CONTRATAÇÕES COM RECEBIMENTO DE PROPOSTAS ABERTO
# ==========================================================

def propostas_abertas(
    data_inicial: str,
    data_final: str,
    pagina: int = 1,
    tamanho_pagina: int = 50,
):
    """
    Consulta contratações com recebimento de propostas aberto.

    Datas no formato:
    yyyymmdd
    """

    params = {
        "dataInicial": data_inicial,
        "dataFinal": data_final,
        "pagina": pagina,
        "tamanhoPagina": tamanho_pagina,
    }

    return pncp.get(
        CONTRATACOES_PROPOSTA,
        params=params
    )


# ==========================================================
# CONTRATAÇÕES POR DATA DE PUBLICAÇÃO
# ==========================================================

def publicacoes(
    data_inicial: str,
    data_final: str,
    pagina: int = 1,
    tamanho_pagina: int = 50,
):

    params = {
        "dataInicial": data_inicial,
        "dataFinal": data_final,
        "pagina": pagina,
        "tamanhoPagina": tamanho_pagina,
    }

    return pncp.get(
        CONTRATACOES_PUBLICACAO,
        params=params
    )


# ==========================================================
# CONTRATAÇÕES POR ATUALIZAÇÃO
# ==========================================================

def atualizacoes(
    data_inicial: str,
    data_final: str,
    pagina: int = 1,
    tamanho_pagina: int = 50,
):

    params = {
        "dataInicial": data_inicial,
        "dataFinal": data_final,
        "pagina": pagina,
        "tamanhoPagina": tamanho_pagina,
    }

    return pncp.get(
        CONTRATACOES_ATUALIZACAO,
        params=params
    )


# ==========================================================
# CONSULTA DE UMA CONTRATAÇÃO ESPECÍFICA
# ==========================================================

def consultar(
    cnpj: str,
    ano: int,
    sequencial: int,
):
    """
    Consulta uma contratação específica.

    Exemplo:

    cnpj = "00394460000141"

    ano = 2026

    sequencial = 15
    """

    endpoint = CONTRATACAO.format(
        cnpj=cnpj,
        ano=ano,
        sequencial=sequencial,
    )

    return pncp.get(endpoint)


# ==========================================================
# CONSULTAR TODAS AS PÁGINAS (PROPOSTAS ABERTAS)
# ==========================================================

def consultar_todas_propostas(
    data_inicial: str,
    data_final: str,
    tamanho_pagina: int = 50,
    max_paginas: int = 20,
):
    """
    Percorre todas as páginas de contratações com propostas abertas
    no período informado e retorna uma lista única e "achatada"
    de registros brutos do PNCP.

    O limite `max_paginas` evita consultas excessivas à API em
    períodos muito longos (20 páginas x 50 registros = até 1000
    licitações por consulta).
    """

    pagina = 1
    todas = []

    while pagina <= max_paginas:

        resposta = propostas_abertas(
            data_inicial=data_inicial,
            data_final=data_final,
            pagina=pagina,
            tamanho_pagina=tamanho_pagina,
        )

        if not resposta.get("success"):
            return resposta

        dados = resposta.get("data", {}) or {}

        registros = dados.get("data", [])

        todas.extend(registros)

        paginas_restantes = dados.get("paginasRestantes", 0)

        if not paginas_restantes:
            break

        pagina += 1

    return {
        "success": True,
        "total": len(todas),
        "data": todas,
    }


# ==========================================================
# RESUMO
# ==========================================================

def resumo(
    data_inicial: str,
    data_final: str,
):
    """
    Retorna apenas a primeira página da consulta de contratações.
    Ideal para dashboards e indicadores.
    """

    return propostas_abertas(
        data_inicial=data_inicial,
        data_final=data_final,
        pagina=1,
        tamanho_pagina=50
    )
