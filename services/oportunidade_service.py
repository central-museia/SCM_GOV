"""
Serviço de Oportunidades

Responsável por identificar oportunidades para a SCM.

Autor: SCM_GOV
"""

from services.score_service import ScoreService


class OportunidadeService:

    SCORE_MINIMO = 70

    def __init__(self):
        self.score_service = ScoreService()

    # ==========================================================
    # VERIFICAR OPORTUNIDADE
    # ==========================================================

    def analisar(self, licitacao):

        score = self.score_service.calcular(licitacao)

        oportunidade = {
            "score": score,
            "classificacao": self.score_service.classificacao(score),
            "oportunidade": True,
            "motivos": []
        }

        # ------------------------------------------
        # Score
        # ------------------------------------------

        if score < self.SCORE_MINIMO:

            oportunidade["oportunidade"] = False

            oportunidade["motivos"].append(
                "Score abaixo do mínimo."
            )

        # ------------------------------------------
        # Cancelada
        # ------------------------------------------

        if licitacao.get("cancelado", False):

            oportunidade["oportunidade"] = False

            oportunidade["motivos"].append(
                "Licitação cancelada."
            )

        # ------------------------------------------
        # Objeto
        # ------------------------------------------

        if not licitacao.get("objeto"):

            oportunidade["oportunidade"] = False

            oportunidade["motivos"].append(
                "Objeto da contratação não informado."
            )

        return oportunidade

    # ==========================================================
    # LISTA DE OPORTUNIDADES
    # ==========================================================

    def filtrar(self, licitacoes):

        oportunidades = []

        for licitacao in licitacoes:

            resultado = self.analisar(licitacao)

            if resultado["oportunidade"]:

                licitacao["score"] = resultado["score"]

                licitacao["classificacao"] = resultado["classificacao"]

                oportunidades.append(licitacao)

        return oportunidades

    # ==========================================================
    # QUANTIDADE
    # ==========================================================

    def quantidade(self, licitacoes):

        return len(self.filtrar(licitacoes))
