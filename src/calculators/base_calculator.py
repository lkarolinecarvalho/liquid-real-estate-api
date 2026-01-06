from abc import ABC, abstractmethod
from typing import List

from src.models.domain import Parcela, TabelaAmortizacao


class BaseCalculator(ABC):    
    @abstractmethod
    def calcular(
        self,
        valor_financiado: float,
        taxa_juros_mensal: float,
        prazo_meses: int
    ) -> TabelaAmortizacao:
        pass
    
    def _converter_taxa_percentual_para_decimal(self, taxa_percentual: float) -> float:
        return taxa_percentual / 100
    
    def _validar_parametros(
        self,
        valor_financiado: float,
        taxa_juros_mensal: float,
        prazo_meses: int
    ) -> None:
        if valor_financiado <= 0:
            raise ValueError("Valor financiado deve ser maior que zero")
        
        if taxa_juros_mensal < 0:
            raise ValueError("Taxa de juros não pode ser negativa")
        
        if prazo_meses <= 0:
            raise ValueError("Prazo deve ser maior que zero")
    
    def _calcular_totais(self, parcelas: List[Parcela]) -> tuple[float, float]:
        total_pago = sum(p.valor_parcela for p in parcelas)
        total_juros = sum(p.valor_juros for p in parcelas)
        
        return total_pago, total_juros