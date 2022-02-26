import dataclasses
from datetime import datetime
from typing import List, Optional, Annotated, Union, Any

from pydantic import Field, constr, AnyHttpUrl, NoneStr
from pydantic.dataclasses import dataclass
from pydantic import validate_arguments
from pydantic.types import ConstrainedStr, StrictStr
from pydantic.validators import str_validator
from pydantic import Field, errors


def empty_to_none(v: str) -> Optional[str]:
    if v == '':
        print('two')
        raise errors.NoneIsNotAllowedError()
    # if v == '':
    #     print('two')
    #     raise errors.MissingError()
    # if v is None:
    #     raise errors.MissingError()
    print('three')
    return v


class NotStrEmpty(str):
    @classmethod
    def __get_validators__(cls):
        yield empty_to_none


@dataclass()
class Category:
    name: constr(min_length=1, max_length=10, strict=True)
    description: Optional[constr(strict=True)] = Field()
    is_active: Optional[bool] = Field()
    created_at: Optional[datetime] = Field()
    #id: Optional[constr(max_length=10, strict=True)] = Field(...)
    # name: EmptyStrToNone =  # Field(...)
    #name: StrictStr =  Field(..., min_length=1, max_length=255)
    #name: Union[NotStrEmpty, constr(max_length=10, strict=True)] = None
    #name: constr(min_length=1, max_length=10, strict=True) #= Field()
    #name: constr(max_length=10, strict=True)
    #test: bool
    # friends: List[int] = dataclasses.field(default_factory=lambda: [0])
    # age: Optional[int] = dataclasses.field(
    #     default=None,
    #     metadata=dict(title='The age of the user', description='do not lie!')
    # )
    # height: Optional[int] = Field(None, title='The height in cm', ge=50, le=300)


user = Category(name='')
print(vars(user))
