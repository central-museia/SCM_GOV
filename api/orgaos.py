"""
Consultas de Órgãos - API PNCP

Autor: SCM_GOV
"""

from api.client import pncp
from api.endpoints import CONTRATACAO


# ==========================================================
# CONSULTAR CONTRATAÇÃO DE UM ÓRGÃO
# ==========================================================

def consultar_compra(
    cnpj: str,
    ano: int,
    sequencial: int,
):
    """
    Consulta uma contratação específica de um órgão.

    Parâmetros:
        cnpj: CNPJ do órgão
        ano: Ano da contratação
        sequencial: Número sequencial da compra
    """

    endpoint = CONTRATACAO.format(
        cnpj=cnpj,
        ano=ano,
        sequencial=sequencial
    )

    return pncp.get(endpoint)


# ==========================================================
# DADOS DO ÓRGÃO
# ==========================================================

def dados_orgao(
    cnpj: str,
    ano: int,
    sequencial: int,
):
    """
    Retorna apenas os dados do órgão.
    """

    resposta = consultar_compra(
        cnpj,
        ano,
        sequencial
    )

    if not resposta["success"]:
        return resposta

    dados = resposta["data"]

    return {
        "success": True,
        "orgao": dados.get("orgaoEntidade", {}),
        "unidade": dados.get("unidadeOrgao", {})
    }


# ==========================================================
# RESUMO DO ÓRGÃO
# ==========================================================

def resumo(
    cnpj: str,
    ano: int,
    sequencial: int,
):
    """
    Retorna um resumo simplificado do órgão.
    """

    resposta = dados_orgao(
        cnpj,
        ano,
        sequencial
    )

    if not resposta["success"]:
        return resposta

    orgao = resposta["orgao"]
    unidade = resposta["unidade"]

    return {
        "success": True,
        "cnpj": orgao.get("cnpj"),
        "nome": orgao.get("razaoSocial"),
        "esfera": orgao.get("esferaId"),
        "poder": orgao.get("poderId"),
        "municipio": unidade.get("municipioNome"),
        "uf": unidade.get("ufSigla"),
        "codigo_unidade": unidade.get("codigoUnidade")
    }
