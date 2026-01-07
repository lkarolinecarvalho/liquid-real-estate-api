class BusinessException(Exception):
    pass


class ExternalServiceException(Exception):
    pass


class CalculationException(Exception):
    pass


def handle_exception(exception: Exception, context: str = "") -> None:
    import logging

    logger = logging.getLogger(__name__)

    logger.error(
        f"Erro capturado: {context}",
        extra={
            "exception_type": type(exception).__name__,
            "exception_message": str(exception),
            "context": context,
        },
        exc_info=True,
    )
