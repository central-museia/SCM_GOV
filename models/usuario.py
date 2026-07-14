"""
Modelo de Usuário

Autor: SCM_GOV
"""

from dataclasses import dataclass


@dataclass
class Usuario:

    id: int = 0

    nome: str = ""

    email: str = ""

    perfil: str = "Administrador"

    ativo: bool = True
