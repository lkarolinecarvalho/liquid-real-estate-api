"""
Módulo de modelos de dados.
"""
from src.models.requests import SimulationRequest
from src.models.responses import (
    SimulationResponse,
    ErrorResponse,
    DadosSimulacao,
    TaxasAplicadas,
    ResultadoFinanciamento,
    Comparativo,
    Analise
)
from src.models.domain import (
    Indicador,
    TaxaJuros,
    Parcela,
    TabelaAmortizacao,
    ResultadoCalculo
)

__all__ = [
    # Requests
    "SimulationRequest",
    
    # Responses
    "SimulationResponse",
    "ErrorResponse",
    "DadosSimulacao",
    "TaxasAplicadas",
    "ResultadoFinanciamento",
    "Comparativo",
    "Analise",
    
    # Domain
    "Indicador",
    "TaxaJuros",
    "Parcela",
    "TabelaAmortizacao",
    "ResultadoCalculo"
]