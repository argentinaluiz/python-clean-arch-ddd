# pylint: disable=unexpected-keyword-arg

from dataclasses import is_dataclass
from datetime import datetime
import unittest
from core.__seedwork.domain.exceptions import SimpleValidationException, ValidationException

from core.category.domain.entities import Category


class TestCategoryInt(unittest.TestCase):

    def test_a_valid_entity(self):
        try:
            # pylint: disable=expression-not-assigned
            Category(name='Movie')
            Category(name='Movie', description=None)
            Category(name='Movie', is_active=True)
            Category(name='Movie', is_active=False)
            Category(name='Movie', description='description test',
                     is_active=False)
        except ValidationException as exception:
            self.fail(
                f'Some object is not a valid category {exception.error}'
            )

    def test_a_invalid_entity_using_name_field(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name=None)
        self.assertEqual(['This field may not be null.'],
                         assert_error.exception.error['name'])

        with self.assertRaises(ValidationException) as assert_error:
            Category(name="")
        self.assertEqual(['This field may not be blank.'],
                         assert_error.exception.error['name'])

        with self.assertRaises(ValidationException) as assert_error:
            Category(name=5)
        self.assertEqual(['Not a valid string.'],
                         assert_error.exception.error['name'])

    def test_a_invalid_entity_using_description_field(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name=None, description=5)
        self.assertEqual(['Not a valid string.'],
                         assert_error.exception.error['description'])

    def test_a_invalid_entity_using_is_active_field(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name=None, is_active=5)
        self.assertEqual(['Must be a valid boolean.'],
                         assert_error.exception.error['is_active'])


# class TestCategoryInt(unittest.TestCase):

#     description = 'some description'

#     def test_invalidation_of_entity(self):
#         with self.assertRaises(SimpleValidationException) as assert_error:
#             Category(name='').simple_validate()
#         self.assertEqual('The name is required',
#                          assert_error.exception.args[0])

#         with self.assertRaises(SimpleValidationException) as assert_error:
#             Category(name=5).simple_validate()
#         self.assertEqual('The name must be a string',
#                          assert_error.exception.args[0])

#         with self.assertRaises(
#             SimpleValidationException,
#         ) as assert_error:
#             Category(name='t' * 256).simple_validate()
#         self.assertEqual('The name must be less than 255 characters',
#                          assert_error.exception.args[0])

#         with self.assertRaises(SimpleValidationException) as assert_error:
#             Category(name='t', description=5).simple_validate()
#         self.assertEqual('The description must be a string',
#                          assert_error.exception.args[0])

#         with self.assertRaises(SimpleValidationException) as assert_error:
#             Category(name='t', is_active=5).simple_validate()
#         self.assertEqual('The is_active must be a boolean',
#                          assert_error.exception.args[0])

    # def test_invalidation_of_entity(self):
    #     with self.assertRaises(SimpleValidationException) as assert_error:
    #         Category(name='').simple_validate()
    #     self.assertEqual('The name is required',
    #                      assert_error.exception.args[0])

    #     with self.assertRaises(SimpleValidationException) as assert_error:
    #         Category(name=5).simple_validate()
    #     self.assertEqual('The name must be a string',
    #                      assert_error.exception.args[0])

    #     with self.assertRaises(
    #         SimpleValidationException,
    #     ) as assert_error:
    #         Category(name='t' * 256).simple_validate()
    #     self.assertEqual('The name must be less than 255 characters',
    #                      assert_error.exception.args[0])

    #     with self.assertRaises(SimpleValidationException) as assert_error:
    #         Category(name='t', description=5).simple_validate()
    #     self.assertEqual('The description must be a string',
    #                      assert_error.exception.args[0])

    #     with self.assertRaises(SimpleValidationException) as assert_error:
    #         Category(name='t', is_active=5).simple_validate()
    #     self.assertEqual('The is_active must be a boolean',
    #                      assert_error.exception.args[0])
