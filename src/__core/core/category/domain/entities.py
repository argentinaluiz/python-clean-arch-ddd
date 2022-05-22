
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from core.__seedwork.domain.entities import AggregateRoot
from core.__seedwork.domain.validators import ValidatorRules
from core.category.domain.validations import CategoryValidatorFactory


@dataclass(frozen=True, kw_only=True, slots=True)
class Category(AggregateRoot):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    # pylint: disable=invalid-name,unnecessary-lambda
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()
    )

    def __post_init__(self):
        self.validate()

    def update(self, name: str, description: str = None):
        self._set('name', name)
        self._set('description', description)
        self.validate()

    def activate(self):
        self._set('is_active', True)

    def deactivate(self):
        self._set('is_active', False)

    def validate(self):
        CategoryValidatorFactory.create().validate(
            {**self.to_dict(), 'unique_entity_id': self.unique_entity_id})

    def simple_validate(self):

        ValidatorRules.values(
            self.name, 'name'
        ).required().string().max_length(255)

        ValidatorRules.values(
            self.description, 'description'
        ).string()

        ValidatorRules.values(
            self.is_active, 'is_active'
        ).boolean()
