
from rest_framework import serializers

from typing import Any
from core.__seedwork.domain.validators import (
    DRFValidator,
    StrictBooleanField,
    StrictCharField,
    UniqueEntityIdField
)

# pylint: disable=abstract-method


class CategoryRules(serializers.Serializer):
    unique_entity_id = UniqueEntityIdField()
    name = StrictCharField(max_length=255)
    description = StrictCharField(required=False, allow_null=True)
    is_active = StrictBooleanField(required=False)
    created_at = serializers.DateTimeField()

class CategoryValidator(DRFValidator): # pylint: disable=too-few-public-methods

    def validate(self, data: Any):
        return super()._validate(CategoryRules(data=data))


class CategoryValidatorFactory: # pylint: disable=too-few-public-methods

    @staticmethod
    def create():
        return CategoryValidator()


# class Config:
#     arbitrary_types_allowed = False

# #@dataclass(config=Config)
# class CategoryRules(BaseModel):
#     # pylint: disable=invalid-name
#     id_teste: UniqueEntityId
#     name: constr(min_length=1, max_length=255, strict=True)
#     description: Optional[constr(strict=True)] = Field()
#     is_active: Optional[StrictBool] = Field()
#     created_at: Optional[datetime] = Field()

#     class Config:
#         allow_population_by_field_name = False

# class CategoryValidator(PydanticValidator):

#     def validate(self, data: Any):
#         return super()._validate(data, CategoryRules)
