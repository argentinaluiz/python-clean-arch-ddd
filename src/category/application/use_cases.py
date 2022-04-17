
# pylint: disable=unexpected-keyword-arg

from dataclasses import dataclass,asdict
from typing import Optional
from category.domain.entities import Category
from category.domain.repositories import CategoryRepository
from category.application.dto import CategoryOutput
from __seedwork.application.dto import PaginationOutput, PaginationOutputMapper, SearchInput
from __seedwork.application.use_cases import UseCase

@dataclass(slots=True, frozen=True)
class CreateCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, request: 'Input') -> 'Output':
        category = Category(
            name=request.name,
            description=request.description,
            is_active=request.is_active
        )
        self.category_repo.insert(category)
        return self.__to_output(category)

    def __to_output(self, category: Category) -> 'Output':
        return self.Output(**category.to_dict())

    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        description: Optional[str] = Category.get_field(
            'description').default
        is_active: Optional[bool] = Category.get_field('is_active').default

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class GetCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, request: 'Input') -> 'Output':
        category = self.category_repo.find_by_id(request.id)
        return self.__to_output(category)

    def __to_output(self, category: Category) -> 'Output':
        return self.Output(**category.to_dict())

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class ListCategoriesUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, request: 'Input') -> 'Output':
        search_params = CategoryRepository.SearchParams(**asdict(request))
        result = self.category_repo.search(search_params)
        return self.__to_output(result)

    def __to_output(self, result: CategoryRepository.SearchResult) -> 'Output':
        items = list(map(lambda category: CategoryOutput(
            **category.to_dict()), result.items))
        return PaginationOutputMapper.to_output(items=items, result=result)

    @dataclass(slots=True, frozen=True)
    class Input(SearchInput[str]):
        pass

    @dataclass(slots=True, frozen=True)
    class Output(PaginationOutput[CategoryOutput]):
        pass


@dataclass(slots=True, frozen=True)
class UpdateCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, request: 'Input') -> 'Output':
        entity = self.category_repo.find_by_id(request.id)
        entity.update(request.name, request.description)

        if request.is_active is True:
            entity.activate()

        if request.is_active is False:
            entity.deactivate()

        self.category_repo.update(entity)
        return self.__to_output(entity)

    def __to_output(self, category: Category) -> 'Output':
        return self.Output(**category.to_dict())

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str
        name: str
        description: Optional[str] = Category.get_field(
            'description').default
        is_active: Optional[bool] = Category.get_field('is_active').default

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class DeleteCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, request: 'Input') -> None:
        self.category_repo.delete(request.id)

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str
