
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from category.domain.entities import Category


@dataclass(frozen=True, slots=True)
class CategoryOutput:
    id: str
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime


class CategoryOutputMapper:
    @staticmethod
    def to_output(category: Category) -> CategoryOutput:
        return CategoryOutput(
            id=str(category.id),
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at
        )
