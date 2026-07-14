from api.parser import PNCPParser

resultado = pncp.get(...)

atas = PNCPParser.parse_atas(
    resultado["data"]
)

"""
Consultas de Atas de Registro de Preços - API PNCP

Autor: SCM_GOV
"""

from api.client import pncp
from api.endpoints import (
    ATAS,
    ATAS_ATUALIZACAO,
)


# ==========================================================
# CONSULTAR ATAS POR PERÍODO DE VIGÊNCIA
# ==========================================================

def consultar(
    data_inicial: str,
    data_final: str,
    pagina: int = 1,
    tamanho_pagina: int = 50,
    id_usuario: int = None,
    cnpj: str = None,
    codigo_unidade_administrativa: str = None,
):
    """
    Consulta Atas de Registro de Preço por período de vigência.

    Datas no formato:
        yyyymmdd
    """

    params = {
        "dataInicial": data_inicial,
        "dataFinal": data_final,
        "pagina": pagina,
        "tamanhoPagina": tamanho_pagina,
    }

    if id_usuario:
        params["idUsuario"] = id_usuario

    if cnpj:
        params["cnpj"] = cnpj

    if codigo_unidade_administrativa:
        params["codigoUnidadeAdministrativa"] = codigo_unidade_administrativa

    return pncp.get(
        ATAS,
        params=params
    )


# ==========================================================
# CONSULTAR ATAS POR DATA DE ATUALIZAÇÃO
# ==========================================================

def atualizadas(
    data_inicial: str,
    data_final: str,
    pagina: int = 1,
    tamanho_pagina: int = 50,
):
    """
    Consulta atas pela data de atualização global.

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
        ATAS_ATUALIZACAO,
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
    Retorna apenas a primeira página.

    Ideal para dashboards.
    """

    return consultar(
        data_inicial=data_inicial,
        data_final=data_final,
        pagina=1,
        tamanho_pagina=50
    )


# ==========================================================
# CONSULTAR TODAS AS PÁGINAS
# ==========================================================

def consultar_todas(
    data_inicial: str,
    data_final: str,
    tamanho_pagina: int = 100,
):
    """
    Consulta todas as páginas disponíveis e retorna
    uma única lista com todas as atas encontradas.
    """

    pagina = 1
    todas_atas = []

    while True:

        resposta = consultar(
            data_inicial=data_inicial,
            data_final=data_final,
            pagina=pagina,
            tamanho_pagina=tamanho_pagina
        )

        if not resposta["success"]:
            return resposta

        dados = resposta["data"]

        atas = dados.get("data", [])

        todas_atas.extend(atas)

        paginas_restantes = dados.get("paginasRestantes", 0)

        if paginas_restantes <= 0:
            break

        pagina += 1

    return {
        "success": True,
        "total": len(todas_atas),
        "data": todas_atas
    }
