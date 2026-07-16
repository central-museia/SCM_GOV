"""
Serviço de consultas ao PNCP

Autor: SCM_GOV
"""

from api.atas import consultar as consultar_atas
from api.contratacoes import propostas_abertas
from api.contratos import publicados
from api.pca import consultar as consultar_pca


class ConsultaService:

    @staticmethod
    def atas(
        data_inicial,
        data_final,
        pagina=1,
        tamanho_pagina=50
    ):

        return consultar_atas(
            data_inicial=data_inicial,
            data_final=data_final,
            pagina=pagina,
            tamanho_pagina=tamanho_pagina
        )

    @staticmethod
    def licitacoes(
        data_inicial,
        data_final,
        pagina=1,
        tamanho_pagina=50
    ):

        return propostas_abertas(
            data_inicial=data_inicial,
            data_final=data_final,
            pagina=pagina,
            tamanho_pagina=tamanho_pagina
        )

    @staticmethod
    def contratos(
        data_inicial,
        data_final,
        pagina=1,
        tamanho_pagina=50
    ):

        return publicados(
            data_inicial=data_inicial,
            data_final=data_final,
            pagina=pagina,
            tamanho_pagina=tamanho_pagina
        )

    @staticmethod
    def pca(
        ano,
        pagina=1,
        tamanho_pagina=50
    ):

        return consultar_pca(
            ano_pca=ano,
            pagina=pagina,
            tamanho_pagina=tamanho_pagina
        )

import requests
import pandas as pd

BASE_URL = "https://pncp.gov.br/api/consulta/v1"


def consultar_licitacoes(
    pagina=1,
    tamanho=50,
    uf="RJ",
    palavra=""
):

    endpoint = f"{BASE_URL}/contratacoes/publicacao"

    params = {
        "pagina": pagina,
        "tamanhoPagina": tamanho,
        "uf": uf,
        "status": "RECEBENDO_PROPOSTA"
    }

    if palavra:
        params["objeto"] = palavra

    response = requests.get(
        endpoint,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    dados = response.json()

    registros = []

    for item in dados.get("data", []):

        registros.append({

            "Número": item.get("numeroControlePNCP"),

            "Objeto": item.get("objetoCompra"),

            "Órgão": item.get("orgaoEntidade", {}).get("razaoSocial"),

            "Município": item.get("unidadeOrgao", {}).get("municipioNome"),

            "UF": item.get("unidadeOrgao", {}).get("ufSigla"),

            "Modalidade": item.get("modalidadeNome"),

            "Valor Estimado": item.get("valorTotalEstimado"),

            "Data Publicação": item.get("dataPublicacaoPncp"),

            "Encerramento": item.get("dataEncerramentoProposta"),

            "Link": item.get("linkSistemaOrigem")

        })

    return pd.DataFrame(registros)
