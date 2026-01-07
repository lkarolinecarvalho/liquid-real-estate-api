from dataclasses import dataclass
from typing import List, Literal


@dataclass
class Indicador:    
    tipo: Literal["SELIC", "IPCA", "TAXA_BASE"]
    valor: float
    fonte: str
    data_referencia: str


@dataclass
class TaxaJuros:    
    taxa_anual: float
    taxa_mensal: float
    indicador: Indicador
    formula: str


@dataclass
class Parcela:    
    numero: int
    valor_parcela: float
    valor_juros: float
    valor_amortizacao: float
    saldo_devedor: float
    
    def to_dict(self) -> dict:
        return {
            "mes": self.numero,
            "parcela": round(self.valor_parcela, 2),
            "juros": round(self.valor_juros, 2),
            "amortizacao": round(self.valor_amortizacao, 2),
            "saldo_devedor": round(self.saldo_devedor, 2)
        }


@dataclass
class TabelaAmortizacao:    
    parcelas: List[Parcela]
    total_pago: float
    total_juros: float
    
    def primeira_parcela(self) -> Parcela:
        return self.parcelas[0]
    
    def ultima_parcela(self) -> Parcela:
        return self.parcelas[-1]
    
    def resumo(self, num_pontos: int = 12) -> List[Parcela]:
        total_parcelas = len(self.parcelas)
        if total_parcelas <= num_pontos:
            return self.parcelas
        
        indices = [0]
        
        step = total_parcelas // (num_pontos - 1)
        for i in range(1, num_pontos - 1):
            indices.append(i * step)
        
        indices.append(total_parcelas - 1)
        
        return [self.parcelas[i] for i in indices]


@dataclass
class ResultadoCalculo:
    tabela: TabelaAmortizacao
    parcela_mensal: float
    taxa: TaxaJuros
    
    @property
    def percentual_juros(self) -> float:

        return (self.tabela.total_juros / self.tabela.total_pago) * 100