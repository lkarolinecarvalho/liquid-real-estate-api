import json
from datetime import datetime
from typing import Dict, Any


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    response_body = {
        "status": "healthy",
        "service": "financing-simulator",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0"
    }
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response_body)
    }