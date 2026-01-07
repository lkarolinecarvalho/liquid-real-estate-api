from typing import Literal

from src.calculators.base_calculator import BaseCalculator
from src.calculators.price_calculator import PRICECalculator
from src.calculators.sac_calculator import SACCalculator


class CalculatorFactory:
    _calculators = {
        "PRICE": PRICECalculator,
        "SAC": SACCalculator
    }

    @classmethod
    def create(cls, tipo_amortizacao: Literal["PRICE", "SAC"]) -> BaseCalculator:
        calculator_class = cls._calculators.get(tipo_amortizacao)

        if calculator_class is None:
            tipos_validos = ", ".join(cls._calculators.keys())
            raise ValueError(
                f"Tipo de amortização '{tipo_amortizacao}' não suportado. "
                f"Tipos válidos: {tipos_validos}"
            )

        return calculator_class()

    @classmethod
    def tipos_disponiveis(cls) -> list[str]:
        return list(cls._calculators.keys())


__all__ = [
    "BaseCalculator",
    "PRICECalculator",
    "SACCalculator",
    "CalculatorFactory"
]
