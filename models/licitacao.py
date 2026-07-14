"""
Modelo de Licitação

Autor: SCM_GOV
"""

from dataclasses import dataclass


@dataclass
class Licitacao:

    numero: str = ""

    objeto: str = ""

    orgao: str = ""

    municipio: str = ""

    uf: str = ""

    modalidade: str = ""

    valor: float = 0.0

    abertura: str = ""

    encerramento: str = ""

    situacao: str = ""

    link: str = ""
