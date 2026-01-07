import logging
import os
from typing import List, Literal

from src.models.responses import Analise, Comparativo

logger = logging.getLogger(__name__)


class ComparisonService:
    def __init__(self):
        """Inicializa o serviço de comparação."""
        self.taxa_media_nacional = float(os.getenv("TAXA_MEDIA_NACIONAL", "9.80"))
        self.comprometimento_ideal = 30

    def comparar_com_media_nacional(self, taxa_aplicada: float) -> Comparativo:
        diferenca = ((taxa_aplicada - self.taxa_media_nacional) / self.taxa_media_nacional) * 100

        if diferenca > 5:
            classificacao: Literal["ACIMA_DA_MEDIA", "NA_MEDIA", "ABAIXO_DA_MEDIA"] = "ACIMA_DA_MEDIA"
            mensagem = f"A taxa aplicada está {abs(diferenca):.2f}% acima da média nacional"
        elif diferenca < -5:
            classificacao = "ABAIXO_DA_MEDIA"
            mensagem = f"A taxa aplicada está {abs(diferenca):.2f}% abaixo da média nacional"
        else:
            classificacao = "NA_MEDIA"
            mensagem = "A taxa aplicada está dentro da média nacional"

        logger.info(
            "Comparativo com média nacional",
            extra={
                "taxa_aplicada": taxa_aplicada,
                "taxa_media": self.taxa_media_nacional,
                "diferenca_percentual": diferenca,
                "classificacao": classificacao
            }
        )

        return Comparativo(
            taxa_media_nacional=round(self.taxa_media_nacional, 2),
            diferenca_percentual=round(diferenca, 2),
            classificacao=classificacao,
            mensagem=mensagem
        )

    def analisar_viabilidade(
        self,
        parcela_mensal: float,
        taxa_aplicada: float,
        taxa_media: float,
        prazo_meses: int,
        percentual_juros: float
    ) -> Analise:
        renda_minima = parcela_mensal / (self.comprometimento_ideal / 100)

        alertas = self._gerar_alertas(
            taxa_aplicada=taxa_aplicada,
            taxa_media=taxa_media,
            prazo_meses=prazo_meses,
            percentual_juros=percentual_juros
        )

        viabilidade = self._classificar_viabilidade(
            taxa_aplicada=taxa_aplicada,
            taxa_media=taxa_media,
            prazo_meses=prazo_meses,
            percentual_juros=percentual_juros
        )

        logger.info(
            "Análise de viabilidade",
            extra={
                "viabilidade": viabilidade,
                "renda_minima_sugerida": renda_minima,
                "num_alertas": len(alertas)
            }
        )

        return Analise(
            comprometimento_renda_sugerido=self.comprometimento_ideal,
            renda_minima_sugerida=round(renda_minima, 2),
            viabilidade=viabilidade,
            alertas=alertas
        )

    def _gerar_alertas(
        self,
        taxa_aplicada: float,
        taxa_media: float,
        prazo_meses: int,
        percentual_juros: float
    ) -> List[str]:
        alertas = []

        diferenca_taxa = ((taxa_aplicada - taxa_media) / taxa_media) * 100
        if diferenca_taxa > 10:
            alertas.append(
                f"Taxa {diferenca_taxa:.1f}% acima da média nacional: "
                "considere pesquisar outras instituições financeiras"
            )
        elif diferenca_taxa > 5:
            alertas.append(
                "Taxa acima da média nacional: vale comparar com outras ofertas"
            )

        if prazo_meses > 300:
            alertas.append(
                "Prazo muito longo (>25 anos): considere reduzir para diminuir juros totais"
            )
        elif prazo_meses > 240:
            alertas.append(
                "Prazo longo: avalie se consegue pagar parcelas maiores para reduzir o prazo"
            )

        if percentual_juros > 80:
            alertas.append(
                f"Juros representam {percentual_juros:.1f}% do total pago: "
                "considere aumentar a entrada para reduzir o valor financiado"
            )
        elif percentual_juros > 70:
            alertas.append(
                "Juros representam mais de 70% do valor total: "
                "uma entrada maior reduziria significativamente os juros"
            )

        if not alertas:
            alertas.append(
                "Condições dentro dos padrões esperados para financiamento imobiliário"
            )

        return alertas

    def _classificar_viabilidade(
        self,
        taxa_aplicada: float,
        taxa_media: float,
        prazo_meses: int,
        percentual_juros: float
    ) -> Literal["ALTA", "MODERADA", "BAIXA"]:
        pontos_negativos = 0

        diferenca_taxa = ((taxa_aplicada - taxa_media) / taxa_media) * 100
        if diferenca_taxa > 15:
            pontos_negativos += 3
        elif diferenca_taxa > 10:
            pontos_negativos += 2
        elif diferenca_taxa > 5:
            pontos_negativos += 1

        if prazo_meses > 300:
            pontos_negativos += 2
        elif prazo_meses > 240:
            pontos_negativos += 1

        if percentual_juros > 80:
            pontos_negativos += 2
        elif percentual_juros > 70:
            pontos_negativos += 1

        if pontos_negativos >= 5:
            return "BAIXA"
        elif pontos_negativos >= 3:
            return "MODERADA"
        else:
            return "ALTA"
