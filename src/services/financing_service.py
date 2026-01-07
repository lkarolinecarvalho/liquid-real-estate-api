import logging
from typing import Literal
from uuid import uuid4

from src.models.requests import SimulationRequest
from src.models.responses import (
    SimulationResponse,
    DadosSimulacao,
    TaxasAplicadas,
    IndicadorEconomico,
    ResultadoFinanciamento,
    DetalheParcela,
    Comparativo,
    Analise,
    ParcelaAmortizacao
)
from src.models.domain import ResultadoCalculo
from src.services.indicator_service import IndicatorService
from src.services.comparison_service import ComparisonService
from src.calculators import CalculatorFactory

logger = logging.getLogger(__name__)


class FinancingService:    
    def __init__(self):
        self.indicator_service = IndicatorService()
        self.comparison_service = ComparisonService()
    
    def simular(self, request: SimulationRequest) -> SimulationResponse:
        request_id = str(uuid4())
        
        logger.info(
            "Iniciando simulação de financiamento",
            extra={
                "request_id": request_id,
                "valor_imovel": request.valor_imovel,
                "prazo_meses": request.prazo_meses,
                "tipo_amortizacao": request.tipo_amortizacao
            }
        )
        
        indicador = self.indicator_service.buscar_indicador_com_fallback()
        
        taxa = self.indicator_service.calcular_taxa_juros(indicador)
        
        resultado = self._calcular_financiamento(request, taxa.taxa_mensal)
        
        comparativo = self.comparison_service.comparar_com_media_nacional(
            taxa.taxa_anual
        )
        
        analise = self.comparison_service.analisar_viabilidade(
            parcela_mensal=resultado.parcela_mensal,
            taxa_aplicada=taxa.taxa_anual,
            taxa_media=comparativo.taxa_media_nacional,
            prazo_meses=request.prazo_meses,
            percentual_juros=resultado.percentual_juros
        )
        
        response = self._montar_resposta(
            request_id=request_id,
            request=request,
            taxa=taxa,
            resultado=resultado,
            comparativo=comparativo,
            analise=analise
        )
        
        logger.info(
            "Simulação concluída com sucesso",
            extra={
                "request_id": request_id,
                "parcela_mensal": resultado.parcela_mensal,
                "taxa_anual": taxa.taxa_anual
            }
        )
        
        return response
    
    def _calcular_financiamento(
        self,
        request: SimulationRequest,
        taxa_mensal: float
    ) -> ResultadoCalculo:
        calculator = CalculatorFactory.create(request.tipo_amortizacao)
        
        valor_financiado = request.valor_financiado()
        
        tabela = calculator.calcular(
            valor_financiado=valor_financiado,
            taxa_juros_mensal=taxa_mensal,
            prazo_meses=request.prazo_meses
        )
        
        parcela_mensal = tabela.primeira_parcela().valor_parcela
        
        from src.models.domain import TaxaJuros, Indicador
        
        indicador = self.indicator_service.buscar_indicador_com_fallback()
        taxa_completa = self.indicator_service.calcular_taxa_juros(indicador)
        
        return ResultadoCalculo(
            tabela=tabela,
            parcela_mensal=parcela_mensal,
            taxa=taxa_completa
        )
    
    def _montar_resposta(
        self,
        request_id: str,
        request: SimulationRequest,
        taxa: "TaxaJuros",
        resultado: ResultadoCalculo,
        comparativo: Comparativo,
        analise: Analise
    ) -> SimulationResponse:
        simulacao = DadosSimulacao(
            valor_imovel=request.valor_imovel,
            entrada=request.entrada,
            valor_financiado=request.valor_financiado(),
            prazo_meses=request.prazo_meses,
            tipo_amortizacao=request.tipo_amortizacao
        )
        
        taxas = TaxasAplicadas(
            indicador=IndicadorEconomico(
                indicador_usado=taxa.indicador.tipo,
                valor_indicador=taxa.indicador.valor,
                fonte=taxa.indicador.fonte,
                data_referencia=taxa.indicador.data_referencia
            ),
            taxa_juros_anual=round(taxa.taxa_anual, 2),
            taxa_juros_mensal=round(taxa.taxa_mensal, 4),
            formula_aplicada=taxa.formula
        )
        
        primeira = resultado.tabela.primeira_parcela()
        ultima = resultado.tabela.ultima_parcela()
        
        resultado_financiamento = ResultadoFinanciamento(
            parcela_mensal=round(resultado.parcela_mensal, 2),
            total_pago=round(resultado.tabela.total_pago, 2),
            juros_totais=round(resultado.tabela.total_juros, 2),
            percentual_juros=round(resultado.percentual_juros, 2),
            primeira_parcela=DetalheParcela(
                valor=round(primeira.valor_parcela, 2),
                juros=round(primeira.valor_juros, 2),
                amortizacao=round(primeira.valor_amortizacao, 2),
                saldo_devedor=round(primeira.saldo_devedor, 2)
            ),
            ultima_parcela=DetalheParcela(
                valor=round(ultima.valor_parcela, 2),
                juros=round(ultima.valor_juros, 2),
                amortizacao=round(ultima.valor_amortizacao, 2),
                saldo_devedor=round(ultima.saldo_devedor, 2)
            )
        )
        
        resumo = resultado.tabela.resumo(num_pontos=12)
        tabela_resumida = [
            ParcelaAmortizacao(**parcela.to_dict())
            for parcela in resumo
        ]
        
        return SimulationResponse(
            request_id=request_id,
            simulacao=simulacao,
            taxas=taxas,
            resultado=resultado_financiamento,
            comparativo=comparativo,
            analise=analise,
            tabela_amortizacao_resumida=tabela_resumida
        )
    
    def close(self):
        self.indicator_service.close()