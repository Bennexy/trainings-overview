import sys
sys.path.append(".")
from app.logger import get_logger

logger = get_logger("logger-exercise-error")


class ExerciseError(Exception):
    def __init__(self, message=None, error=Exception, previous_error=None) -> None:
        logger.error(f"{message} {error}")
        self.message = message
        self.error = error
        self. previous_error = previous_error

class InvalidFileFormat(ExerciseError):
    def __init__(self, message, previous_error: Exception = None) -> None:
        super().__init__(message=message, error=InvalidFileFormat, previous_error=previous_error)
        self.name = "InvalidFileFormat"

class InvalidDateFormat(ExerciseError):
    def __init__(self, message, previous_error: Exception = None) -> None:
        super().__init__(message=message, error=InvalidDateFormat, previous_error=previous_error)
        self.name = "InvalidDateFormat"

class ExerciseNameToLongError(ExerciseError):
    def __init__(self, message, previous_error: Exception = None) -> None:
        super().__init__(message=message, error=ExerciseNameToLongError, previous_error=previous_error)
        self.name = "ExerciseNameToLongError"

