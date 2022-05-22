
from datetime import datetime
import unittest
from unittest import mock
from core.category.application import (
    CategoryOutput,
    ListCategoriesUseCase,
    GetCategoryUseCase,
    CreateCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)
from category.api import CategoryResource
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
#from django_app import container
#from django.conf import settings


class TestCategoryResourceUnit(unittest.TestCase):

    # def setUp(self) -> None:
    #     pass
    #     # if not settings.configured:
    #     #     print('adfasdf')
    #     #     settings.configure()

    def test_get_method(self):
        list_use_case = mock.Mock(ListCategoriesUseCase)

        list_use_case.execute.return_value = ListCategoriesUseCase.Output(
            items=[
                CategoryOutput(
                    id='5490020a-e866-4229-9adc-aa44b83234c4',
                    name='Movie',
                    description='some description',
                    is_active=True,
                    created_at=datetime.now()
                )
            ],
            total=1,
            current_page=1,
            per_page=2,
            last_page=1
        )
        mock_execute_method: mock.MagicMock = list_use_case.execute
        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'list_use_case': lambda: list_use_case,
            }
        )
        request = APIRequestFactory().get(
            '/?page=1&per_page=1&sort=name&sort_dir=asc&filter=test')
        request = Request(request)
        response = resource.get(request)
        mock_execute_method.assert_called_with(ListCategoriesUseCase.Input(
            page='1',
            per_page='1',
            sort='name',
            sort_dir='asc',
            filter='test'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'items': [
                {'id': '5490020a-e866-4229-9adc-aa44b83234c4',
                 'name': 'Movie',
                 'description':
                 'some description',
                 'is_active': True,
                 'created_at': list_use_case.execute.return_value.items[0].created_at
                 }
            ],
            'total': 1,
            'current_page': 1,
            'last_page': 1,
            'per_page': 2
        })

    def test_get_object_method(self):
        get_use_case = mock.Mock(GetCategoryUseCase)

        get_use_case.execute.return_value = GetCategoryUseCase.Output(
            id='5490020a-e866-4229-9adc-aa44b83234c4',
            name='Movie',
            description='some description',
            is_active=True,
            created_at=datetime.now()
        )
        mock_execute_method: mock.MagicMock = get_use_case.execute
        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'get_use_case': lambda: get_use_case,
            }
        )
        response = resource.get_object('5490020a-e866-4229-9adc-aa44b83234c4')
        mock_execute_method.assert_called_with(GetCategoryUseCase.Input(
            id='5490020a-e866-4229-9adc-aa44b83234c4'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': '5490020a-e866-4229-9adc-aa44b83234c4',
            'name': 'Movie',
            'description':
            'some description',
            'is_active': True,
            'created_at': get_use_case.execute.return_value.created_at
        })

    def test_post_method(self):
        create_use_case = mock.Mock(CreateCategoryUseCase)

        create_use_case.execute.return_value = CreateCategoryUseCase.Output(
            id='5490020a-e866-4229-9adc-aa44b83234c4',
            name='Movie',
            description=None,
            is_active=True,
            created_at=datetime.now()
        )
        mock_execute_method: mock.MagicMock = create_use_case.execute
        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'create_use_case': lambda: create_use_case,
            }
        )
        send_data = {'name': 'Movie'}
        request = APIRequestFactory().post('/', send_data)
        request = Request(request)
        request._full_data = send_data
        response = resource.post(request)
        mock_execute_method.assert_called_with(CreateCategoryUseCase.Input(
            name='Movie'
        ))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {
            'id': '5490020a-e866-4229-9adc-aa44b83234c4',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': create_use_case.execute.return_value.created_at
        })

    def test_put_method(self):
        update_use_case = mock.Mock(UpdateCategoryUseCase)

        update_use_case.execute.return_value = UpdateCategoryUseCase.Output(
            id='5490020a-e866-4229-9adc-aa44b83234c4',
            name='Movie',
            description=None,
            is_active=True,
            created_at=datetime.now()
        )
        mock_execute_method: mock.MagicMock = update_use_case.execute
        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'update_use_case': lambda: update_use_case,
            }
        )
        send_data = {'name': 'Movie'}
        request = APIRequestFactory().put('/', send_data)
        request = Request(request)
        request._full_data = send_data
        response = resource.put(
            request, '5490020a-e866-4229-9adc-aa44b83234c4')
        mock_execute_method.assert_called_with(UpdateCategoryUseCase.Input(
            id='5490020a-e866-4229-9adc-aa44b83234c4',
            name='Movie'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': '5490020a-e866-4229-9adc-aa44b83234c4',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': update_use_case.execute.return_value.created_at
        })

    def test_delete_method(self):
        delete_use_case = mock.Mock(DeleteCategoryUseCase)

        mock_execute_method: mock.MagicMock = delete_use_case.execute
        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'delete_use_case': lambda: delete_use_case,
            }
        )
        request = APIRequestFactory().delete('/')
        request = Request(request)
        response = resource.delete('5490020a-e866-4229-9adc-aa44b83234c4')
        mock_execute_method.assert_called_with(DeleteCategoryUseCase.Input(
            id='5490020a-e866-4229-9adc-aa44b83234c4',
        ))
        self.assertEqual(response.status_code, 204)

    def __init_all_none(self):
        return {
            'list_use_case': None,
            'get_use_case': None,
            'create_use_case': None,
            'update_use_case': None,
            'delete_use_case': None,
        }
