import sys
sys.path.append(".")
from app.logger import get_logger

logger = get_logger("logger-user-error")

class UserException(Exception):
    def __init__(self, message=None, error=Exception) -> None:
        logger.error(f"{message} {error}")

class NoArgsGivenError(UserException):
    def __init__(self, message) -> None:
        super().__init__(message=message, error=NoArgsGivenError)
