from farm_ng.core import linalg_pb2 as _linalg_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UnitVec3F64(_message.Message):
    __slots__ = ("vec3",)
    VEC3_FIELD_NUMBER: _ClassVar[int]
    vec3: _linalg_pb2.Vec3F64
    def __init__(self, vec3: _Optional[_Union[_linalg_pb2.Vec3F64, _Mapping]] = ...) -> None: ...

class Hyperplane3F64(_message.Message):
    __slots__ = ("normal", "offset")
    NORMAL_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    normal: UnitVec3F64
    offset: float
    def __init__(self, normal: _Optional[_Union[UnitVec3F64, _Mapping]] = ..., offset: _Optional[float] = ...) -> None: ...
