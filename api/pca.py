"""
Consultas ao Plano de Contratação Anual (PCA) - API PNCP

Autor: SCM_GOV
"""

from api.client import pncp
from api.endpoints import (
    PCA,
    PCA_USUARIO,
    PCA_ATUALIZACAO,
)


# ==========================================================
# PCA POR ANO
# ==========================================================

def consultar(
    ano_pca: int,
    codigo_classificacao: str = None,
    pagina: int = 1,
    tamanho_pagina: int = 50,
):
    """
    Consulta itens do Plano de Contratação Anual (PCA).

    Parâmetros:
        ano_pca: Ano do PCA
        codigo_classificacao: Código da classificação superior (opcional)
        pagina: Número da página
        tamanho_pagina: Quantidade de registros por página
    """

    params = {
        "anoPca": ano_pca,
        "pagina": pagina,
        "tamanhoPagina": tamanho_pagina,
    }

    if codigo_classificacao:
        params["codigoClassificacaoSuperior"] = codigo_classificacao

    return pncp.get(
        PCA,
        params=params
    )


# ==========================================================
# PCA POR USUÁRIO
# ==========================================================

def consultar_usuario(
    ano_pca: int,
    id_usuario: int,
    codigo_classificacao: str = None,
    pagina: int = 1,
    tamanho_pagina: int = 50,
):
    """
    Consulta PCA por usuário.

    Geralmente utilizado por órgãos públicos.
    """

    params = {
        "anoPca": ano_pca,
        "idUsuario": id_usuario,
        "pagina": pagina,
        "tamanhoPagina": tamanho_pagina,
    }

    if codigo_classificacao:
        params["codigoClassificacaoSuperior"] = codigo_classificacao

    return pncp.get(
        PCA_USUARIO,
        params=params
    )


# ==========================================================
# PCA POR DATA DE ATUALIZAÇÃO
# ==========================================================

def atualizados(
    data_inicial: str,
    data_final: str,
    pagina: int = 1,
    tamanho_pagina: int = 50,
):
    """
    Consulta os PCAs atualizados em determinado período.

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
        PCA_ATUALIZACAO,
        params=params
    )


# ==========================================================
# RESUMO
# ==========================================================

def resumo(
    ano_pca: int,
):
    """
    Retorna a primeira página do PCA.

    Ideal para dashboards.
    """

    return consultar(
        ano_pca=ano_pca,
        pagina=1,
        tamanho_pagina=50
    )
