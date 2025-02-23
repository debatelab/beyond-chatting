from abc import ABC
from multipledispatch import dispatch  # type: ignore


class Pipable(ABC):
    def __or__(self, other):
        return self.__class__(other(self))


class PipableStr(str, Pipable):
    "Pipable string"


class PipableDict(dict, Pipable):
    "Pipable dict"
    def __or__(self, other):
        composite = self.__class__(**self)
        composite.update(output=other(**self))
        return composite


class Inputs():

    @dispatch(str)
    def __call__(self, arg):
        return PipableStr(arg)

    @dispatch(dict)  # type: ignore
    def __call__(self, arg):  # noqa: F811
        return PipableDict(arg)

