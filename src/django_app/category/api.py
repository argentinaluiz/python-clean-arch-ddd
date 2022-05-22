from dataclasses import asdict, dataclass, field
from typing import Callable
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from core.category.application.use_cases import (
    DeleteCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    CreateCategoryUseCase,
    UpdateCategoryUseCase
)
from core.__seedwork.domain.exceptions import ValidationException


@dataclass(slots=True)
class CategoryResource(APIView):

    # list_use_case: ListCategoriesUseCase = field(
    #     default_factory=container.use_case_category_list_categories
    # )

    # get_use_case: GetCategoryUseCase = field(
    #     default_factory=container.use_case_category_get_category
    # )

    # create_use_case: CreateCategoryUseCase = field(
    #     default_factory=container.use_case_category_create_category
    # )

    # update_use_case: UpdateCategoryUseCase = field(
    #     default_factory=container.use_case_category_update_category
    # )

    # delete_use_case: DeleteCategoryUseCase = field(
    #     default_factory=container.use_case_category_delete_category
    # )

    list_use_case: Callable[[], ListCategoriesUseCase]
    get_use_case: Callable[[], GetCategoryUseCase]
    create_use_case: Callable[[], CreateCategoryUseCase]
    update_use_case: Callable[[], UpdateCategoryUseCase]
    delete_use_case: Callable[[], DeleteCategoryUseCase]

    # list_use_case: ListCategoriesUseCase = None
    # get_use_case: GetCategoryUseCase = None
    # create_use_case: CreateCategoryUseCase = None
    # update_use_case: UpdateCategoryUseCase = None
    # delete_use_case: DeleteCategoryUseCase = None

    def get(self, request: Request):
        input = ListCategoriesUseCase.Input(**request.query_params.dict())
        output = self.list_use_case().execute(input)
        print(output)
        return Response(asdict(output))

    def get_object(self, pk):
        input = GetCategoryUseCase.Input(id=pk)
        output = self.get_use_case().execute(input)
        return Response(asdict(output))

    def post(self, request: Request):
        input = CreateCategoryUseCase.Input(**request.data)
        output = self.create_use_case().execute(input)
        return Response(asdict(output), status=status.HTTP_201_CREATED)

    def put(self, request: Request, pk):
        input = UpdateCategoryUseCase.Input(**{'id': pk, **request.data})
        output = self.update_use_case().execute(input)
        return Response(asdict(output))

    def delete(self, pk):
        input = DeleteCategoryUseCase.Input(id=pk)
        self.delete_use_case().execute(input)
        return Response(status=status.HTTP_204_NO_CONTENT)
