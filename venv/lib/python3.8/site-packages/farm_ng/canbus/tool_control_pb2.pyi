from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HBridgeCommandType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HBRIDGE_UNKNOWN: _ClassVar[HBridgeCommandType]
    HBRIDGE_PASSIVE: _ClassVar[HBridgeCommandType]
    HBRIDGE_FORWARD: _ClassVar[HBridgeCommandType]
    HBRIDGE_STOPPED: _ClassVar[HBridgeCommandType]
    HBRIDGE_REVERSE: _ClassVar[HBridgeCommandType]

class PtoCommandType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PTO_UNKNOWN: _ClassVar[PtoCommandType]
    PTO_PASSIVE: _ClassVar[PtoCommandType]
    PTO_FORWARD: _ClassVar[PtoCommandType]
    PTO_STOPPED: _ClassVar[PtoCommandType]
    PTO_REVERSE: _ClassVar[PtoCommandType]

class BugDispenserState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUG_DISPENSER_UNKNOW: _ClassVar[BugDispenserState]
    BUG_DISPENSER_ACTIVE: _ClassVar[BugDispenserState]
    BUG_DISPENSER_STOPPED: _ClassVar[BugDispenserState]

class ToolCommandReply(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TOOL_UNKNOWN: _ClassVar[ToolCommandReply]
    TOOL_PASSIVE: _ClassVar[ToolCommandReply]
    TOOL_FORWARD: _ClassVar[ToolCommandReply]
    TOOL_STOPPED: _ClassVar[ToolCommandReply]
    TOOL_REVERSE: _ClassVar[ToolCommandReply]

class HBridgeDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HBRIDGE_DIRECTION_UNKNOWN: _ClassVar[HBridgeDirection]
    HBRIDGE_DIRECTION_FORWARD: _ClassVar[HBridgeDirection]
    HBRIDGE_DIRECTION_REVERSE: _ClassVar[HBridgeDirection]
    HBRIDGE_DIRECTION_STOPPED: _ClassVar[HBridgeDirection]
    HBRIDGE_DIRECTION_BRAKING: _ClassVar[HBridgeDirection]

class HBridgeFaultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HBRIDGE_UNKNOWN_FAULT: _ClassVar[HBridgeFaultCode]
    HBRIDGE_SHORT_CIRCUIT_FORWARD: _ClassVar[HBridgeFaultCode]
    HBRIDGE_SHORT_CIRCUIT_REVERSE: _ClassVar[HBridgeFaultCode]
    HBRIDGE_OVERCURRENT_FORWARD: _ClassVar[HBridgeFaultCode]
    HBRIDGE_OVERCURRENT_REVERSE: _ClassVar[HBridgeFaultCode]
    HBRIDGE_INRUSH_OVERCURRENT_FORWARD: _ClassVar[HBridgeFaultCode]
    HBRIDGE_INRUSH_OVERCURRENT_REVERSE: _ClassVar[HBridgeFaultCode]
    HBRIDGE_BATTERY_OVERVOLTAGE: _ClassVar[HBridgeFaultCode]
    HBRIDGE_BATTERY_UNDERVOLTAGE: _ClassVar[HBridgeFaultCode]
    HBRIDGE_OVER_TEMPERATURE: _ClassVar[HBridgeFaultCode]
    HBRIDGE_OUTPUT_INCORRECT_STATE: _ClassVar[HBridgeFaultCode]
    HBRIDGE_COMMUNICATION_LOSS: _ClassVar[HBridgeFaultCode]

class PtoFaultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PTO_UNKNOWN_FAULT: _ClassVar[PtoFaultCode]
HBRIDGE_UNKNOWN: HBridgeCommandType
HBRIDGE_PASSIVE: HBridgeCommandType
HBRIDGE_FORWARD: HBridgeCommandType
HBRIDGE_STOPPED: HBridgeCommandType
HBRIDGE_REVERSE: HBridgeCommandType
PTO_UNKNOWN: PtoCommandType
PTO_PASSIVE: PtoCommandType
PTO_FORWARD: PtoCommandType
PTO_STOPPED: PtoCommandType
PTO_REVERSE: PtoCommandType
BUG_DISPENSER_UNKNOW: BugDispenserState
BUG_DISPENSER_ACTIVE: BugDispenserState
BUG_DISPENSER_STOPPED: BugDispenserState
TOOL_UNKNOWN: ToolCommandReply
TOOL_PASSIVE: ToolCommandReply
TOOL_FORWARD: ToolCommandReply
TOOL_STOPPED: ToolCommandReply
TOOL_REVERSE: ToolCommandReply
HBRIDGE_DIRECTION_UNKNOWN: HBridgeDirection
HBRIDGE_DIRECTION_FORWARD: HBridgeDirection
HBRIDGE_DIRECTION_REVERSE: HBridgeDirection
HBRIDGE_DIRECTION_STOPPED: HBridgeDirection
HBRIDGE_DIRECTION_BRAKING: HBridgeDirection
HBRIDGE_UNKNOWN_FAULT: HBridgeFaultCode
HBRIDGE_SHORT_CIRCUIT_FORWARD: HBridgeFaultCode
HBRIDGE_SHORT_CIRCUIT_REVERSE: HBridgeFaultCode
HBRIDGE_OVERCURRENT_FORWARD: HBridgeFaultCode
HBRIDGE_OVERCURRENT_REVERSE: HBridgeFaultCode
HBRIDGE_INRUSH_OVERCURRENT_FORWARD: HBridgeFaultCode
HBRIDGE_INRUSH_OVERCURRENT_REVERSE: HBridgeFaultCode
HBRIDGE_BATTERY_OVERVOLTAGE: HBridgeFaultCode
HBRIDGE_BATTERY_UNDERVOLTAGE: HBridgeFaultCode
HBRIDGE_OVER_TEMPERATURE: HBridgeFaultCode
HBRIDGE_OUTPUT_INCORRECT_STATE: HBridgeFaultCode
HBRIDGE_COMMUNICATION_LOSS: HBridgeFaultCode
PTO_UNKNOWN_FAULT: PtoFaultCode

class HBridgeCommand(_message.Message):
    __slots__ = ("id", "command")
    ID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    id: int
    command: HBridgeCommandType
    def __init__(self, id: _Optional[int] = ..., command: _Optional[_Union[HBridgeCommandType, str]] = ...) -> None: ...

class PtoCommand(_message.Message):
    __slots__ = ("id", "command", "rpm")
    ID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    RPM_FIELD_NUMBER: _ClassVar[int]
    id: int
    command: PtoCommandType
    rpm: float
    def __init__(self, id: _Optional[int] = ..., command: _Optional[_Union[PtoCommandType, str]] = ..., rpm: _Optional[float] = ...) -> None: ...

class BugDispenserCommand(_message.Message):
    __slots__ = ("id", "rate", "state")
    ID_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    id: int
    rate: float
    state: BugDispenserState
    def __init__(self, id: _Optional[int] = ..., rate: _Optional[float] = ..., state: _Optional[_Union[BugDispenserState, str]] = ...) -> None: ...

class ActuatorCommands(_message.Message):
    __slots__ = ("hbridges", "ptos", "bug_dispensers")
    HBRIDGES_FIELD_NUMBER: _ClassVar[int]
    PTOS_FIELD_NUMBER: _ClassVar[int]
    BUG_DISPENSERS_FIELD_NUMBER: _ClassVar[int]
    hbridges: _containers.RepeatedCompositeFieldContainer[HBridgeCommand]
    ptos: _containers.RepeatedCompositeFieldContainer[PtoCommand]
    bug_dispensers: _containers.RepeatedCompositeFieldContainer[BugDispenserCommand]
    def __init__(self, hbridges: _Optional[_Iterable[_Union[HBridgeCommand, _Mapping]]] = ..., ptos: _Optional[_Iterable[_Union[PtoCommand, _Mapping]]] = ..., bug_dispensers: _Optional[_Iterable[_Union[BugDispenserCommand, _Mapping]]] = ...) -> None: ...

class HBridgeStatus(_message.Message):
    __slots__ = ("stamp", "id", "command_reply", "faults", "direction")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_REPLY_FIELD_NUMBER: _ClassVar[int]
    FAULTS_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    stamp: float
    id: int
    command_reply: ToolCommandReply
    faults: _containers.RepeatedScalarFieldContainer[HBridgeFaultCode]
    direction: HBridgeDirection
    def __init__(self, stamp: _Optional[float] = ..., id: _Optional[int] = ..., command_reply: _Optional[_Union[ToolCommandReply, str]] = ..., faults: _Optional[_Iterable[_Union[HBridgeFaultCode, str]]] = ..., direction: _Optional[_Union[HBridgeDirection, str]] = ...) -> None: ...

class PtoStatus(_message.Message):
    __slots__ = ("stamp", "id", "command_reply", "faults", "rpm", "gear_ratio")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_REPLY_FIELD_NUMBER: _ClassVar[int]
    FAULTS_FIELD_NUMBER: _ClassVar[int]
    RPM_FIELD_NUMBER: _ClassVar[int]
    GEAR_RATIO_FIELD_NUMBER: _ClassVar[int]
    stamp: float
    id: int
    command_reply: ToolCommandReply
    faults: _containers.RepeatedScalarFieldContainer[PtoFaultCode]
    rpm: float
    gear_ratio: float
    def __init__(self, stamp: _Optional[float] = ..., id: _Optional[int] = ..., command_reply: _Optional[_Union[ToolCommandReply, str]] = ..., faults: _Optional[_Iterable[_Union[PtoFaultCode, str]]] = ..., rpm: _Optional[float] = ..., gear_ratio: _Optional[float] = ...) -> None: ...

class BugDispenserStatus(_message.Message):
    __slots__ = ("stamp", "id", "state", "rate", "bug_dispenser_is_dispensing", "volume_dispensed")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    BUG_DISPENSER_IS_DISPENSING_FIELD_NUMBER: _ClassVar[int]
    VOLUME_DISPENSED_FIELD_NUMBER: _ClassVar[int]
    stamp: float
    id: int
    state: BugDispenserState
    rate: float
    bug_dispenser_is_dispensing: bool
    volume_dispensed: float
    def __init__(self, stamp: _Optional[float] = ..., id: _Optional[int] = ..., state: _Optional[_Union[BugDispenserState, str]] = ..., rate: _Optional[float] = ..., bug_dispenser_is_dispensing: bool = ..., volume_dispensed: _Optional[float] = ...) -> None: ...

class ToolStatuses(_message.Message):
    __slots__ = ("hbridges", "ptos", "bug_dispensers")
    HBRIDGES_FIELD_NUMBER: _ClassVar[int]
    PTOS_FIELD_NUMBER: _ClassVar[int]
    BUG_DISPENSERS_FIELD_NUMBER: _ClassVar[int]
    hbridges: _containers.RepeatedCompositeFieldContainer[HBridgeStatus]
    ptos: _containers.RepeatedCompositeFieldContainer[PtoStatus]
    bug_dispensers: _containers.RepeatedCompositeFieldContainer[BugDispenserStatus]
    def __init__(self, hbridges: _Optional[_Iterable[_Union[HBridgeStatus, _Mapping]]] = ..., ptos: _Optional[_Iterable[_Union[PtoStatus, _Mapping]]] = ..., bug_dispensers: _Optional[_Iterable[_Union[BugDispenserStatus, _Mapping]]] = ...) -> None: ...
