"""
Score SCM

Calcula a aderência de uma licitação ao perfil da SCM.

Autor: SCM_GOV
"""

import json
import re
from pathlib import Path


class ScoreService:

    def __init__(self):

        self.cnaes = self._carregar_json("assets/cnaes.json")
        self.palavras = self._carregar_json("assets/palavras_chave.json")
        self.regioes = self._carregar_json("assets/regioes_rj.json") or self._carregar_json("assets/estados.json")

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

    @staticmethod
    def _palavras_relevantes(texto, minimo=4):
        """
        Extrai da descrição do CNAE apenas as palavras "significativas"
        (ignora preposições/artigos curtos) para comparar com o objeto
        da licitação.
        """

        palavras = re.findall(r"[A-Za-zÀ-ÿ]+", texto.lower())

        return [p for p in palavras if len(p) >= minimo]

    # ----------------------------------------------------------
    # REGIÃO
    # ----------------------------------------------------------

    def score_regiao(self, municipio):

        if not municipio:
            return 0

        municipio = municipio.lower()

        regioes = self.regioes if isinstance(self.regioes, list) else []

        for regiao in regioes:

            municipios = [
                m.lower()
                for m in regiao.get("municipios", [])
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

    def palavras_compativeis(self, texto):
        """
        Retorna a lista (sem repetição) de palavras-chave cadastradas
        que aparecem no objeto da licitação.
        """

        if not texto:
            return []

        texto = texto.lower()

        encontradas = []

        for categoria in self.palavras.values():

            for palavra in categoria:

                if palavra.lower() in texto and palavra not in encontradas:

                    encontradas.append(palavra)

        return encontradas

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

            palavras_chave = item.get("palavras_chave") or self._palavras_relevantes(descricao)

            if any(palavra.lower() in texto for palavra in palavras_chave):

                pontos += 5

        return min(pontos, 20)

    def cnaes_compativeis(self, texto):
        """
        Retorna os CNAEs da SCM (código + descrição) cuja descrição
        tem alguma palavra relevante presente no objeto da licitação.
        """

        if not texto:
            return []

        texto = texto.lower()

        encontrados = []

        for item in self.cnaes:

            descricao = item.get("descricao", "")

            palavras_chave = item.get("palavras_chave") or self._palavras_relevantes(descricao)

            if any(palavra.lower() in texto for palavra in palavras_chave):

                encontrados.append(item)

        return encontrados

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

    def fatores(self, licitacao):
        """
        Retorna o detalhamento do score por fator, usado para exibir
        a "explicação" da pontuação (Nível 3 - Score SCM).
        """

        texto = licitacao.get("objeto", "")

        municipio = licitacao.get("municipio", "")

        proposta = licitacao.get("recebimento_proposta", False)

        return {
            "Região de atuação": self.score_regiao(municipio),
            "Palavras-chave": self.score_palavras(texto),
            "CNAE": self.score_cnae(texto),
            "Proposta em aberto": self.score_proposta(proposta),
        }

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
