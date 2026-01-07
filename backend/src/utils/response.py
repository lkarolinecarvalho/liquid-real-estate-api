import json
from typing import Dict, Any, Optional


def create_response(
    data: Any,
    status_code: int = 200,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    default_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': '*'
    }
    
    if headers:
        default_headers.update(headers)
    
    return {
        'statusCode': status_code,
        'headers': default_headers,
        'body': json.dumps(data, ensure_ascii=False)
    }


def create_error_response(
    message: str,
    status_code: int = 500,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    error_body = {
        'error': True,
        'message': message
    }
    
    if error_code:
        error_body['error_code'] = error_code
    
    if details:
        error_body['details'] = details
    
    return create_response(
        data=error_body,
        status_code=status_code
    )