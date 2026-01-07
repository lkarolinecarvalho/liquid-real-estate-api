from typing import Literal

from pydantic import BaseModel, Field, field_validator


class SimulationRequest(BaseModel):
    valor_imovel: float = Field(
        gt=0, le=100_000_000, description="Valor do imóvel em reais", examples=[500000.00]
    )

    entrada: float = Field(ge=0, description="Valor da entrada em reais", examples=[100000.00])

    prazo_meses: int = Field(
        ge=12, le=480, description="Prazo do financiamento em meses", examples=[360]
    )

    tipo_amortizacao: Literal["PRICE", "SAC"] = Field(
        description="Sistema de amortização: PRICE (parcelas fixas) ou SAC (parcelas decrescentes)",
        examples=["PRICE"],
    )

    regiao: str = Field(
        min_length=2, max_length=2, description="Sigla da UF (ex: SP, RJ, MG)", examples=["SP"]
    )

    @field_validator("regiao")
    @classmethod
    def regiao_maiuscula(cls, v: str) -> str:
        """Converte região para maiúsculas."""
        return v.upper()

    @field_validator("regiao")
    @classmethod
    def regiao_valida(cls, v: str) -> str:
        """Valida se a região é uma UF brasileira válida."""
        ufs_validas = {
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        }

        if v not in ufs_validas:
            raise ValueError(f"Região '{v}' inválida. Use uma UF brasileira válida.")

        return v

    @field_validator("entrada")
    @classmethod
    def entrada_menor_que_imovel(cls, v: float, info) -> float:
        if "valor_imovel" in info.data and v >= info.data["valor_imovel"]:
            raise ValueError("Entrada deve ser menor que o valor do imóvel")
        return v

    def valor_financiado(self) -> float:
        return self.valor_imovel - self.entrada

    def percentual_entrada(self) -> float:
        """Calcula o percentual da entrada sobre o valor do imóvel."""
        return (self.entrada / self.valor_imovel) * 100

    class Config:
        json_schema_extra = {
            "example": {
                "valor_imovel": 500000.00,
                "entrada": 100000.00,
                "prazo_meses": 360,
                "tipo_amortizacao": "PRICE",
                "regiao": "SP",
            }
        }
