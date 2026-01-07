import json
from datetime import datetime, timezone
from typing import Any, Dict

from pydantic import ValidationError

from src.models.requests import SimulationRequest
from src.services import FinancingService
from src.services.dynamodb_service import get_dynamodb_service
from src.utils.exceptions import BusinessException, ExternalServiceException
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    request_id = context.request_id if hasattr(context, 'request_id') else 'local'

    logger.info(
        "Requisição recebida",
        extra={
            "request_id": request_id,
            "path": event.get("path"),
            "method": event.get("httpMethod")
        }
    )

    try:
        try:
            body = _parse_body(event)
        except ValueError as e:
            logger.warning(
                "Erro ao parsear JSON",
                extra={
                    "request_id": request_id,
                    "error": str(e)
                }
            )
            return _error_response(
                status_code=400,
                error_code="INVALID_JSON",
                message="Body JSON inválido",
                details=str(e),
                request_id=request_id
            )

        try:
            simulation_request = SimulationRequest(**body)
        except ValidationError as e:
            logger.warning(
                "Erro de validação",
                extra={
                    "request_id": request_id,
                    "errors": e.errors()
                }
            )
            return _error_response(
                status_code=400,
                error_code="VALIDATION_ERROR",
                message="Dados de entrada inválidos",
                details=[
                    {
                        "field": err["loc"][0] if err["loc"] else "unknown",
                        "message": err["msg"]
                    }
                    for err in e.errors()
                ],
                request_id=request_id
            )

        service = FinancingService()
        try:
            result = service.simular(simulation_request)
        finally:
            service.close()

        logger.info(
            "Simulação concluída com sucesso",
            extra={
                "request_id": request_id,
                "parcela_mensal": result.resultado.parcela_mensal
            }
        )

        # ✨ NOVO: Persistir no DynamoDB
        simulation_id = None
        try:
            headers = event.get('headers', {})
            user_identifier = headers.get('x-user-id') or \
                event.get('requestContext', {}).get('http', {}).get('sourceIp', 'unknown')

            # Converte resultado para dict
            result_dict = result.model_dump(mode='json')

            db_service = get_dynamodb_service()
            db_result = db_service.save_simulation(
                simulation_data=result_dict,
                user_identifier=user_identifier
            )

            simulation_id = db_result['simulation_id']
            logger.info("Simulação persistida", extra={'simulation_id': simulation_id})

        except Exception as db_error:
            logger.warning(f"Erro ao persistir no DynamoDB: {str(db_error)}", exc_info=True)
            # Continua sem quebrar - persistência é opcional

        return _success_response(result, request_id, simulation_id)

    except ExternalServiceException as e:
        logger.error(
            "Erro em serviço externo",
            extra={
                "request_id": request_id,
                "error": str(e)
            }
        )
        return _error_response(
            status_code=503,
            error_code="EXTERNAL_SERVICE_ERROR",
            message="Serviços externos temporariamente indisponíveis",
            details=str(e),
            request_id=request_id
        )

    except BusinessException as e:
        logger.error(
            "Erro de negócio",
            extra={
                "request_id": request_id,
                "error": str(e)
            }
        )
        return _error_response(
            status_code=400,
            error_code="BUSINESS_ERROR",
            message=str(e),
            request_id=request_id
        )

    except Exception as e:
        logger.exception(
            "Erro não tratado",
            extra={
                "request_id": request_id,
                "error_type": type(e).__name__
            }
        )
        return _error_response(
            status_code=500,
            error_code="INTERNAL_ERROR",
            message="Erro interno do servidor",
            details="Entre em contato com o suporte se o problema persistir",
            request_id=request_id
        )


def _parse_body(event: Dict[str, Any]) -> Dict[str, Any]:
    body = event.get("body", "{}")

    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError as err:
            raise ValueError("Body JSON inválido") from err

    return body


def _success_response(result: Any, request_id: str, simulation_id: str = None) -> Dict[str, Any]:
    response_dict = result.model_dump(mode='json')

    response_dict['request_id'] = request_id

    if simulation_id:
        response_dict['simulation_id'] = simulation_id

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "X-Request-Id": request_id
        },
        "body": json.dumps(response_dict, ensure_ascii=False, default=str)
    }


def _error_response(
    status_code: int,
    error_code: str,
    message: str,
    details: Any = None,
    request_id: str = None
) -> Dict[str, Any]:
    error_body = {
        "error": {
            "code": error_code,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    }

    if details:
        error_body["error"]["details"] = details

    if request_id:
        error_body["error"]["request_id"] = request_id

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "X-Request-Id": request_id or "unknown"
        },
        "body": json.dumps(error_body, ensure_ascii=False)
    }
