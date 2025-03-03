from farm_ng.imu import imu_pb2 as _imu_pb2
from farm_ng.core import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AmigaRobotConfig(_message.Message):
    __slots__ = ("pose_tree", "imus", "wheels")
    class ImusEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _imu_pb2.ImuBias
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_imu_pb2.ImuBias, _Mapping]] = ...) -> None: ...
    class WheelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: WheelConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[WheelConfig, _Mapping]] = ...) -> None: ...
    POSE_TREE_FIELD_NUMBER: _ClassVar[int]
    IMUS_FIELD_NUMBER: _ClassVar[int]
    WHEELS_FIELD_NUMBER: _ClassVar[int]
    pose_tree: _pose_pb2.PoseTree
    imus: _containers.MessageMap[str, _imu_pb2.ImuBias]
    wheels: _containers.MessageMap[str, WheelConfig]
    def __init__(self, pose_tree: _Optional[_Union[_pose_pb2.PoseTree, _Mapping]] = ..., imus: _Optional[_Mapping[str, _imu_pb2.ImuBias]] = ..., wheels: _Optional[_Mapping[str, WheelConfig]] = ...) -> None: ...

class WheelConfig(_message.Message):
    __slots__ = ("canbus_id", "wheel_from_motor_rate", "wheel_diameter_m")
    CANBUS_ID_FIELD_NUMBER: _ClassVar[int]
    WHEEL_FROM_MOTOR_RATE_FIELD_NUMBER: _ClassVar[int]
    WHEEL_DIAMETER_M_FIELD_NUMBER: _ClassVar[int]
    canbus_id: int
    wheel_from_motor_rate: float
    wheel_diameter_m: float
    def __init__(self, canbus_id: _Optional[int] = ..., wheel_from_motor_rate: _Optional[float] = ..., wheel_diameter_m: _Optional[float] = ...) -> None: ...
