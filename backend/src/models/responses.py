from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class IndicadorEconomico(BaseModel):
    indicador_usado: Literal["SELIC", "IPCA", "TAXA_BASE"] = Field(
        description="Tipo de indicador utilizado no cálculo"
    )
    valor_indicador: float = Field(description="Valor do indicador em percentual anual")
    fonte: str = Field(description="Fonte dos dados (ex: Banco Central, IBGE)")
    data_referencia: str = Field(description="Data de referência dos dados no formato YYYY-MM-DD")


class TaxasAplicadas(BaseModel):
    indicador: IndicadorEconomico
    taxa_juros_anual: float = Field(description="Taxa de juros anual aplicada (%)")
    taxa_juros_mensal: float = Field(description="Taxa de juros mensal aplicada (%)")
    formula_aplicada: str = Field(description="Fórmula utilizada no cálculo da taxa")


class DadosSimulacao(BaseModel):
    """Dados da simulação realizada."""

    valor_imovel: float
    entrada: float
    valor_financiado: float
    prazo_meses: int
    tipo_amortizacao: Literal["PRICE", "SAC"]


class DetalheParcela(BaseModel):
    """Detalhes de uma parcela específica."""

    valor: float = Field(description="Valor total da parcela")
    juros: float = Field(description="Valor dos juros")
    amortizacao: float = Field(description="Valor da amortização")
    saldo_devedor: float = Field(description="Saldo devedor após a parcela")


class ResultadoFinanciamento(BaseModel):
    """Resultado do cálculo de financiamento."""

    parcela_mensal: float = Field(
        description="Valor da parcela mensal (PRICE fixo, SAC primeira parcela)"
    )
    total_pago: float = Field(description="Valor total a ser pago ao final do financiamento")
    juros_totais: float = Field(description="Valor total de juros pagos")
    percentual_juros: float = Field(description="Percentual que os juros representam do total pago")
    primeira_parcela: DetalheParcela = Field(description="Detalhes da primeira parcela")
    ultima_parcela: DetalheParcela = Field(description="Detalhes da última parcela")


class Comparativo(BaseModel):
    """Comparativo com a média nacional."""

    taxa_media_nacional: float = Field(description="Taxa média nacional de financiamento (%)")
    diferenca_percentual: float = Field(
        description="Diferença percentual em relação à média nacional"
    )
    classificacao: Literal["ACIMA_DA_MEDIA", "NA_MEDIA", "ABAIXO_DA_MEDIA"] = Field(
        description="Classificação da taxa aplicada"
    )
    mensagem: str = Field(description="Mensagem explicativa sobre o comparativo")


class Analise(BaseModel):
    """Análise de viabilidade do financiamento."""

    comprometimento_renda_sugerido: int = Field(
        default=30, description="Percentual sugerido de comprometimento de renda (%)"
    )
    renda_minima_sugerida: float = Field(
        description="Renda mínima sugerida para esse financiamento"
    )
    viabilidade: Literal["ALTA", "MODERADA", "BAIXA"] = Field(
        description="Classificação da viabilidade do financiamento"
    )
    alertas: List[str] = Field(default_factory=list, description="Lista de alertas e recomendações")


class ParcelaAmortizacao(BaseModel):
    """Linha da tabela de amortização."""

    mes: int
    parcela: float
    juros: float
    amortizacao: float
    saldo_devedor: float


class SimulationResponse(BaseModel):
    """Resposta completa da simulação de financiamento."""

    request_id: str = Field(description="ID único da requisição")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Data e hora da simulação"
    )
    simulacao: DadosSimulacao
    taxas: TaxasAplicadas
    resultado: ResultadoFinanciamento
    comparativo: Comparativo
    analise: Analise
    tabela_amortizacao_resumida: List[ParcelaAmortizacao] = Field(
        description="Resumo da tabela de amortização (pontos chave)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "request_id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2026-01-06T15:30:00Z",
                "simulacao": {
                    "valor_imovel": 500000.00,
                    "entrada": 100000.00,
                    "valor_financiado": 400000.00,
                    "prazo_meses": 360,
                    "tipo_amortizacao": "PRICE",
                },
                "taxas": {
                    "indicador": {
                        "indicador_usado": "SELIC",
                        "valor_indicador": 11.75,
                        "fonte": "Banco Central do Brasil",
                        "data_referencia": "2026-01-06",
                    },
                    "taxa_juros_anual": 10.50,
                    "taxa_juros_mensal": 0.8368,
                    "formula_aplicada": "taxa_base + (selic * fator_ajuste)",
                },
                "resultado": {
                    "parcela_mensal": 3656.45,
                    "total_pago": 1316322.00,
                    "juros_totais": 916322.00,
                    "percentual_juros": 69.60,
                    "primeira_parcela": {
                        "valor": 3656.45,
                        "juros": 3347.20,
                        "amortizacao": 309.25,
                        "saldo_devedor": 399690.75,
                    },
                    "ultima_parcela": {
                        "valor": 3656.45,
                        "juros": 30.44,
                        "amortizacao": 3625.01,
                        "saldo_devedor": 0.00,
                    },
                },
                "comparativo": {
                    "taxa_media_nacional": 9.80,
                    "diferenca_percentual": 7.14,
                    "classificacao": "ACIMA_DA_MEDIA",
                    "mensagem": "A taxa aplicada está 7.14% acima da média nacional",
                },
                "analise": {
                    "comprometimento_renda_sugerido": 30,
                    "renda_minima_sugerida": 12188.17,
                    "viabilidade": "MODERADA",
                    "alertas": [
                        "Prazo longo: considere reduzir para diminuir juros totais",
                        "Taxa acima da média nacional: vale pesquisar outras instituições",
                    ],
                },
                "tabela_amortizacao_resumida": [
                    {
                        "mes": 1,
                        "parcela": 3656.45,
                        "juros": 3347.20,
                        "amortizacao": 309.25,
                        "saldo_devedor": 399690.75,
                    }
                ],
            }
        }
    )


class ErrorDetail(BaseModel):
    """Detalhes de um erro de validação."""

    field: str = Field(description="Campo que gerou o erro")
    message: str = Field(description="Mensagem de erro")


class ErrorResponse(BaseModel):
    """Resposta de erro padronizada."""

    error: dict = Field(description="Objeto contendo informações do erro")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Dados de entrada inválidos",
                    "details": [
                        {"field": "valor_imovel", "message": "Valor deve ser maior que zero"}
                    ],
                    "request_id": "550e8400-e29b-41d4-a716-446655440000",
                    "timestamp": "2026-01-06T15:30:00Z",
                }
            }
        }
    )
