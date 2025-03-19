from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StructExample1(_message.Message):
    __slots__ = ("integer", "f")
    INTEGER_FIELD_NUMBER: _ClassVar[int]
    F_FIELD_NUMBER: _ClassVar[int]
    integer: float
    f: float
    def __init__(self, integer: _Optional[float] = ..., f: _Optional[float] = ...) -> None: ...

class StructExample2(_message.Message):
    __slots__ = ("name", "ex1")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EX1_FIELD_NUMBER: _ClassVar[int]
    name: str
    ex1: StructExample1
    def __init__(self, name: _Optional[str] = ..., ex1: _Optional[_Union[StructExample1, _Mapping]] = ...) -> None: ...
