from datetime import datetime
import unittest
from unittest import mock
from unittest.mock import MagicMock, PropertyMock
from dataclasses import fields
from rest_framework import serializers
from django.conf import settings
from __seedwork.domain.entities import UniqueEntityId
from __seedwork.domain.validators import (
    DRFValidator,
    StrictBooleanField,
    StrictCharField,
    UniqueEntityIdField,
    ValidatorFieldsInterface,
    ValidatorRules
)
from __seedwork.domain.exceptions import SimpleValidationException, ValidationException


class TestValidationRulesUnit(unittest.TestCase):

    def test_algumacoisa(self):
        validator = ValidatorRules.values('test', 'field')
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual('test', validator.value)
        self.assertEqual('field', validator.prop)

    def test_required_rule(self):
        data = [
            {'value': "test", 'prop': "field"},
            {'value': 5, 'prop': "field"},
            {'value': 0, 'prop': "field"},
            {'value': False, 'prop': "field"},
        ]

        for i in data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).required(),
                ValidatorRules
            )

        data = [
            {'value': None, 'prop': "field"},
            {'value': "", 'prop': "field"},
        ]

        message_error = 'The field is required'

        for i in data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).required()
            self.assertEqual(message_error, assert_error.exception.args[0])

    def test_string_rule(self):
        data = [
            {'value': None, 'prop': "field"},
            {'value': "", 'prop': "field"},
            {'value': "test", 'prop': "field"},
        ]

        for i in data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).string(),
                ValidatorRules
            )

        data = [
            {'value': 5, 'prop': "field"},
            {'value': datetime, 'prop': "field"},
        ]

        message_error = 'The field must be a string'

        for i in data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).string()
            self.assertEqual(message_error, assert_error.exception.args[0])

    def test_max_length_rule(self):
        data = [
            {'value': None, 'prop': "field"},
            {'value': "t" * 5, 'prop': "field"},
        ]

        for i in data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).max_length(5),
                ValidatorRules
            )

        data = [
            {'value': "t" * 11, 'prop': "field"},
        ]

        message_error = 'The field must be less than 10 characters'

        for i in data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).max_length(10)
            self.assertEqual(message_error, assert_error.exception.args[0])

    def test_boolean_rule(self):
        data = [
            {'value': None, 'prop': "field"},
            {'value': True, 'prop': "field"},
            {'value': False, 'prop': "field"},
        ]

        for i in data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).boolean(),
                ValidatorRules
            )

        data = [
            {'value': "", 'prop': "field"},
            {'value': 5, 'prop': "field"},
        ]

        message_error = 'The field must be a boolean'

        for i in data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).boolean()
            self.assertEqual(message_error, assert_error.exception.args[0])


class TestValidatorFieldsInterfaceUnit(unittest.TestCase):

    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            ValidatorFieldsInterface()
        self.assertEqual(
            "Can't instantiate abstract class ValidatorFieldsInterface " +
            "with abstract method validate",
            assert_error.exception.args[0]
        )

    def test_errors_attribute_is_none(self):
        fields_class = fields(ValidatorFieldsInterface)
        self.assertEqual(fields_class[0].name, 'errors')
        self.assertIsNone(fields_class[0].default)


class StubDRFValidation(DRFValidator):
    mock_serializer: serializers.Serializer

    def __init__(self, serializer=None) -> None:
        self.mock_serializer = serializer
        super().__init__()

    def validate(self, data):
        self._validate(self.mock_serializer)


class TestDRFValidatorUnit(unittest.TestCase):

    def test_django_settings(self):
        self.assertTrue(settings.configure)
        self.assertFalse(settings.USE_I18N)

    def test_throw_error_when_validate_method_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            DRFValidator()
        self.assertEqual(
            "Can't instantiate abstract class DRFValidator with abstract method validate",
            assert_error.exception.args[0]
        )

    def test_errors_attribute_is_none(self):
        self.assertIsNone(StubDRFValidation().errors)

    def test_error_field(self):
        validator = StubDRFValidation()
        self.assertIsNone(validator.errors)
        validator.errors = {'field': ['some error']}
        self.assertDictEqual({'field': ['some error']}, validator.errors)

    @mock.patch.object(serializers.Serializer, 'is_valid', return_value=False)
    @mock.patch.object(serializers.Serializer, 'errors', return_value={'field': ['some error']}, new_callable=PropertyMock)
    def test_validate_with_validate_error(self, mock_is_valid: MagicMock, mock_errors: PropertyMock):
        # mock_serializer = serializers.Serializer()
        # mock_serializer.is_valid = MagicMock(return_value=False,)
        # mock_serializer.errors = {'field': ['some error']}
        validator = StubDRFValidation(serializers.Serializer())
        with self.assertRaises(ValidationException) as assert_error:
            validator.validate({'field': None})
        self.assertDictEqual(
            assert_error.exception.error,
            {'field': ['some error']}
        )
        self.assertEqual(
            validator.errors,
            {'field': ['some error']}
        )

        mock_is_valid.assert_called()
        mock_errors.assert_called()

    def test_validate_with_success(self):
        mock_serializer = serializers.Serializer()
        mock_serializer.is_valid = MagicMock(return_value=True)

        validator = StubDRFValidation(mock_serializer)
        validator.validate({'field': 'test'})
        mock_serializer.is_valid.assert_called_once()


class TestStrictCharField(unittest.TestCase):

    def test_if_not_str_values_is_invalid(self):
        # pylint: disable=abstract-method
        class StubStrictCharFieldSerializer(serializers.Serializer):
            name = StrictCharField()

        serializer = StubStrictCharFieldSerializer(data={'name': 5})
        serializer.is_valid()
        self.assertDictEqual(
            {'name': [serializers.ErrorDetail(
                string='Not a valid string.', code='invalid')]},
            serializer.errors
        )

        serializer = StubStrictCharFieldSerializer(data={'name': True})
        serializer.is_valid()
        self.assertDictEqual(
            {'name': [serializers.ErrorDetail(
                string='Not a valid string.', code='invalid')]},
            serializer.errors
        )

    def test_if_none_values_is_valid(self):
        # pylint: disable=abstract-method
        class StubStrictCharFieldSerializer(serializers.Serializer):
            name = StrictCharField(allow_null=True, required=False)

        serializer = StubStrictCharFieldSerializer(data={'name': None})
        self.assertTrue(serializer.is_valid())


class TestStrictBooleanField(unittest.TestCase):

    def test_if_not_bool_values_is_invalid(self):
        # pylint: disable=abstract-method
        class StubStrictBooleanFieldSerializer(serializers.Serializer):
            active = StrictBooleanField()

        message_boolean_invalid = 'Must be a valid boolean.'
        
        serializer = StubStrictBooleanFieldSerializer(data={'active': 0})
        serializer.is_valid()
        self.assertDictEqual(
            {'active': [serializers.ErrorDetail(
                string=message_boolean_invalid, code='invalid')]},
            serializer.errors
        )

        serializer = StubStrictBooleanFieldSerializer(data={'active': 1})
        serializer.is_valid()
        self.assertDictEqual(
            {'active': [serializers.ErrorDetail(
                string=message_boolean_invalid, code='invalid')]},
            serializer.errors
        )

        serializer = StubStrictBooleanFieldSerializer(data={'active': 'True'})
        serializer.is_valid()
        self.assertDictEqual(
            {'active': [serializers.ErrorDetail(
                string=message_boolean_invalid, code='invalid')]},
            serializer.errors
        )

        serializer = StubStrictBooleanFieldSerializer(data={'active': 'False'})
        serializer.is_valid()
        self.assertDictEqual(
            {'active': [serializers.ErrorDetail(
                string=message_boolean_invalid, code='invalid')]},
            serializer.errors
        )

    def test_valid_values(self):
        # pylint: disable=abstract-method
        class StubStrictBooleanFieldSerializer(serializers.Serializer):
            active = StrictBooleanField(allow_null=True)

        serializer = StubStrictBooleanFieldSerializer(data={'active': True})
        self.assertTrue(serializer.is_valid())

        serializer = StubStrictBooleanFieldSerializer(data={'active': False})
        self.assertTrue(serializer.is_valid())

        serializer = StubStrictBooleanFieldSerializer(data={'active': None})
        self.assertTrue(serializer.is_valid())


class TestUniqueEntityIdField(unittest.TestCase):

    def test_invalid_cases(self):
        # pylint: disable=abstract-method
        class StubUniqueEntityIdSerializer(serializers.Serializer):
            id = UniqueEntityIdField()

        serializer = StubUniqueEntityIdSerializer(data={'id': 0})
        serializer.is_valid()
        self.assertDictEqual(
            {'id': [serializers.ErrorDetail(
                string='Must be a instance of UniqueEntityId.', code='invalid')]},
            serializer.errors
        )

        serializer = StubUniqueEntityIdSerializer(data={'id': ''})
        serializer.is_valid()
        self.assertDictEqual(
            {'id': [serializers.ErrorDetail(
                string='Must be a instance of UniqueEntityId.', code='invalid')]},
            serializer.errors
        )

    def test_valid_values(self):
        # pylint: disable=abstract-method
        class StubUniqueEntityIdSerializer(serializers.Serializer):
            id = UniqueEntityIdField()

        serializer = StubUniqueEntityIdSerializer(
            data={'id': UniqueEntityId()})
        self.assertTrue(serializer.is_valid())


# class StubPydanticValidation(PydanticValidator):
#     mock_pydantic_class: Any

#     def __init__(self, mock_pydantic_class=None) -> None:
#         self.mock_pydantic_class = mock_pydantic_class
#         super().__init__()

#     def validate(self, data):
#         self._validate(data, self.mock_pydantic_class)


# class TestPydanticValidatorUnit(unittest.TestCase):

#     def test_throw_error_when_validate_method_not_implemented(self):
#         with self.assertRaises(TypeError) as assert_error:
#             # pylint: disable=abstract-class-instantiated
#             PydanticValidator()
#         self.assertEqual(
#             "Can't instantiate abstract class PydanticValidator with abstract method validate",
#             assert_error.exception.args[0]
#         )

#     def test_error_field(self):
#         validator = StubPydanticValidation()
#         self.assertIsNone(validator.errors)
#         setattr(validator, '_errors', {'field': ['som error']})
#         self.assertDictEqual({'field': ['som error']}, validator.errors)

#     def test_validate_with_validate_error(self):
#         mock_pydantic_class = MagicMock(
#             side_effect=ValidationException({'field': ['some error']}))

#         validator = StubPydanticValidation(mock_pydantic_class)
#         with self.assertRaises(ValidationException) as assert_error:
#             validator.validate({'field': None})
#         self.assertDictEqual(
#             {'field': ['some error']}, assert_error.exception.error)
#         mock_pydantic_class.assert_called_once()

#     def test_validate_with_success(self):
#         mock_pydantic_class = MagicMock()

#         validator = StubPydanticValidation(mock_pydantic_class)
#         validator.validate({'field': 'test'})
#         mock_pydantic_class.assert_called_once()
