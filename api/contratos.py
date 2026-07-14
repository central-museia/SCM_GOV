"""
Consultas de Contratos/Empenhos - API PNCP

Autor: SCM_GOV
"""

from api.client import pncp
from api.endpoints import (
    CONTRATOS,
    CONTRATOS_ATUALIZACAO,
)


# ==========================================================
# CONTRATOS POR DATA DE PUBLICAÇÃO
# ==========================================================

def publicados(
    data_inicial: str,
    data_final: str,
    pagina: int = 1,
    tamanho_pagina: int = 50,
):
    """
    Consulta contratos publicados.

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
        CONTRATOS,
        params=params
    )


# ==========================================================
# CONTRATOS POR DATA DE ATUALIZAÇÃO
# ==========================================================

def atualizados(
    data_inicial: str,
    data_final: str,
    pagina: int = 1,
    tamanho_pagina: int = 50,
):
    """
    Consulta contratos atualizados.

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
        CONTRATOS_ATUALIZACAO,
        params=params
    )


# ==========================================================
# RESUMO
# ==========================================================

def resumo(
    data_inicial: str,
    data_final: str,
):
    """
    Retorna apenas a primeira página da consulta de contratos.
    Ideal para dashboards e indicadores.
    """

    return publicados(
        data_inicial=data_inicial,
        data_final=data_final,
        pagina=1,
        tamanho_pagina=50
    )
