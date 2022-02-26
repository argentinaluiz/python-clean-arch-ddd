
from abc import ABC
import abc
from dataclasses import dataclass
from typing import Any, Dict, List  # terá uma Self na versão 3.11
from pydantic import ValidationError as PydanticValidationError
from __seedwork.exceptions import SimpleValidationException, NotImplementedException, ValidationException

@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str

    @staticmethod
    def values(value, prop):
        return ValidatorRules(value, prop)

    def required(self) -> 'ValidatorRules':
        if self.value is None or self.value == '':
            raise SimpleValidationException(f'The {self.prop} is required')
        return self

    def string(self) -> 'ValidatorRules':
        if self.value is not None and not isinstance(self.value, str):
            raise SimpleValidationException(
                f'The {self.prop} must be a string')
        return self

    def max_length(self, max_length: int) -> 'ValidatorRules':
        if self.value is not None and len(self.value) > max_length:
            raise SimpleValidationException(
                f'The {self.prop} must be less than {max_length} characters'
            )
        return self

    def boolean(self) -> 'ValidatorRules':
        if self.value is not None and self.value is not True and self.value is not False:
            raise SimpleValidationException(
                f'The {self.prop} must be a boolean'
            )
        return self


ValidationErrorFields = Dict[str, List[str]]


class ValidatorInterface(ABC):

    @abc.abstractmethod
    def validate(self, data: Any) -> None:
        raise NotImplementedException

    @property
    @abc.abstractmethod
    def errors(self) -> ValidationErrorFields:
        raise NotImplementedException


class PydanticValidator(ValidatorInterface, ABC):
    _errors: ValidationErrorFields = None

    def _validate(self, data: dict | None, pydantic_class) -> None:
        try:
            data = data if isinstance(data, dict) else {}
            pydantic_class(**data)
        except PydanticValidationError as error:
            self._errors = {e['loc'][0]: e['msg'] for e in error.errors()}
            raise ValidationException(self._errors) from error

    @abc.abstractmethod
    def validate(self, data: Any):
        raise NotImplementedException

    @property
    def errors(self) -> ValidationErrorFields:
        return self._errors

# class DRFValidator(ValidatorInterface, ABC):

#     _errors: ValidationErrorFields = None

#     def _validate(self, serializer: Serializer) -> None:
#         # pylint: disable=import-outside-toplevel
#         from __seedwork.exceptions import ValidationError
#         is_valid = serializer.is_valid()
#         if not is_valid:
#             raise ValidationError(serializer.error_messages)

#     @abc.abstractmethod
#     def validate(self, data: Any):
#         # pylint: disable=import-outside-toplevel
#         from __seedwork.exceptions import NotImplementedException
#         raise NotImplementedException

#     @property
#     def errors(self) -> ValidationErrorFields:
#         return self._errors
