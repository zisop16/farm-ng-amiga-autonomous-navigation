from farm_ng.core import linalg_pb2 as _linalg_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegionI32(_message.Message):
    __slots__ = ("is_empty", "min", "max")
    IS_EMPTY_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    is_empty: bool
    min: int
    max: int
    def __init__(self, is_empty: bool = ..., min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...

class RegionF32(_message.Message):
    __slots__ = ("is_empty", "min", "max")
    IS_EMPTY_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    is_empty: bool
    min: float
    max: float
    def __init__(self, is_empty: bool = ..., min: _Optional[float] = ..., max: _Optional[float] = ...) -> None: ...

class RegionF64(_message.Message):
    __slots__ = ("is_empty", "min", "max")
    IS_EMPTY_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    is_empty: bool
    min: float
    max: float
    def __init__(self, is_empty: bool = ..., min: _Optional[float] = ..., max: _Optional[float] = ...) -> None: ...

class Region2F64(_message.Message):
    __slots__ = ("is_empty", "min", "max")
    IS_EMPTY_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    is_empty: bool
    min: _linalg_pb2.Vec2F64
    max: _linalg_pb2.Vec2F64
    def __init__(self, is_empty: bool = ..., min: _Optional[_Union[_linalg_pb2.Vec2F64, _Mapping]] = ..., max: _Optional[_Union[_linalg_pb2.Vec2F64, _Mapping]] = ...) -> None: ...

class RepeatedG0Region2F64(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.RepeatedCompositeFieldContainer[Region2F64]
    def __init__(self, value: _Optional[_Iterable[_Union[Region2F64, _Mapping]]] = ...) -> None: ...
