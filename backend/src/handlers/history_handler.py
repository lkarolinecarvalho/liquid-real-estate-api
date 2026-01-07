import logging
from typing import Dict, Any

from src.services.dynamodb_service import get_dynamodb_service
from src.utils.response import create_response, create_error_response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler para buscar histórico de simulações
    
    Query Parameters:
        - user_identifier (opcional): Filtrar por usuário específico
        - limit (opcional): Número máximo de resultados (padrão: 10)
    """
    try:
        # Extrai query parameters
        query_params = event.get('queryStringParameters') or {}
        user_identifier = query_params.get('user_identifier')
        limit = int(query_params.get('limit', 10))
        
        # Valida limit
        if limit < 1 or limit > 100:
            return create_error_response(
                message="Limit deve estar entre 1 e 100",
                status_code=400
            )
        
        # Busca simulações
        db_service = get_dynamodb_service()
        
        if user_identifier:
            simulations = db_service.get_user_simulations(
                user_identifier=user_identifier,
                limit=limit
            )
        else:
            simulations = db_service.get_recent_simulations(limit=limit)
        
        return create_response(
            data={
                'total': len(simulations),
                'simulations': simulations,
                'filters': {
                    'user_identifier': user_identifier,
                    'limit': limit
                }
            }
        )
        
    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        return create_error_response(
            message=f"Parâmetros inválidos: {str(e)}",
            status_code=400
        )
        
    except Exception as e:
        logger.error(f"Erro ao buscar histórico: {str(e)}", exc_info=True)
        return create_error_response(
            message="Erro ao buscar histórico de simulações",
            status_code=500
        )


def get_by_id(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler para buscar simulação específica por ID
    
    Path Parameters:
        - id: ID da simulação
    
    Query Parameters:
        - created_at: Timestamp de criação (ISO format)
    """
    try:
        # Extrai path parameters
        path_params = event.get('pathParameters') or {}
        simulation_id = path_params.get('id')
        
        if not simulation_id:
            return create_error_response(
                message="ID da simulação é obrigatório",
                status_code=400
            )
        
        # Extrai query parameters
        query_params = event.get('queryStringParameters') or {}
        created_at = query_params.get('created_at')
        
        if not created_at:
            return create_error_response(
                message="created_at é obrigatório",
                status_code=400
            )
        
        # Busca simulação
        db_service = get_dynamodb_service()
        simulation = db_service.get_simulation(
            simulation_id=simulation_id,
            created_at=created_at
        )
        
        if not simulation:
            return create_error_response(
                message="Simulação não encontrada",
                status_code=404
            )
        
        return create_response(data=simulation)
        
    except Exception as e:
        logger.error(f"Erro ao buscar simulação: {str(e)}", exc_info=True)
        return create_error_response(
            message="Erro ao buscar simulação",
            status_code=500
        )