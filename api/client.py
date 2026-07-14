"""
Cliente HTTP da API do Portal Nacional de Contratações Públicas (PNCP)

Autor: SCM_GOV
"""

from typing import Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from api.endpoints import BASE_URL


class PNCPClient:
    """
    Cliente HTTP para comunicação com a API do PNCP.
    """

    def __init__(
        self,
        timeout: int = 30,
        retries: int = 3,
        backoff_factor: float = 1.0,
    ):

        self.base_url = BASE_URL
        self.timeout = timeout

        self.session = requests.Session()

        retry = Retry(
            total=retries,
            connect=retries,
            read=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[
                429,
                500,
                502,
                503,
                504,
            ],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry)

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "SCM_GOV/1.0",
            }
        )

    # ---------------------------------------------------------
    # GET
    # ---------------------------------------------------------

    def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
    ) -> Dict:

        url = f"{self.base_url}{endpoint}"

        try:

            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout,
            )

            response.raise_for_status()

            if response.status_code == 204:
                return {
                    "success": True,
                    "data": [],
                    "message": "Nenhum registro encontrado."
                }

            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json(),
            }

        except requests.exceptions.HTTPError as e:

            return {
                "success": False,
                "status_code": response.status_code,
                "message": str(e),
            }

        except requests.exceptions.ConnectionError:

            return {
                "success": False,
                "message": "Erro de conexão com o PNCP.",
            }

        except requests.exceptions.Timeout:

            return {
                "success": False,
                "message": "Tempo de resposta excedido.",
            }

        except Exception as e:

            return {
                "success": False,
                "message": str(e),
            }


# -------------------------------------------------------------------
# Instância única para todo o projeto
# -------------------------------------------------------------------

pncp = PNCPClient()
