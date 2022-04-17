
from typing import List
from __seedwork.domain.repositories import InMemorySearchableRepository, SortDirection
from category.domain.entities import Category
from category.domain.repositories import CategoryRepository


class CategoryInMemoryRepository(CategoryRepository, InMemorySearchableRepository[Category]):
    sortable_fields: List[str] = ["name", "created_at"]

    def _apply_filter(self, items: List[Category], filter_param: str = None) -> List[Category]:
        if filter_param:
            filter_obj = filter(
                lambda i: filter_param.lower() in i.name.lower(),
                items
            )
            return list(filter_obj)

        return items

    def _apply_sort(self, items: List[Category], sort: str = None, sort_dir: SortDirection = None) -> List[Category]:
        return super()._apply_sort(items, "created_at", "desc") \
                if not sort \
                else super()._apply_sort(items, sort, sort_dir)
