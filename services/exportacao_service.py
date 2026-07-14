"""
Serviço de Exportação

Responsável por exportar os dados do SCM_GOV.

Autor: SCM_GOV
"""

from pathlib import Path

import pandas as pd


class ExportacaoService:

    # ==========================================================
    # DATAFRAME
    # ==========================================================

    @staticmethod
    def dataframe(dados):

        return pd.DataFrame(dados)

    # ==========================================================
    # CSV
    # ==========================================================

    @staticmethod
    def csv(
        dados,
        arquivo="licitacoes.csv",
        pasta="exports"
    ):

        Path(pasta).mkdir(
            parents=True,
            exist_ok=True
        )

        caminho = Path(pasta) / arquivo

        df = pd.DataFrame(dados)

        df.to_csv(
            caminho,
            index=False,
            encoding="utf-8-sig",
            sep=";"
        )

        return caminho

    # ==========================================================
    # EXCEL
    # ==========================================================

    @staticmethod
    def excel(
        dados,
        arquivo="licitacoes.xlsx",
        pasta="exports"
    ):

        Path(pasta).mkdir(
            parents=True,
            exist_ok=True
        )

        caminho = Path(pasta) / arquivo

        df = pd.DataFrame(dados)

        with pd.ExcelWriter(
            caminho,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                sheet_name="Licitações",
                index=False
            )

        return caminho

    # ==========================================================
    # JSON
    # ==========================================================

    @staticmethod
    def json(
        dados,
        arquivo="licitacoes.json",
        pasta="exports"
    ):

        Path(pasta).mkdir(
            parents=True,
            exist_ok=True
        )

        caminho = Path(pasta) / arquivo

        df = pd.DataFrame(dados)

        df.to_json(
            caminho,
            orient="records",
            force_ascii=False,
            indent=4
        )

        return caminho
