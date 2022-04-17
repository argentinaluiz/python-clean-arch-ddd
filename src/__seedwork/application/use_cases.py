from abc import ABC
import abc
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')


class UseCase(Generic[Input, Output], ABC):
    @abc.abstractmethod
    def execute(self, request: Input) -> Output:
        raise NotImplementedError()
