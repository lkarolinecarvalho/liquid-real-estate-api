"""
Módulo de modelos de dados.
"""
from src.models.domain import Indicador, Parcela, ResultadoCalculo, TabelaAmortizacao, TaxaJuros
from src.models.requests import SimulationRequest
from src.models.responses import (
    Analise,
    Comparativo,
    DadosSimulacao,
    ErrorResponse,
    ResultadoFinanciamento,
    SimulationResponse,
    TaxasAplicadas,
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
