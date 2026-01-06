from typing import List

from src.calculators.base_calculator import BaseCalculator
from src.models.domain import Parcela, TabelaAmortizacao


class PRICECalculator(BaseCalculator):
    def calcular(
        self,
        valor_financiado: float,
        taxa_juros_mensal: float,
        prazo_meses: int
    ) -> TabelaAmortizacao:
        self._validar_parametros(valor_financiado, taxa_juros_mensal, prazo_meses)
   
        taxa_decimal = self._converter_taxa_percentual_para_decimal(taxa_juros_mensal)
        
        parcela_fixa = self._calcular_parcela_price(
            valor_financiado,
            taxa_decimal,
            prazo_meses
        )
        
        parcelas = self._gerar_tabela(
            valor_financiado,
            parcela_fixa,
            taxa_decimal,
            prazo_meses
        )
        
        total_pago, total_juros = self._calcular_totais(parcelas)
        
        return TabelaAmortizacao(
            parcelas=parcelas,
            total_pago=total_pago,
            total_juros=total_juros
        )
    
    def _calcular_parcela_price(
        self,
        valor_presente: float,
        taxa_decimal: float,
        num_parcelas: int
    ) -> float:
        if taxa_decimal == 0:
            return valor_presente / num_parcelas
        
        fator = (1 + taxa_decimal) ** num_parcelas
        
        parcela = valor_presente * (taxa_decimal * fator) / (fator - 1)
        
        return parcela
    
    def _gerar_tabela(
        self,
        saldo_inicial: float,
        parcela_fixa: float,
        taxa_decimal: float,
        num_parcelas: int
    ) -> List[Parcela]:
        parcelas = []
        saldo_devedor = saldo_inicial
        
        for mes in range(1, num_parcelas + 1):
            juros = saldo_devedor * taxa_decimal
            
            amortizacao = parcela_fixa - juros
            
            saldo_devedor -= amortizacao
            
            if mes == num_parcelas:
                saldo_devedor = 0.0
            
            parcela = Parcela(
                numero=mes,
                valor_parcela=parcela_fixa,
                valor_juros=juros,
                valor_amortizacao=amortizacao,
                saldo_devedor=saldo_devedor
            )
            
            parcelas.append(parcela)
        
        return parcelas