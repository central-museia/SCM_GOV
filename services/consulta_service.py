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

import pandas as pd


def consultar_licitacoes(
    estado,
    palavra_chave,
    quantidade
):

    # EXEMPLO
    # depois substituímos pela chamada da API PNCP

    dados = [

        {
            "Objeto": "Reforma Predial",
            "Órgão": "Prefeitura do Rio",
            "Município": "Rio de Janeiro",
            "UF": "RJ",
            "Valor": 1250000,
            "Data Abertura": "15/07/2026",
            "Situação": "Aberta"
        },

        {
            "Objeto": "Manutenção Civil",
            "Órgão": "UERJ",
            "Município": "Rio de Janeiro",
            "UF": "RJ",
            "Valor": 840000,
            "Data Abertura": "20/07/2026",
            "Situação": "Aberta"
        }

    ]

    return pd.DataFrame(dados)
