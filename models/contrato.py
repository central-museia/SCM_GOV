"""
Modelo de Contrato

Autor: SCM_GOV
"""

from dataclasses import dataclass


@dataclass
class Contrato:

    numero: str = ""

    objeto: str = ""

    orgao: str = ""

    contratado: str = ""

    cnpj: str = ""

    valor: float = 0.0

    inicio: str = ""

    fim: str = ""

    situacao: str = ""
