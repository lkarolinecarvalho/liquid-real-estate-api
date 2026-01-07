import pytest
from pydantic import ValidationError

from src.models.requests import SimulationRequest


class TestSimulationRequest:
    def test_request_valido(self):
        request = SimulationRequest(
            valor_imovel=500000,
            entrada=100000,
            prazo_meses=360,
            tipo_amortizacao="PRICE",
            regiao="SP"
        )

        assert request.valor_imovel == 500000
        assert request.entrada == 100000
        assert request.prazo_meses == 360
        assert request.tipo_amortizacao == "PRICE"
        assert request.regiao == "SP"

    def test_valor_imovel_invalido(self):
        # Valor zero
        with pytest.raises(ValidationError):
            SimulationRequest(
                valor_imovel=0,
                entrada=10000,
                prazo_meses=360,
                tipo_amortizacao="PRICE",
                regiao="SP"
            )

        # Valor negativo
        with pytest.raises(ValidationError):
            SimulationRequest(
                valor_imovel=-100000,
                entrada=10000,
                prazo_meses=360,
                tipo_amortizacao="PRICE",
                regiao="SP"
            )

        # Valor muito alto
        with pytest.raises(ValidationError):
            SimulationRequest(
                valor_imovel=200_000_000,
                entrada=10000,
                prazo_meses=360,
                tipo_amortizacao="PRICE",
                regiao="SP"
            )

    def test_entrada_negativa(self):
        """Testa validação de entrada negativa."""
        with pytest.raises(ValidationError):
            SimulationRequest(
                valor_imovel=500000,
                entrada=-10000,
                prazo_meses=360,
                tipo_amortizacao="PRICE",
                regiao="SP"
            )

    def test_entrada_maior_que_imovel(self):
        """Testa entrada maior que valor do imóvel."""
        with pytest.raises(ValidationError, match="menor que o valor do imóvel"):
            SimulationRequest(
                valor_imovel=500000,
                entrada=600000,
                prazo_meses=360,
                tipo_amortizacao="PRICE",
                regiao="SP"
            )

    def test_prazo_invalido(self):
        """Testa validação de prazo."""
        # Prazo muito curto
        with pytest.raises(ValidationError):
            SimulationRequest(
                valor_imovel=500000,
                entrada=100000,
                prazo_meses=6,
                tipo_amortizacao="PRICE",
                regiao="SP"
            )

        # Prazo muito longo
        with pytest.raises(ValidationError):
            SimulationRequest(
                valor_imovel=500000,
                entrada=100000,
                prazo_meses=600,
                tipo_amortizacao="PRICE",
                regiao="SP"
            )

    def test_tipo_amortizacao_invalido(self):
        """Testa tipo de amortização inválido."""
        with pytest.raises(ValidationError):
            SimulationRequest(
                valor_imovel=500000,
                entrada=100000,
                prazo_meses=360,
                tipo_amortizacao="INVALIDO",
                regiao="SP"
            )

    def test_regiao_invalida(self):
        """Testa validação de região."""
        # Região com tamanho errado
        with pytest.raises(ValidationError):
            SimulationRequest(
                valor_imovel=500000,
                entrada=100000,
                prazo_meses=360,
                tipo_amortizacao="PRICE",
                regiao="SPP"
            )

        # UF inválida
        with pytest.raises(ValidationError, match="Região.*inválida"):
            SimulationRequest(
                valor_imovel=500000,
                entrada=100000,
                prazo_meses=360,
                tipo_amortizacao="PRICE",
                regiao="XX"
            )

    def test_regiao_lowercase_convertida(self):
        """Testa conversão de região para maiúsculas."""
        request = SimulationRequest(
            valor_imovel=500000,
            entrada=100000,
            prazo_meses=360,
            tipo_amortizacao="PRICE",
            regiao="sp"
        )

        assert request.regiao == "SP"

    def test_todas_ufs_validas(self):
        """Testa que todas as UFs brasileiras são aceitas."""
        ufs = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
            "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
            "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ]

        for uf in ufs:
            request = SimulationRequest(
                valor_imovel=500000,
                entrada=100000,
                prazo_meses=360,
                tipo_amortizacao="PRICE",
                regiao=uf
            )
            assert request.regiao == uf

    def test_valor_financiado(self):
        """Testa cálculo de valor financiado."""
        request = SimulationRequest(
            valor_imovel=500000,
            entrada=100000,
            prazo_meses=360,
            tipo_amortizacao="PRICE",
            regiao="SP"
        )

        assert request.valor_financiado() == 400000

    def test_percentual_entrada(self):
        """Testa cálculo de percentual de entrada."""
        request = SimulationRequest(
            valor_imovel=500000,
            entrada=100000,
            prazo_meses=360,
            tipo_amortizacao="PRICE",
            regiao="SP"
        )

        assert request.percentual_entrada() == 20.0

    def test_entrada_zero_valida(self):
        """Testa que entrada zero é válida."""
        request = SimulationRequest(
            valor_imovel=500000,
            entrada=0,
            prazo_meses=360,
            tipo_amortizacao="PRICE",
            regiao="SP"
        )

        assert request.entrada == 0
        assert request.valor_financiado() == 500000
        assert request.percentual_entrada() == 0.0

    def test_sac_tambem_valido(self):
        """Testa que SAC também é aceito."""
        request = SimulationRequest(
            valor_imovel=500000,
            entrada=100000,
            prazo_meses=360,
            tipo_amortizacao="SAC",
            regiao="RJ"
        )

        assert request.tipo_amortizacao == "SAC"
