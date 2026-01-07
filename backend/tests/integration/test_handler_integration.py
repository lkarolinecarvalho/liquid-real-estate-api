import json
from unittest.mock import Mock

from src.handlers.financing_handler import handler


class TestFinancingHandlerIntegration:
    """Testes de integração do handler principal."""

    def test_handler_request_valido_completo(self):
        """Testa handler com request válido completo."""
        event = {
            "body": json.dumps({
                "valor_imovel": 500000,
                "entrada": 100000,
                "prazo_meses": 360,
                "tipo_amortizacao": "PRICE",
                "regiao": "SP"
            })
        }

        context = Mock()
        context.request_id = "test-123"

        response = handler(event, context)

        # Verificar resposta
        assert response["statusCode"] == 200
        assert "application/json" in response["headers"]["Content-Type"]

        # Parse body
        body = json.loads(response["body"])

        # Verificar estrutura da resposta
        assert "request_id" in body
        assert "simulacao" in body
        assert "taxas" in body
        assert "resultado" in body
        assert "comparativo" in body
        assert "analise" in body
        assert "tabela_amortizacao_resumida" in body

        # Verificar dados da simulação
        assert body["simulacao"]["valor_imovel"] == 500000
        assert body["simulacao"]["entrada"] == 100000
        assert body["simulacao"]["valor_financiado"] == 400000

        # Verificar resultado
        assert body["resultado"]["parcela_mensal"] > 0
        assert body["resultado"]["total_pago"] > 400000
        assert body["resultado"]["juros_totais"] > 0

    def test_handler_request_sac(self):
        """Testa handler com sistema SAC."""
        event = {
            "body": json.dumps({
                "valor_imovel": 300000,
                "entrada": 50000,
                "prazo_meses": 240,
                "tipo_amortizacao": "SAC",
                "regiao": "RJ"
            })
        }

        context = Mock()
        context.request_id = "test-sac"

        response = handler(event, context)

        assert response["statusCode"] == 200

        body = json.loads(response["body"])
        assert body["simulacao"]["tipo_amortizacao"] == "SAC"
        assert body["resultado"]["parcela_mensal"] > 0

    def test_handler_erro_validacao(self):
        """Testa handler com dados inválidos."""
        event = {
            "body": json.dumps({
                "valor_imovel": -100000,  # Inválido
                "entrada": 10000,
                "prazo_meses": 360,
                "tipo_amortizacao": "PRICE",
                "regiao": "SP"
            })
        }

        context = Mock()
        context.request_id = "test-error"

        response = handler(event, context)

        # Deve retornar erro 400
        assert response["statusCode"] == 400

        body = json.loads(response["body"])
        assert "error" in body
        assert body["error"]["code"] == "VALIDATION_ERROR"
        assert "details" in body["error"]

    def test_handler_body_json_invalido(self):
        """Testa handler com JSON inválido."""
        event = {
            "body": "{ invalid json"
        }

        context = Mock()
        context.request_id = "test-invalid-json"

        response = handler(event, context)

        assert response["statusCode"] == 400

    def test_handler_entrada_maior_que_imovel(self):
        """Testa erro quando entrada é maior que valor do imóvel."""
        event = {
            "body": json.dumps({
                "valor_imovel": 200000,
                "entrada": 300000,  # Maior que o imóvel
                "prazo_meses": 360,
                "tipo_amortizacao": "PRICE",
                "regiao": "MG"
            })
        }

        context = Mock()
        context.request_id = "test-entrada-invalida"

        response = handler(event, context)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "error" in body

    def test_handler_regiao_invalida(self):
        """Testa erro com região inválida."""
        event = {
            "body": json.dumps({
                "valor_imovel": 500000,
                "entrada": 100000,
                "prazo_meses": 360,
                "tipo_amortizacao": "PRICE",
                "regiao": "XX"  # Inválida
            })
        }

        context = Mock()
        context.request_id = "test-regiao-invalida"

        response = handler(event, context)

        assert response["statusCode"] == 400

    def test_handler_tipo_amortizacao_invalido(self):
        """Testa erro com tipo de amortização inválido."""
        event = {
            "body": json.dumps({
                "valor_imovel": 500000,
                "entrada": 100000,
                "prazo_meses": 360,
                "tipo_amortizacao": "INVALIDO",
                "regiao": "SP"
            })
        }

        context = Mock()
        context.request_id = "test-tipo-invalido"

        response = handler(event, context)

        assert response["statusCode"] == 400

    def test_handler_headers_cors(self):
        """Testa se headers CORS estão presentes."""
        event = {
            "body": json.dumps({
                "valor_imovel": 500000,
                "entrada": 100000,
                "prazo_meses": 360,
                "tipo_amortizacao": "PRICE",
                "regiao": "SP"
            })
        }

        context = Mock()
        context.request_id = "test-cors"

        response = handler(event, context)

        # Verificar CORS headers
        assert "Access-Control-Allow-Origin" in response["headers"]
        assert response["headers"]["Access-Control-Allow-Origin"] == "*"
        assert "Access-Control-Allow-Methods" in response["headers"]

    def test_handler_todas_regioes_validas(self):
        """Testa que todas as UFs são processadas corretamente."""
        ufs = ["SP", "RJ", "MG", "BA", "RS", "PR", "SC"]

        for uf in ufs:
            event = {
                "body": json.dumps({
                    "valor_imovel": 400000,
                    "entrada": 80000,
                    "prazo_meses": 300,
                    "tipo_amortizacao": "PRICE",
                    "regiao": uf
                })
            }

            context = Mock()
            context.request_id = f"test-{uf}"

            response = handler(event, context)

            assert response["statusCode"] == 200, f"Falhou para UF {uf}"

    def test_handler_entrada_zero(self):
        """Testa financiamento com entrada zero."""
        event = {
            "body": json.dumps({
                "valor_imovel": 300000,
                "entrada": 0,  # Sem entrada
                "prazo_meses": 360,
                "tipo_amortizacao": "PRICE",
                "regiao": "SP"
            })
        }

        context = Mock()
        context.request_id = "test-sem-entrada"

        response = handler(event, context)

        assert response["statusCode"] == 200

        body = json.loads(response["body"])
        assert body["simulacao"]["valor_financiado"] == 300000
        assert body["simulacao"]["entrada"] == 0

    def test_handler_prazo_minimo(self):
        """Testa com prazo mínimo (12 meses)."""
        event = {
            "body": json.dumps({
                "valor_imovel": 150000,
                "entrada": 50000,
                "prazo_meses": 12,
                "tipo_amortizacao": "PRICE",
                "regiao": "SP"
            })
        }

        context = Mock()
        context.request_id = "test-prazo-minimo"

        response = handler(event, context)

        assert response["statusCode"] == 200

        body = json.loads(response["body"])
        assert len(body["tabela_amortizacao_resumida"]) <= 12

    def test_handler_prazo_maximo(self):
        """Testa com prazo máximo (480 meses)."""
        event = {
            "body": json.dumps({
                "valor_imovel": 800000,
                "entrada": 200000,
                "prazo_meses": 480,
                "tipo_amortizacao": "SAC",
                "regiao": "DF"
            })
        }

        context = Mock()
        context.request_id = "test-prazo-maximo"

        response = handler(event, context)

        assert response["statusCode"] == 200

        body = json.loads(response["body"])
        assert body["simulacao"]["prazo_meses"] == 480


class TestHealthHandler:
    """Testes para health check handler."""

    def test_health_check_sucesso(self):
        """Testa health check."""
        from src.handlers.health_handler import handler

        event = {}
        context = Mock()

        response = handler(event, context)

        assert response["statusCode"] == 200

        body = json.loads(response["body"])
        assert body["status"] == "healthy"
        assert body["service"] == "financing-simulator"
        assert "timestamp" in body
        assert "version" in body
