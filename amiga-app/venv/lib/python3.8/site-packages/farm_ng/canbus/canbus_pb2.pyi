from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MotorControllerStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PRE_OPERATIONAL: _ClassVar[MotorControllerStatus]
    IDLE: _ClassVar[MotorControllerStatus]
    POST_OPERATIONAL: _ClassVar[MotorControllerStatus]
    RUN: _ClassVar[MotorControllerStatus]
    FAULT: _ClassVar[MotorControllerStatus]
PRE_OPERATIONAL: MotorControllerStatus
IDLE: MotorControllerStatus
POST_OPERATIONAL: MotorControllerStatus
RUN: MotorControllerStatus
FAULT: MotorControllerStatus

class Twist2d(_message.Message):
    __slots__ = ("linear_velocity_x", "linear_velocity_y", "angular_velocity")
    LINEAR_VELOCITY_X_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_Y_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    linear_velocity_x: float
    linear_velocity_y: float
    angular_velocity: float
    def __init__(self, linear_velocity_x: _Optional[float] = ..., linear_velocity_y: _Optional[float] = ..., angular_velocity: _Optional[float] = ...) -> None: ...

class RawCanbusMessage(_message.Message):
    __slots__ = ("stamp", "id", "error", "remote_transmission", "data")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REMOTE_TRANSMISSION_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    stamp: float
    id: int
    error: bool
    remote_transmission: bool
    data: bytes
    def __init__(self, stamp: _Optional[float] = ..., id: _Optional[int] = ..., error: bool = ..., remote_transmission: bool = ..., data: _Optional[bytes] = ...) -> None: ...

class RawCanbusMessages(_message.Message):
    __slots__ = ("messages",)
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[RawCanbusMessage]
    def __init__(self, messages: _Optional[_Iterable[_Union[RawCanbusMessage, _Mapping]]] = ...) -> None: ...

class MotorState(_message.Message):
    __slots__ = ("stamp", "id", "status", "rpm", "voltage", "current", "temperature")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RPM_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    stamp: float
    id: int
    status: int
    rpm: int
    voltage: float
    current: float
    temperature: int
    def __init__(self, stamp: _Optional[float] = ..., id: _Optional[int] = ..., status: _Optional[int] = ..., rpm: _Optional[int] = ..., voltage: _Optional[float] = ..., current: _Optional[float] = ..., temperature: _Optional[int] = ...) -> None: ...

class MotorStates(_message.Message):
    __slots__ = ("motors",)
    MOTORS_FIELD_NUMBER: _ClassVar[int]
    motors: _containers.RepeatedCompositeFieldContainer[MotorState]
    def __init__(self, motors: _Optional[_Iterable[_Union[MotorState, _Mapping]]] = ...) -> None: ...
