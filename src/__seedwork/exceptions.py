from dataclasses import dataclass
from typing import TYPE_CHECKING


class NotImplementedException(Exception):
    pass


class SimpleValidationException(Exception):
    pass


if TYPE_CHECKING:
    from __seedwork.domain.validations import ValidationErrorFields


@dataclass()
class ValidationException(Exception):
    error: 'ValidationErrorFields'

    def __init__(self, error: 'ValidationErrorFields'):
        self.error = error
        super().__init__('Validation Error')
