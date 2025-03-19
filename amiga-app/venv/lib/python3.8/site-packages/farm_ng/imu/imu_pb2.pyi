from farm_ng.core import linalg_pb2 as _linalg_pb2
from farm_ng.core import lie_pb2 as _lie_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImuBias(_message.Message):
    __slots__ = ("gyro_bias", "accelero_bias")
    GYRO_BIAS_FIELD_NUMBER: _ClassVar[int]
    ACCELERO_BIAS_FIELD_NUMBER: _ClassVar[int]
    gyro_bias: _linalg_pb2.Vec3F64
    accelero_bias: _linalg_pb2.Vec3F64
    def __init__(self, gyro_bias: _Optional[_Union[_linalg_pb2.Vec3F64, _Mapping]] = ..., accelero_bias: _Optional[_Union[_linalg_pb2.Vec3F64, _Mapping]] = ...) -> None: ...

class Imu(_message.Message):
    __slots__ = ("angular_velocity", "linear_acceleration", "orientation", "bias")
    ANGULAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    LINEAR_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    BIAS_FIELD_NUMBER: _ClassVar[int]
    angular_velocity: _linalg_pb2.Vec3F64
    linear_acceleration: _linalg_pb2.Vec3F64
    orientation: _lie_pb2.QuaternionF64
    bias: ImuBias
    def __init__(self, angular_velocity: _Optional[_Union[_linalg_pb2.Vec3F64, _Mapping]] = ..., linear_acceleration: _Optional[_Union[_linalg_pb2.Vec3F64, _Mapping]] = ..., orientation: _Optional[_Union[_lie_pb2.QuaternionF64, _Mapping]] = ..., bias: _Optional[_Union[ImuBias, _Mapping]] = ...) -> None: ...
