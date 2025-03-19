from farm_ng.core import linalg_pb2 as _linalg_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QuaternionF64(_message.Message):
    __slots__ = ("imag", "real")
    IMAG_FIELD_NUMBER: _ClassVar[int]
    REAL_FIELD_NUMBER: _ClassVar[int]
    imag: _linalg_pb2.Vec3F64
    real: float
    def __init__(self, imag: _Optional[_Union[_linalg_pb2.Vec3F64, _Mapping]] = ..., real: _Optional[float] = ...) -> None: ...

class Rotation2F64(_message.Message):
    __slots__ = ("theta",)
    THETA_FIELD_NUMBER: _ClassVar[int]
    theta: float
    def __init__(self, theta: _Optional[float] = ...) -> None: ...

class Isometry2F64(_message.Message):
    __slots__ = ("rotation", "translation")
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    rotation: Rotation2F64
    translation: _linalg_pb2.Vec2F64
    def __init__(self, rotation: _Optional[_Union[Rotation2F64, _Mapping]] = ..., translation: _Optional[_Union[_linalg_pb2.Vec2F64, _Mapping]] = ...) -> None: ...

class Rotation3F64(_message.Message):
    __slots__ = ("unit_quaternion",)
    UNIT_QUATERNION_FIELD_NUMBER: _ClassVar[int]
    unit_quaternion: QuaternionF64
    def __init__(self, unit_quaternion: _Optional[_Union[QuaternionF64, _Mapping]] = ...) -> None: ...

class Isometry3F64(_message.Message):
    __slots__ = ("rotation", "translation")
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    rotation: Rotation3F64
    translation: _linalg_pb2.Vec3F64
    def __init__(self, rotation: _Optional[_Union[Rotation3F64, _Mapping]] = ..., translation: _Optional[_Union[_linalg_pb2.Vec3F64, _Mapping]] = ...) -> None: ...

class Isometry3F64Tangent(_message.Message):
    __slots__ = ("linear_velocity", "angular_velocity")
    LINEAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    linear_velocity: _linalg_pb2.Vec3F64
    angular_velocity: _linalg_pb2.Vec3F64
    def __init__(self, linear_velocity: _Optional[_Union[_linalg_pb2.Vec3F64, _Mapping]] = ..., angular_velocity: _Optional[_Union[_linalg_pb2.Vec3F64, _Mapping]] = ...) -> None: ...
