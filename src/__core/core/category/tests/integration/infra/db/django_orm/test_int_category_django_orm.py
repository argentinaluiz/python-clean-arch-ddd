import unittest
from core.category.infra import CategoryModel

class TestCategoryModelInt(unittest.TestCase):

    def test_something(self):
        CategoryModel.objects.create(name='Movie')