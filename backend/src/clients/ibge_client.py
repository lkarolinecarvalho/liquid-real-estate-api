"""
Cliente para API do IBGE (Instituto Brasileiro de Geografia e Estatística).
Consulta o IPCA (Índice Nacional de Preços ao Consumidor Amplo).
"""
import logging
import os
from datetime import datetime
from typing import Optional

from src.clients.base_client import BaseHTTPClient
from src.models.domain import Indicador

logger = logging.getLogger(__name__)


class IBGEClient:
    """  
    API utilizada: IBGE - Agregados
    Documentação: https://servicodados.ibge.gov.br/api/docs/agregados
    
    Agregado consultado: 1737 (IPCA)
    Variável: 2266 (IPCA - Variação mensal)
    """

    def __init__(self):
        self.base_url = os.getenv(
            "IBGE_API_URL",
            "https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/last/variaveis/2266"
        )
        self.timeout = int(os.getenv("API_TIMEOUT", "3"))
        self.max_retries = int(os.getenv("API_RETRY_ATTEMPTS", "2"))

        self.http_client = BaseHTTPClient(
            timeout=self.timeout,
            max_retries=self.max_retries
        )

    def buscar_ipca(self) -> Optional[Indicador]:
        try:
            logger.info("Consultando IPCA no IBGE")

            response_data = self.http_client.get(self.base_url)

            if not response_data:
                logger.warning("Resposta vazia do IBGE")
                return None

            try:
                resultado = response_data[0]["resultados"][0]
                serie_data = resultado["series"][0]["serie"]

                periodo = list(serie_data.keys())[-1]
                valor_str = serie_data[periodo]

            except (KeyError, IndexError, TypeError) as e:
                logger.warning(
                    "Formato inesperado na resposta do IBGE",
                    extra={
                        "error": str(e),
                        "response": response_data
                    }
                )
                return None

            try:
                valor = float(valor_str)
            except ValueError:
                logger.error(
                    f"Erro ao converter valor do IPCA: {valor_str}",
                    extra={"periodo": periodo}
                )
                return None

            data_referencia = self._converter_periodo(periodo)

            logger.info(
                "IPCA obtido com sucesso",
                extra={
                    "valor": valor,
                    "periodo": periodo,
                    "data_referencia": data_referencia
                }
            )

            return Indicador(
                tipo="IPCA",
                valor=valor,
                fonte="IBGE",
                data_referencia=data_referencia
            )

        except Exception as e:
            logger.error(
                "Erro ao buscar IPCA",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            return None

    def _converter_periodo(self, periodo: str) -> str:
        try:
            ano = periodo[:4]
            mes = periodo[4:6]
            return f"{ano}-{mes}-01"
        except Exception as e:
            logger.warning(
                f"Erro ao converter período '{periodo}', usando data atual",
                extra={"error": str(e)}
            )
            return datetime.now().strftime("%Y-%m-%d")

    def close(self):
        self.http_client.close()
