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
# TODAS AS PROPOSTAS (todas as páginas)
# ==========================================================

def consultar_todas_propostas(
    data_inicial: str,
    data_final: str,
    tamanho_pagina: int = 100,
):
    """
    Percorre todas as páginas de propostas abertas e retorna
    uma lista única com todos os registros brutos do PNCP.
    """

    pagina = 1
    todas = []

    while True:

        resposta = propostas_abertas(
            data_inicial=data_inicial,
            data_final=data_final,
            pagina=pagina,
            tamanho_pagina=tamanho_pagina
        )

        if not resposta.get("success"):
            return resposta

        dados = resposta["data"]

        itens = dados.get("data", [])

        todas.extend(itens)

        paginas_restantes = dados.get("paginasRestantes", 0)

        if paginas_restantes <= 0:
            break

        pagina += 1

    return {
        "success": True,
        "total": len(todas),
        "data": todas
    }
