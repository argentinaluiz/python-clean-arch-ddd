
from datetime import datetime
from typing import Any, Optional
from pydantic import Field
from pydantic.dataclasses import dataclass
from pydantic.types import constr
from __seedwork.domain.validations import PydanticValidator


@dataclass
class CategoryRules:
    name: constr(min_length=1, max_length=10, strict=True)
    description: Optional[constr(strict=True)] = Field()
    is_active: Optional[bool] = Field()
    created_at: Optional[datetime] = Field()


class CategoryValidator(PydanticValidator):

    def validate(self, data: Any):
        return super()._validate(data, CategoryRules)


class CategoryValidatorFactory:

    @staticmethod
    def create():
        return CategoryValidator()
