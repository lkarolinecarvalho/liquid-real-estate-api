import logging
import os
from datetime import datetime
from typing import Optional

from src.clients.base_client import BaseHTTPClient
from src.models.domain import Indicador

logger = logging.getLogger(__name__)


class BacenClient:
    """
    API utilizada: BCB - SGS (Sistema Gerenciador de Séries Temporais)
    Documentação: https://www3.bcb.gov.br/sgspub/

    Série consultada: 432 (Taxa Selic)
    """

    def __init__(self):
        self.base_url = os.getenv(
            "BACEN_API_URL",
            "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
        )
        self.timeout = int(os.getenv("API_TIMEOUT", "3"))
        self.max_retries = int(os.getenv("API_RETRY_ATTEMPTS", "2"))

        self.http_client = BaseHTTPClient(
            timeout=self.timeout,
            max_retries=self.max_retries
        )

    def buscar_selic(self) -> Optional[Indicador]:
        try:
            logger.info("Consultando taxa SELIC no Banco Central")

            response_data = self.http_client.get(self.base_url)

            if not response_data:
                logger.warning("Resposta vazia do Banco Central")
                return None

            if not isinstance(response_data, list) or len(response_data) == 0:
                logger.warning(
                    "Formato inesperado na resposta do Banco Central",
                    extra={"response": response_data}
                )
                return None

            dados = response_data[0]

            valor_str = dados.get("valor", "0")
            data_str = dados.get("data", "")

            try:
                valor = float(valor_str)
            except ValueError:
                logger.error(
                    f"Erro ao converter valor da SELIC: {valor_str}",
                    extra={"dados": dados}
                )
                return None

            data_referencia = self._converter_data(data_str)

            logger.info(
                "SELIC obtida com sucesso",
                extra={
                    "valor": valor,
                    "data_referencia": data_referencia
                }
            )

            return Indicador(
                tipo="SELIC",
                valor=valor,
                fonte="Banco Central do Brasil",
                data_referencia=data_referencia
            )

        except Exception as e:
            logger.error(
                "Erro ao buscar SELIC",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            return None

    def _converter_data(self, data_str: str) -> str:
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y")
            return data_obj.strftime("%Y-%m-%d")
        except Exception as e:
            logger.warning(
                f"Erro ao converter data '{data_str}', usando data atual",
                extra={"error": str(e)}
            )
            return datetime.now().strftime("%Y-%m-%d")

    def close(self):
        self.http_client.close()
