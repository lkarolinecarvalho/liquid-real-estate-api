import pytest

from src.calculators import CalculatorFactory, PRICECalculator, SACCalculator


class TestPRICECalculator:
    def test_calcular_price_basico(self):
        calc = PRICECalculator()

        resultado = calc.calcular(
            valor_financiado=100000,
            taxa_juros_mensal=1.0,
            prazo_meses=12
        )

        # Verificar estrutura
        assert len(resultado.parcelas) == 12
        assert resultado.total_pago > 100000
        assert resultado.total_juros > 0

        # Verificar parcelas fixas (PRICE)
        primeira_parcela = resultado.parcelas[0].valor_parcela
        for parcela in resultado.parcelas:
            assert abs(parcela.valor_parcela - primeira_parcela) < 0.01

    def test_calcular_price_saldo_final_zero(self):
        """Testa se saldo final é zero."""
        calc = PRICECalculator()

        resultado = calc.calcular(
            valor_financiado=400000,
            taxa_juros_mensal=0.8368,
            prazo_meses=360
        )

        # Última parcela deve zerar saldo
        assert resultado.parcelas[-1].saldo_devedor == 0.0

    def test_calcular_price_juros_decrescentes(self):
        """Testa se juros são decrescentes no PRICE."""
        calc = PRICECalculator()

        resultado = calc.calcular(
            valor_financiado=200000,
            taxa_juros_mensal=1.0,
            prazo_meses=24
        )

        # Juros devem decrescer
        for i in range(len(resultado.parcelas) - 1):
            assert resultado.parcelas[i].valor_juros >= resultado.parcelas[i + 1].valor_juros

    def test_calcular_price_amortizacao_crescente(self):
        """Testa se amortização é crescente no PRICE."""
        calc = PRICECalculator()

        resultado = calc.calcular(
            valor_financiado=200000,
            taxa_juros_mensal=1.0,
            prazo_meses=24
        )

        # Amortização deve crescer
        for i in range(len(resultado.parcelas) - 1):
            assert resultado.parcelas[i].valor_amortizacao <= resultado.parcelas[i + 1].valor_amortizacao

    def test_calcular_price_taxa_zero(self):
        """Testa cálculo com taxa zero."""
        calc = PRICECalculator()

        resultado = calc.calcular(
            valor_financiado=120000,
            taxa_juros_mensal=0.0,
            prazo_meses=12
        )

        # Com taxa zero, parcela = valor / prazo
        parcela_esperada = 120000 / 12
        assert abs(resultado.parcelas[0].valor_parcela - parcela_esperada) < 0.01
        assert resultado.total_juros == 0.0

    def test_validacao_parametros_invalidos(self):
        """Testa validação de parâmetros."""
        calc = PRICECalculator()

        # Valor negativo
        with pytest.raises(ValueError):
            calc.calcular(-100000, 1.0, 12)

        # Taxa negativa
        with pytest.raises(ValueError):
            calc.calcular(100000, -1.0, 12)

        # Prazo zero
        with pytest.raises(ValueError):
            calc.calcular(100000, 1.0, 0)


class TestSACCalculator:
    """Testes para calculadora SAC."""

    def test_calcular_sac_basico(self):
        """Testa cálculo básico SAC."""
        calc = SACCalculator()

        resultado = calc.calcular(
            valor_financiado=100000,
            taxa_juros_mensal=1.0,
            prazo_meses=12
        )

        # Verificar estrutura
        assert len(resultado.parcelas) == 12
        assert resultado.total_pago > 100000
        assert resultado.total_juros > 0

    def test_calcular_sac_amortizacao_constante(self):
        """Testa se amortização é constante no SAC."""
        calc = SACCalculator()

        resultado = calc.calcular(
            valor_financiado=120000,
            taxa_juros_mensal=1.0,
            prazo_meses=12
        )

        amortizacao_esperada = 120000 / 12

        # Todas as amortizações devem ser iguais
        for parcela in resultado.parcelas:
            assert abs(parcela.valor_amortizacao - amortizacao_esperada) < 0.01

    def test_calcular_sac_parcelas_decrescentes(self):
        """Testa se parcelas são decrescentes no SAC."""
        calc = SACCalculator()

        resultado = calc.calcular(
            valor_financiado=200000,
            taxa_juros_mensal=1.0,
            prazo_meses=24
        )

        # Parcelas devem decrescer
        for i in range(len(resultado.parcelas) - 1):
            assert resultado.parcelas[i].valor_parcela >= resultado.parcelas[i + 1].valor_parcela

    def test_calcular_sac_saldo_final_zero(self):
        """Testa se saldo final é zero."""
        calc = SACCalculator()

        resultado = calc.calcular(
            valor_financiado=300000,
            taxa_juros_mensal=0.8,
            prazo_meses=240
        )

        assert resultado.parcelas[-1].saldo_devedor == 0.0

    def test_calcular_sac_primeira_parcela_maior(self):
        """Testa se primeira parcela é a maior."""
        calc = SACCalculator()

        resultado = calc.calcular(
            valor_financiado=150000,
            taxa_juros_mensal=1.2,
            prazo_meses=36
        )

        primeira = resultado.parcelas[0].valor_parcela

        for parcela in resultado.parcelas[1:]:
            assert primeira >= parcela.valor_parcela

    def test_metodos_auxiliares(self):
        """Testa métodos auxiliares do SAC."""
        calc = SACCalculator()

        primeira = calc.calcular_primeira_parcela(100000, 1.0, 12)
        ultima = calc.calcular_ultima_parcela(100000, 1.0, 12)

        assert primeira > ultima  # Primeira deve ser maior
        assert primeira > 0
        assert ultima > 0


class TestCalculatorFactory:
    """Testes para factory de calculadoras."""

    def test_criar_price(self):
        """Testa criação de calculadora PRICE."""
        calc = CalculatorFactory.create("PRICE")
        assert isinstance(calc, PRICECalculator)

    def test_criar_sac(self):
        """Testa criação de calculadora SAC."""
        calc = CalculatorFactory.create("SAC")
        assert isinstance(calc, SACCalculator)

    def test_tipo_invalido(self):
        """Testa tipo inválido."""
        with pytest.raises(ValueError, match="não suportado"):
            CalculatorFactory.create("INVALIDO")

    def test_tipos_disponiveis(self):
        """Testa listagem de tipos disponíveis."""
        tipos = CalculatorFactory.tipos_disponiveis()
        assert "PRICE" in tipos
        assert "SAC" in tipos


class TestComparacaoPRICEvsSAC:
    """Testes comparativos entre PRICE e SAC."""

    def test_sac_juros_menores_que_price(self):
        """Testa se SAC paga menos juros que PRICE."""
        price_calc = PRICECalculator()
        sac_calc = SACCalculator()

        # Mesmo financiamento
        params = {
            "valor_financiado": 200000,
            "taxa_juros_mensal": 1.0,
            "prazo_meses": 60
        }

        price_result = price_calc.calcular(**params)
        sac_result = sac_calc.calcular(**params)

        # SAC deve ter juros totais menores
        assert sac_result.total_juros < price_result.total_juros

    def test_price_parcela_fixa_sac_decrescente(self):
        """Testa características distintas de cada sistema."""
        price_calc = PRICECalculator()
        sac_calc = SACCalculator()

        params = {
            "valor_financiado": 150000,
            "taxa_juros_mensal": 0.9,
            "prazo_meses": 36
        }

        price_result = price_calc.calcular(**params)
        sac_result = sac_calc.calcular(**params)

        # PRICE: primeira = última parcela
        assert abs(
            price_result.parcelas[0].valor_parcela -
            price_result.parcelas[-1].valor_parcela
        ) < 0.01

        # SAC: primeira > última parcela
        assert (
            sac_result.parcelas[0].valor_parcela >
            sac_result.parcelas[-1].valor_parcela
        )
