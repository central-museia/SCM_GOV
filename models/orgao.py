"""
Modelo de Órgão Público

Autor: SCM_GOV
"""

from dataclasses import dataclass


@dataclass
class Orgao:

    cnpj: str = ""

    nome: str = ""

    esfera: str = ""

    poder: str = ""

    municipio: str = ""

    uf: str = ""

    codigo_unidade: str = ""
