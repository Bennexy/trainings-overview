import sys
sys.path.append(".")
from app.logger import get_logger

logger = get_logger("logger-user-error")

class UserException(Exception):
    def __init__(self, message=None, error=Exception, previous_error=None) -> None:
        logger.error(f"{message} {error}")
        self.message=message
        self.error = error
        self.previous_error = previous_error

class NoArgsGivenError(UserException):
    def __init__(self, message, previous_error: Exception = None) -> None:
        super().__init__(message=message, error=NoArgsGivenError, previous_error=previous_error)
        self.name = "NoArgsGivenError"

class UserIdNotValidError(UserException):
    def __init__(self, message, previous_error: Exception = None) -> None:
        super().__init__(message=message, error=NoArgsGivenError, previous_error=previous_error)
        self.name = "NoArgsGivenError"

