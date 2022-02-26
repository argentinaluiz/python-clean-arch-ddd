import unittest
from pydantic.dataclasses import dataclass
# pylint: disable=no-name-in-module
from pydantic.fields import Field
from __seedwork.exceptions import ValidationException
from __seedwork.domain.validations import PydanticValidator


@dataclass
class StubPydantic:
    prop1: str = Field(...)
    prop2: int = Field(...)


class StubPydanticValidation(PydanticValidator):

    def validate(self, data):
        self._validate(data, StubPydantic)


class TestDRFValidatorInt(unittest.TestCase):

    def test_validation_error(self):
        with self.assertRaises(ValidationException) as assert_error:
            StubPydanticValidation().validate({})
        self.assertDictEqual(
            {'prop1': 'field required', 'prop2': 'field required'}, assert_error.exception.error)
