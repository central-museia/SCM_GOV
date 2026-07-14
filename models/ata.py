"""
Modelo de Ata de Registro de Preço

Autor: SCM_GOV
"""

from dataclasses import dataclass


@dataclass
class Ata:

    numero: str = ""

    ano: int = 0

    objeto: str = ""

    orgao: str = ""

    unidade: str = ""

    vigencia_inicio: str = ""

    vigencia_fim: str = ""

    assinatura: str = ""

    publicacao: str = ""

    cancelada: bool = False

    adesao: bool = False
