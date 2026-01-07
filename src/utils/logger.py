import os
import logging
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:

        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        if hasattr(record, "__dict__"):
            for key, value in record.__dict__.items():
                if key not in ["name", "msg", "args", "created", "filename", 
                              "funcName", "levelname", "levelno", "lineno", 
                              "module", "msecs", "message", "pathname", "process",
                              "processName", "relativeCreated", "thread", "threadName",
                              "exc_info", "exc_text", "stack_info"]:
                    log_data[key] = value
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level))
    
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    logger.addHandler(handler)
    
    return logger