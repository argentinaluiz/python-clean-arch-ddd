import unittest

from datetime import datetime
from __seedwork.domain.exceptions import SimpleValidationException, ValidationException
from __seedwork.domain.value_objects import UniqueEntityId
from category.domain.validations import CategoryRules, CategoryValidator, CategoryValidatorFactory
from category.domain.entities import Category


class TestCategoryValidatorUnit(unittest.TestCase):

    validator: CategoryValidator

    def setUp(self) -> None:
        self.validator = CategoryValidatorFactory.create()
        return super().setUp()

    def test_invalidation_cases_for_id_field(self):
        with self.assertRaises(ValidationException) as assert_error:
            self.validator.validate({'unique_entity_id': None})
        self.assertListEqual(
            ['This field may not be null.'],
            assert_error.exception.error['unique_entity_id']
        )

        with self.assertRaises(ValidationException) as assert_error:
            self.validator.validate({'unique_entity_id': ''})
        self.assertListEqual(
            ['Must be a instance of UniqueEntityId.'],
            assert_error.exception.error['unique_entity_id']
        )

    def test_invalidation_cases_for_name_field(self):
        with self.assertRaises(ValidationException) as assert_error:
            self.validator.validate({})
        self.assertListEqual(
            ['This field is required.'],
            assert_error.exception.error['name']
        )

        with self.assertRaises(ValidationException) as assert_error:
            self.validator.validate({'name': None})
        self.assertListEqual(
            ['This field may not be null.'],
            assert_error.exception.error['name']
        )

        with self.assertRaises(ValidationException) as assert_error:
            self.validator.validate({'name': ''})
        self.assertListEqual(
            ['This field may not be blank.'],
            assert_error.exception.error['name']
        )

        with self.assertRaises(ValidationException) as assert_error:
            self.validator.validate({'name': 5})
        self.assertListEqual(
            ['Not a valid string.'],
            assert_error.exception.error['name']
        )

        with self.assertRaises(ValidationException) as assert_error:
            self.validator.validate({'name': 't' * 256})
        self.assertListEqual(
            ['Ensure this field has no more than 255 characters.'],
            assert_error.exception.error['name']
        )

    def test_invalidation_cases_for_description_field(self):
        with self.assertRaises(ValidationException) as assert_error:
            self.validator.validate({'description': 5})
        self.assertEqual(
            ['Not a valid string.'],
            assert_error.exception.error['description']
        )

    def test_invalidation_cases_for_is_active_field(self):
        expected = ['Must be a valid boolean.']
        with self.assertRaises(ValidationException) as assert_error:
            self.validator.validate({'is_active': 5})
        self.assertEqual(
            expected,
            assert_error.exception.error['is_active']
        )

        with self.assertRaises(ValidationException) as assert_error:
            self.validator.validate({'is_active': 0})
        self.assertEqual(
            expected,
            assert_error.exception.error['is_active']
        )

        with self.assertRaises(ValidationException) as assert_error:
            self.validator.validate({'is_active': 1})
        self.assertEqual(
            expected,
            assert_error.exception.error['is_active']
        )

    def test_validate_cases_for_fields(self):
        required_data = {
            'unique_entity_id': UniqueEntityId(),
            'name': 'test',
            'created_at': datetime.now()
        }
        arrange = [
            {**required_data},
            {**required_data, 'description': None},
            {**required_data, 'description': 'description test'},
            {**required_data, 'is_active': True},
            {**required_data, 'is_active': False},
        ]

        for row in arrange:
            self.validator.validate({
                **row
            })
            self.assertEqual(None, self.validator.errors)


# class TestCategoryValidatorUnit(unittest.TestCase):

#     validator: CategoryValidator

#     def setUp(self) -> None:
#         self.validator = CategoryValidator()
#         return super().setUp()

#     def test_if_raises_error_when_constructor_missing_args(self):
#         with self.assertRaises(TypeError) as assert_error:
#             self.validator.validate(None)
#         self.assertEqual(
#             "CategoryRules.__init__() missing 2 required positional arguments: 'id' and 'name'",
#             assert_error.exception.args[0]
#         )

#     def test_invalidation_cases_for_id_field(self):
#         default_props = {'name': None}
#         with self.assertRaises(ValidationException) as assert_error:
#             self.validator.validate({'id': None, **default_props})
#         self.assertIn(
#             'none is not an allowed value',
#             assert_error.exception.error['id']
#         )

#         with self.assertRaises(ValidationException) as assert_error:
#             self.validator.validate({'id': '', **default_props})
#         self.assertIn(
#             'instance of UniqueEntityId, tuple or dict expected',
#             assert_error.exception.error['id']
#         )

#         with self.assertRaises(ValidationException) as assert_error:
#             self.validator.validate({'id': 'fake', **default_props})
#         print(assert_error.exception.error)
#         self.assertIn(
#             'instance of UniqueEntityId, tuple or dict expected',
#             assert_error.exception.error['id']
#         )
#         print(assert_error.exception.error)

#         with self.assertRaises(ValidationException) as assert_error:
#             self.validator.validate(
#                 {'id': ('6160cbcf-3743-4b21-bf41-2ee1484b72fb',), **default_props})
#         self.assertEqual(
#             'field required',
#             assert_error.exception.error['id']
#         )

#     def test_invalidation_cases_for_name_field(self):
#         default_props = {'id': None}
#         with self.assertRaises(ValidationException) as assert_error:
#             self.validator.validate({'name': None, **default_props})
#         self.assertEqual(
#             'none is not an allowed value',
#             assert_error.exception.error['name']
#         )

#         with self.assertRaises(ValidationException) as assert_error:
#             self.validator.validate({'name': '', **default_props})
#         self.assertEqual(
#             'ensure this value has at least 1 characters',
#             assert_error.exception.error['name']
#         )

#         with self.assertRaises(ValidationException) as assert_error:
#             self.validator.validate({'name': 5, **default_props})
#         self.assertEqual(
#             'str type expected',
#             assert_error.exception.error['name']
#         )

#         with self.assertRaises(ValidationException) as assert_error:
#             self.validator.validate({'name': 't' * 256, **default_props})
#         self.assertEqual(
#             'ensure this value has at most 255 characters',
#             assert_error.exception.error['name']
#         )

#     def test_invalidation_cases_for_description_field(self):
#         default_props = {'id': None, 'name': None}
#         with self.assertRaises(ValidationException) as assert_error:
#             self.validator.validate({'description': 5, **default_props})
#         self.assertEqual(
#             'str type expected',
#             assert_error.exception.error['description']
#         )

#     def test_invalidation_cases_for_is_active_field(self):
#         default_props = {'id': None, 'name': None}
#         with self.assertRaises(ValidationException) as assert_error:
#             self.validator.validate({'is_active': 5, **default_props})
#         self.assertEqual(
#             'value is not a valid boolean',
#             assert_error.exception.error['is_active']
#         )

#         with self.assertRaises(ValidationException) as assert_error:
#             self.validator.validate({'is_active': 0, **default_props})
#         self.assertEqual(
#             'value is not a valid boolean',
#             assert_error.exception.error['is_active']
#         )

#         with self.assertRaises(ValidationException) as assert_error:
#             self.validator.validate({'is_active': 1, **default_props})
#         self.assertEqual(
#             'value is not a valid boolean',
#             assert_error.exception.error['is_active']
#         )

#     def test_validate_cases_for_fields(self):
#         # import traceback
#         # try:
#         #     print(UniqueEntityId().id)
#         #     CategoryRules.validate({'id_teste':UniqueEntityId(),'name': 'test'})
#         # except Exception as e:
#         #     lines = traceback.format_exception(type(e), e, e.__traceback__)
#         #     print(''.join(lines))

#         from rest_framework import serializers
#         import django
#         from django.conf import settings
#         settings.configure(
#            USE_I18N=False
#         )
#         print(settings.configured)

#         class CommentSerializer(serializers.Serializer):
#             email = serializers.EmailField()
#             content = serializers.CharField(max_length=200)
#             created = serializers.DateTimeField()

#         serializer = CommentSerializer(data=None)
#         serializer.is_valid()
#         print(serializer.errors)
#         # try:
#         #     self.validator.validate({
#         #         'id': UniqueEntityId(),
#         #         'name': 'test',
#         #     })
#         # except ValidationException as exception:
#         #     self.fail(exception.error)
