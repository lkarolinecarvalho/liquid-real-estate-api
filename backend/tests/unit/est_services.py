from unittest.mock import patch

from src.models.domain import Indicador
from src.services import ComparisonService, IndicatorService


class TestComparisonService:
    """Testes para serviço de comparação."""

    def test_comparar_taxa_acima_media(self):
        """Testa comparação com taxa acima da média."""
        service = ComparisonService()

        comparativo = service.comparar_com_media_nacional(12.0)

        assert comparativo.taxa_media_nacional == 9.80
        assert comparativo.diferenca_percentual > 0
        assert comparativo.classificacao == "ACIMA_DA_MEDIA"
        assert "acima" in comparativo.mensagem.lower()

    def test_comparar_taxa_abaixo_media(self):
        """Testa comparação com taxa abaixo da média."""
        service = ComparisonService()

        comparativo = service.comparar_com_media_nacional(8.0)

        assert comparativo.diferenca_percentual < 0
        assert comparativo.classificacao == "ABAIXO_DA_MEDIA"
        assert "abaixo" in comparativo.mensagem.lower()

    def test_comparar_taxa_na_media(self):
        """Testa comparação com taxa na média."""
        service = ComparisonService()

        comparativo = service.comparar_com_media_nacional(9.9)

        assert comparativo.classificacao == "NA_MEDIA"
        assert "média nacional" in comparativo.mensagem.lower()

    def test_analisar_viabilidade_alta(self):
        """Testa análise com viabilidade alta."""
        service = ComparisonService()

        analise = service.analisar_viabilidade(
            parcela_mensal=3000,
            taxa_aplicada=9.5,
            taxa_media=9.8,
            prazo_meses=180,
            percentual_juros=60
        )

        assert analise.viabilidade == "ALTA"
        assert analise.renda_minima_sugerida == 10000.0
        assert analise.comprometimento_renda_sugerido == 30
        assert len(analise.alertas) > 0

    def test_analisar_viabilidade_moderada(self):
        """Testa análise com viabilidade moderada."""
        service = ComparisonService()

        analise = service.analisar_viabilidade(
            parcela_mensal=3500,
            taxa_aplicada=11.0,
            taxa_media=9.8,
            prazo_meses=300,
            percentual_juros=75
        )

        assert analise.viabilidade == "MODERADA"
        assert len(analise.alertas) > 1

    def test_analisar_viabilidade_baixa(self):
        """Testa análise com viabilidade baixa."""
        service = ComparisonService()

        analise = service.analisar_viabilidade(
            parcela_mensal=4000,
            taxa_aplicada=13.0,
            taxa_media=9.8,
            prazo_meses=360,
            percentual_juros=85
        )

        assert analise.viabilidade == "BAIXA"
        assert len(analise.alertas) >= 2

    def test_alertas_prazo_longo(self):
        """Testa geração de alerta para prazo longo."""
        service = ComparisonService()

        analise = service.analisar_viabilidade(
            parcela_mensal=3000,
            taxa_aplicada=9.5,
            taxa_media=9.8,
            prazo_meses=350,
            percentual_juros=65
        )

        # Deve ter alerta sobre prazo
        alertas_texto = " ".join(analise.alertas).lower()
        assert "prazo" in alertas_texto

    def test_alertas_juros_altos(self):
        """Testa geração de alerta para juros altos."""
        service = ComparisonService()

        analise = service.analisar_viabilidade(
            parcela_mensal=3000,
            taxa_aplicada=9.5,
            taxa_media=9.8,
            prazo_meses=180,
            percentual_juros=85
        )

        # Deve ter alerta sobre juros
        alertas_texto = " ".join(analise.alertas).lower()
        assert "juros" in alertas_texto


class TestIndicatorService:
    """Testes para serviço de indicadores."""

    def test_calcular_taxa_selic(self):
        """Testa cálculo de taxa baseado em SELIC."""
        service = IndicatorService()

        indicador = Indicador(
            tipo="SELIC",
            valor=11.75,
            fonte="Banco Central",
            data_referencia="2026-01-06"
        )

        taxa = service.calcular_taxa_juros(indicador)

        assert taxa.taxa_anual > 0
        assert taxa.taxa_mensal > 0
        assert taxa.indicador.tipo == "SELIC"
        assert "selic" in taxa.formula.lower()

    def test_calcular_taxa_ipca(self):
        """Testa cálculo de taxa baseado em IPCA."""
        service = IndicatorService()

        indicador = Indicador(
            tipo="IPCA",
            valor=4.62,
            fonte="IBGE",
            data_referencia="2026-01-06"
        )

        taxa = service.calcular_taxa_juros(indicador)

        assert taxa.taxa_anual > 0
        assert taxa.taxa_mensal > 0
        assert taxa.indicador.tipo == "IPCA"
        assert "ipca" in taxa.formula.lower()

    def test_calcular_taxa_base(self):
        """Testa cálculo com taxa base (fallback)."""
        service = IndicatorService()

        indicador = Indicador(
            tipo="TAXA_BASE",
            valor=10.0,
            fonte="Sistema",
            data_referencia="2026-01-06"
        )

        taxa = service.calcular_taxa_juros(indicador)

        assert taxa.taxa_anual == 10.0
        assert "fallback" in taxa.formula.lower()

    def test_limites_taxa(self):
        """Testa aplicação de limites na taxa."""
        service = IndicatorService()

        # Taxa muito baixa (deve ser limitada a 8%)
        assert service._aplicar_limites(5.0) == 8.0

        # Taxa muito alta (deve ser limitada a 15%)
        assert service._aplicar_limites(20.0) == 15.0

        # Taxa dentro dos limites
        assert service._aplicar_limites(10.0) == 10.0

    def test_converter_anual_para_mensal(self):
        """Testa conversão de taxa anual para mensal."""
        service = IndicatorService()

        # 12% ao ano
        taxa_mensal = service._converter_anual_para_mensal(12.0)

        # Taxa mensal composta deve ser menor que 1% (12/12)
        assert taxa_mensal < 1.0
        assert taxa_mensal > 0.9

        # Verificar que composição anual retorna ~12%
        taxa_anual_recalculada = ((1 + taxa_mensal/100) ** 12 - 1) * 100
        assert abs(taxa_anual_recalculada - 12.0) < 0.01

    @patch('src.clients.bacen_client.BacenClient.buscar_selic')
    @patch('src.clients.ibge_client.IBGEClient.buscar_ipca')
    def test_fallback_quando_apis_falham(self, mock_ipca, mock_selic):
        """Testa fallback quando APIs externas falham."""
        # Simular falha em ambas as APIs
        mock_selic.return_value = None
        mock_ipca.return_value = None

        service = IndicatorService()
        indicador = service.buscar_indicador_com_fallback()

        # Deve retornar taxa base
        assert indicador.tipo == "TAXA_BASE"
        assert indicador.valor == 10.0
        assert "fallback" in indicador.fonte.lower()

    @patch('src.clients.bacen_client.BacenClient.buscar_selic')
    def test_usa_selic_quando_disponivel(self, mock_selic):
        """Testa que SELIC é usada quando disponível."""
        mock_selic.return_value = Indicador(
            tipo="SELIC",
            valor=11.75,
            fonte="Banco Central",
            data_referencia="2026-01-06"
        )

        service = IndicatorService()
        indicador = service.buscar_indicador_com_fallback()

        assert indicador.tipo == "SELIC"
        assert indicador.valor == 11.75

    @patch('src.clients.bacen_client.BacenClient.buscar_selic')
    @patch('src.clients.ibge_client.IBGEClient.buscar_ipca')
    def test_usa_ipca_quando_selic_falha(self, mock_ipca, mock_selic):
        """Testa fallback para IPCA quando SELIC falha."""
        mock_selic.return_value = None
        mock_ipca.return_value = Indicador(
            tipo="IPCA",
            valor=4.62,
            fonte="IBGE",
            data_referencia="2025-12-01"
        )

        service = IndicatorService()
        indicador = service.buscar_indicador_com_fallback()

        assert indicador.tipo == "IPCA"
        assert indicador.valor == 4.62
