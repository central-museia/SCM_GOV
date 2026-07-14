"""
Modelo de Estatísticas

Autor: SCM_GOV
"""

from dataclasses import dataclass


@dataclass
class Estatistica:

    total: int = 0

    oportunidades: int = 0

    canceladas: int = 0

    score_medio: float = 0.0
