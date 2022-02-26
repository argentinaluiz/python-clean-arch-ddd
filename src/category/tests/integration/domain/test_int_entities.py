# pylint: disable=unexpected-keyword-arg

from dataclasses import is_dataclass
from datetime import datetime
import unittest
from __seedwork.exceptions import SimpleValidationException

from category.domain.entities import Category


class TestCategoryInt(unittest.TestCase):

    description = 'some description'

    def test_invalidation_of_entity(self):
        with self.assertRaises(SimpleValidationException) as assert_error:
            Category(name='').simple_validate()
        self.assertEqual('The name is required',
                         assert_error.exception.args[0])

        with self.assertRaises(SimpleValidationException) as assert_error:
            Category(name=5).simple_validate()
        self.assertEqual('The name must be a string',
                         assert_error.exception.args[0])

        with self.assertRaises(
            SimpleValidationException,
        ) as assert_error:
            Category(name='t' * 256).simple_validate()
        self.assertEqual('The name must be less than 255 characters',
                         assert_error.exception.args[0])

        with self.assertRaises(SimpleValidationException) as assert_error:
            Category(name='t', description=5).simple_validate()
        self.assertEqual('The description must be a string',
                         assert_error.exception.args[0])

        with self.assertRaises(SimpleValidationException) as assert_error:
            Category(name='t', is_active=5).simple_validate()
        self.assertEqual('The is_active must be a boolean',
                         assert_error.exception.args[0])
