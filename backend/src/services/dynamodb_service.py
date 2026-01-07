import logging
import os
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table_name = os.getenv("DYNAMODB_TABLE", "financing-simulations-dev")
        self.table = self.dynamodb.Table(self.table_name)

    def _python_to_dynamo(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: self._python_to_dynamo(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._python_to_dynamo(item) for item in obj]
        elif isinstance(obj, float):
            return Decimal(str(obj))
        return obj

    def _dynamo_to_python(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: self._dynamo_to_python(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._dynamo_to_python(item) for item in obj]
        elif isinstance(obj, Decimal):
            return float(obj)
        return obj

    def save_simulation(
        self, simulation_data: Dict[str, Any], user_identifier: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            simulation_id = str(uuid.uuid4())
            created_at = datetime.utcnow().isoformat()
            ttl = int((datetime.utcnow() + timedelta(days=90)).timestamp())

            item = {
                "simulation_id": simulation_id,
                "created_at": created_at,
                "user_identifier": user_identifier or "anonymous",
                "ttl": ttl,
                **self._python_to_dynamo(simulation_data),
            }

            self.table.put_item(Item=item)
            logger.info(f"Simulação salva: {simulation_id}")

            return {
                "simulation_id": simulation_id,
                "created_at": created_at,
                "data": simulation_data,
            }

        except ClientError as e:
            logger.error(f"Erro ao salvar: {e.response['Error']['Message']}")
            raise

    def get_simulation(self, simulation_id: str, created_at: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.table.get_item(
                Key={"simulation_id": simulation_id, "created_at": created_at}
            )

            item = response.get("Item")
            if item:
                return self._dynamo_to_python(item)

            return None

        except ClientError as e:
            logger.error(f"Erro ao buscar: {e.response['Error']['Message']}")
            return None

    def get_user_simulations(self, user_identifier: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            response = self.table.query(
                IndexName="UserIndex",
                KeyConditionExpression=Key("user_identifier").eq(user_identifier),
                ScanIndexForward=False,
                Limit=limit,
            )

            items = response.get("Items", [])
            return [self._dynamo_to_python(item) for item in items]

        except ClientError as e:
            logger.error(f"Erro ao buscar usuário: {e.response['Error']['Message']}")
            return []

    def get_recent_simulations(self, limit: int = 20) -> List[Dict[str, Any]]:
        try:
            yesterday = (datetime.utcnow() - timedelta(days=1)).isoformat()

            response = self.table.scan(
                FilterExpression=Key("created_at").gt(yesterday), Limit=limit
            )

            items = response.get("Items", [])
            items_sorted = sorted(items, key=lambda x: x.get("created_at", ""), reverse=True)

            return [self._dynamo_to_python(item) for item in items_sorted]

        except ClientError as e:
            logger.error(f"Erro ao buscar recentes: {e.response['Error']['Message']}")
            return []


_service = None


def get_dynamodb_service() -> DynamoDBService:
    global _service
    if _service is None:
        _service = DynamoDBService()
    return _service
