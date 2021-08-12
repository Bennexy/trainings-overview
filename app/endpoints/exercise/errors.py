import sys
sys.path.append(".")
from app.logger import get_logger

logger = get_logger("logger-exercise-error")


class ExerciseError(Exception):
    def __init__(self, message=None, error=Exception) -> None:
        logger.error(f"{message} {error}")
        self.message = message
        self.error = error

class InvalidFileFormat(ExerciseError):
    def __init__(self, message) -> None:
        super().__init__(message=message, error=InvalidFileFormat)
        self.name = "InvalidFileFormat"

class InvalidDateFormat(ExerciseError):
    def __init__(self, message) -> None:
        super().__init__(message=message, error=InvalidDateFormat)
        self.name = "InvalidDateFormat"


