from typing import List

from src.calculators.base_calculator import BaseCalculator
from src.models.domain import Parcela, TabelaAmortizacao


class SACCalculator(BaseCalculator):
    
    def calcular(
        self,
        valor_financiado: float,
        taxa_juros_mensal: float,
        prazo_meses: int
    ) -> TabelaAmortizacao:
        self._validar_parametros(valor_financiado, taxa_juros_mensal, prazo_meses)
        
        taxa_decimal = self._converter_taxa_percentual_para_decimal(taxa_juros_mensal)
        
        amortizacao_constante = valor_financiado / prazo_meses
        
        parcelas = self._gerar_tabela(
            valor_financiado,
            amortizacao_constante,
            taxa_decimal,
            prazo_meses
        )
        
        total_pago, total_juros = self._calcular_totais(parcelas)
        
        return TabelaAmortizacao(
            parcelas=parcelas,
            total_pago=total_pago,
            total_juros=total_juros
        )
    
    def _gerar_tabela(
        self,
        saldo_inicial: float,
        amortizacao_constante: float,
        taxa_decimal: float,
        num_parcelas: int
    ) -> List[Parcela]:
        parcelas = []
        saldo_devedor = saldo_inicial
        
        for mes in range(1, num_parcelas + 1):
            juros = saldo_devedor * taxa_decimal
            
            amortizacao = amortizacao_constante
            
            valor_parcela = amortizacao + juros
            
            saldo_devedor -= amortizacao
            
            if mes == num_parcelas:
                saldo_devedor = 0.0
            
            parcela = Parcela(
                numero=mes,
                valor_parcela=valor_parcela,
                valor_juros=juros,
                valor_amortizacao=amortizacao,
                saldo_devedor=saldo_devedor
            )
            
            parcelas.append(parcela)
        
        return parcelas
    
    def calcular_primeira_parcela(
        self,
        valor_financiado: float,
        taxa_juros_mensal: float,
        prazo_meses: int
    ) -> float:
        taxa_decimal = self._converter_taxa_percentual_para_decimal(taxa_juros_mensal)
        amortizacao = valor_financiado / prazo_meses
        juros_primeiro_mes = valor_financiado * taxa_decimal
        
        return amortizacao + juros_primeiro_mes
    
    def calcular_ultima_parcela(
        self,
        valor_financiado: float,
        taxa_juros_mensal: float,
        prazo_meses: int
    ) -> float:

        taxa_decimal = self._converter_taxa_percentual_para_decimal(taxa_juros_mensal)
        amortizacao = valor_financiado / prazo_meses
        
        saldo_antes_ultima = amortizacao
        juros_ultimo_mes = saldo_antes_ultima * taxa_decimal
        
        return amortizacao + juros_ultimo_mes