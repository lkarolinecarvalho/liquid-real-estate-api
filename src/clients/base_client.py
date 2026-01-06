import httpx
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseHTTPClient:
    def __init__(
        self,
        timeout: int = 3,
        max_retries: int = 2
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.client = httpx.Client(
            timeout=httpx.Timeout(timeout),
            follow_redirects=True
        )
    
    def get(
        self,
        url: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Optional[dict]:
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(
                    f"Requisição HTTP GET",
                    extra={
                        "url": url,
                        "attempt": attempt,
                        "max_retries": self.max_retries
                    }
                )
                
                response = self.client.get(
                    url,
                    params=params,
                    headers=headers
                )
                
                response.raise_for_status()
                
                logger.info(
                    f"Requisição bem-sucedida",
                    extra={
                        "url": url,
                        "status_code": response.status_code,
                        "attempt": attempt
                    }
                )
                
                return response.json()
                
            except httpx.TimeoutException as e:
                logger.warning(
                    f"Timeout na requisição (tentativa {attempt}/{self.max_retries})",
                    extra={
                        "url": url,
                        "error": str(e),
                        "attempt": attempt
                    }
                )
                
                if attempt == self.max_retries:
                    logger.error(
                        f"Falha após {self.max_retries} tentativas - Timeout",
                        extra={"url": url}
                    )
                    return None
                    
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"Erro HTTP {e.response.status_code}",
                    extra={
                        "url": url,
                        "status_code": e.response.status_code,
                        "attempt": attempt
                    }
                )
                
                if 400 <= e.response.status_code < 500:
                    return None
                
                if attempt == self.max_retries:
                    return None
                    
            except Exception as e:
                logger.error(
                    f"Erro inesperado na requisição",
                    extra={
                        "url": url,
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "attempt": attempt
                    }
                )
                
                if attempt == self.max_retries:
                    return None
        
        return None
    
    def close(self):
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()