import logging
import os
from datetime import datetime

from src.clients import BacenClient, IBGEClient
from src.models.domain import Indicador, TaxaJuros

logger = logging.getLogger(__name__)


class IndicatorService:
    """
    Serviço responsável por buscar indicadores econômicos e calcular taxas de juros.

    Estratégia de fallback:
    1. Tenta buscar SELIC (Banco Central) - primário
    2. Se falhar, tenta buscar IPCA (IBGE) - fallback
    3. Se ambos falharem, usa taxa base padrão
    """

    def __init__(self):
        self.taxa_base_anual = float(os.getenv("TAXA_BASE_ANUAL", "10.0"))
        self.fator_ajuste = float(os.getenv("FATOR_AJUSTE", "0.15"))

        self.bacen_client = BacenClient()
        self.ibge_client = IBGEClient()

    def buscar_indicador_com_fallback(self) -> Indicador:
        logger.info("Iniciando busca de indicador econômico")

        selic = self.bacen_client.buscar_selic()
        if selic:
            logger.info(
                "Indicador obtido com sucesso",
                extra={"tipo": "SELIC", "valor": selic.valor, "fonte": selic.fonte},
            )
            return selic

        logger.warning("SELIC indisponível, tentando fallback para IPCA")

        ipca = self.ibge_client.buscar_ipca()
        if ipca:
            logger.info(
                "Indicador obtido via fallback",
                extra={"tipo": "IPCA", "valor": ipca.valor, "fonte": ipca.fonte},
            )
            return ipca

        logger.warning("Todos os indicadores externos falharam, usando taxa base padrão")

        return self._criar_indicador_fallback()

    def calcular_taxa_juros(self, indicador: Indicador) -> TaxaJuros:
        if indicador.tipo == "SELIC":
            taxa_anual = self._calcular_taxa_selic(indicador.valor)
            formula = f"taxa_base({self.taxa_base_anual}%) + (selic({indicador.valor}%) × fator_ajuste({self.fator_ajuste}) × 0.1)"

        elif indicador.tipo == "IPCA":
            taxa_anual = self._calcular_taxa_ipca(indicador.valor)
            formula = f"taxa_base({self.taxa_base_anual}%) + (ipca({indicador.valor}%) × fator_ajuste({self.fator_ajuste}))"

        else:
            taxa_anual = self.taxa_base_anual
            formula = f"taxa_base({self.taxa_base_anual}%) - fallback padrão"

        taxa_anual = self._aplicar_limites(taxa_anual)

        taxa_mensal = self._converter_anual_para_mensal(taxa_anual)

        logger.info(
            "Taxa de juros calculada",
            extra={
                "indicador_tipo": indicador.tipo,
                "indicador_valor": indicador.valor,
                "taxa_anual": taxa_anual,
                "taxa_mensal": taxa_mensal,
            },
        )

        return TaxaJuros(
            taxa_anual=taxa_anual, taxa_mensal=taxa_mensal, indicador=indicador, formula=formula
        )

    def _calcular_taxa_selic(self, selic: float) -> float:
        ajuste = selic * self.fator_ajuste * 0.1
        return self.taxa_base_anual + ajuste

    def _calcular_taxa_ipca(self, ipca: float) -> float:
        ajuste = ipca * self.fator_ajuste
        return self.taxa_base_anual + ajuste

    def _aplicar_limites(self, taxa: float) -> float:
        return max(8.0, min(15.0, taxa))

    def _converter_anual_para_mensal(self, taxa_anual: float) -> float:
        taxa_decimal = taxa_anual / 100
        taxa_mensal_decimal = ((1 + taxa_decimal) ** (1 / 12)) - 1
        taxa_mensal_percentual = taxa_mensal_decimal * 100

        return round(taxa_mensal_percentual, 4)

    def _criar_indicador_fallback(self) -> Indicador:
        return Indicador(
            tipo="TAXA_BASE",
            valor=self.taxa_base_anual,
            fonte="Sistema (fallback)",
            data_referencia=datetime.now().strftime("%Y-%m-%d"),
        )

    def close(self):
        self.bacen_client.close()
        self.ibge_client.close()
