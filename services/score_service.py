"""
Score SCM

Calcula a aderência de uma licitação ao perfil da SCM.

Autor: SCM_GOV
"""

import json
from pathlib import Path


class ScoreService:

    def __init__(self):

        self.cnaes = self._carregar_json("assets/cnaes.json")
        self.palavras = self._carregar_json("assets/palavras_chave.json")
        self.regioes = self._carregar_json("assets/regioes_rj.json")

    # ----------------------------------------------------------
    # UTIL
    # ----------------------------------------------------------

    @staticmethod
    def _carregar_json(caminho):

        arquivo = Path(caminho)

        if not arquivo.exists():
            return {}

        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)

    # ----------------------------------------------------------
    # REGIÃO
    # ----------------------------------------------------------

    def score_regiao(self, municipio):

        if not municipio:
            return 0

        municipio = municipio.lower()

        for regiao in self.regioes:

            municipios = [
                m.lower()
                for m in regiao["municipios"]
            ]

            if municipio in municipios:
                return 30

        return 0

    # ----------------------------------------------------------
    # PALAVRAS-CHAVE
    # ----------------------------------------------------------

    def score_palavras(self, texto):

        if not texto:
            return 0

        texto = texto.lower()

        pontos = 0

        for categoria in self.palavras.values():

            for palavra in categoria:

                if palavra.lower() in texto:

                    pontos += 4

        return min(pontos, 40)

   # ----------------------------------------------------------
    # CNAE
    # ----------------------------------------------------------

    def score_cnae(self, texto):

        if not texto:
            return 0

        texto = texto.lower()

        pontos = 0

        for item in self.cnaes:

            descricao = item.get("descricao", "")

            if not descricao:
                continue

            # Quebra a descrição em palavras significativas (>3 letras)
            # e verifica se alguma aparece no objeto da licitação
            palavras_descricao = [
                p.strip(".,()/")
                for p in descricao.lower().split()
                if len(p) > 3
            ]

            if any(palavra in texto for palavra in palavras_descricao):

                pontos += 10 if item.get("principal") else 5

        return min(pontos, 20)

    # ----------------------------------------------------------
    # PROPOSTA ABERTA
    # ----------------------------------------------------------

    @staticmethod
    def score_proposta(aberta):

        return 10 if aberta else 0

    # ----------------------------------------------------------
    # SCORE FINAL
    # ----------------------------------------------------------

    def calcular(self, licitacao):

        texto = licitacao.get("objeto", "")

        municipio = licitacao.get("municipio", "")

        proposta = licitacao.get(
            "recebimento_proposta",
            False
        )

        score = (
            self.score_regiao(municipio)
            + self.score_palavras(texto)
            + self.score_cnae(texto)
            + self.score_proposta(proposta)
        )

        return min(score, 100)

    # ----------------------------------------------------------
    # CLASSIFICAÇÃO
    # ----------------------------------------------------------

    @staticmethod
    def classificacao(score):

        if score >= 85:
            return "Excelente"

        if score >= 70:
            return "Alta"

        if score >= 50:
            return "Média"

        if score >= 30:
            return "Baixa"

        return "Descartar"
