"""
Modelo de Oportunidade

Autor: SCM_GOV
"""

from dataclasses import dataclass


@dataclass
class Oportunidade:

    score: int = 0

    classificacao: str = ""

    oportunidade: bool = False

    motivo: str = ""
