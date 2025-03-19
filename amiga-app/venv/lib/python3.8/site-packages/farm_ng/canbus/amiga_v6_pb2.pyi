from farm_ng.canbus import canbus_pb2 as _canbus_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AmigaControlState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATE_BOOT: _ClassVar[AmigaControlState]
    STATE_MANUAL_READY: _ClassVar[AmigaControlState]
    STATE_MANUAL_ACTIVE: _ClassVar[AmigaControlState]
    STATE_CC_ACTIVE: _ClassVar[AmigaControlState]
    STATE_AUTO_READY: _ClassVar[AmigaControlState]
    STATE_AUTO_ACTIVE: _ClassVar[AmigaControlState]
    STATE_ESTOPPED: _ClassVar[AmigaControlState]

class ConfigOperationIds(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_OPERATION: _ClassVar[ConfigOperationIds]
    READ: _ClassVar[ConfigOperationIds]
    WRITE: _ClassVar[ConfigOperationIds]
    STORE: _ClassVar[ConfigOperationIds]

class ConfigValueIds(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_VALUE: _ClassVar[ConfigValueIds]
    VEL_MAX: _ClassVar[ConfigValueIds]
    FLIP_JOYSTICK: _ClassVar[ConfigValueIds]
    MAX_TURN_RATE: _ClassVar[ConfigValueIds]
    MIN_TURN_RATE: _ClassVar[ConfigValueIds]
    MAX_ANG_ACC: _ClassVar[ConfigValueIds]
    M10_ON: _ClassVar[ConfigValueIds]
    M11_ON: _ClassVar[ConfigValueIds]
    M12_ON: _ClassVar[ConfigValueIds]
    M13_ON: _ClassVar[ConfigValueIds]
    BATT_LO: _ClassVar[ConfigValueIds]
    BATT_HI: _ClassVar[ConfigValueIds]
    TURTLE_V: _ClassVar[ConfigValueIds]
    TURTLE_W: _ClassVar[ConfigValueIds]
    WHEEL_TRACK: _ClassVar[ConfigValueIds]
    WHEEL_GEAR_RATIO: _ClassVar[ConfigValueIds]
    WHEEL_RADIUS: _ClassVar[ConfigValueIds]
    PTO_CUR_DEV: _ClassVar[ConfigValueIds]
    PTO_CUR_RPM: _ClassVar[ConfigValueIds]
    PTO_MIN_RPM: _ClassVar[ConfigValueIds]
    PTO_MAX_RPM: _ClassVar[ConfigValueIds]
    PTO_DEF_RPM: _ClassVar[ConfigValueIds]
    PTO_GEAR_RATIO: _ClassVar[ConfigValueIds]
    STEERING_GAMMA: _ClassVar[ConfigValueIds]

class ConfigValueUnits(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_UNITS: _ClassVar[ConfigValueUnits]
    UNITLESS: _ClassVar[ConfigValueUnits]
    METERS: _ClassVar[ConfigValueUnits]
    MPS: _ClassVar[ConfigValueUnits]
    RADPS: _ClassVar[ConfigValueUnits]
    RPM: _ClassVar[ConfigValueUnits]
    MS2: _ClassVar[ConfigValueUnits]
    RADS2: _ClassVar[ConfigValueUnits]
    VOLTS: _ClassVar[ConfigValueUnits]
STATE_BOOT: AmigaControlState
STATE_MANUAL_READY: AmigaControlState
STATE_MANUAL_ACTIVE: AmigaControlState
STATE_CC_ACTIVE: AmigaControlState
STATE_AUTO_READY: AmigaControlState
STATE_AUTO_ACTIVE: AmigaControlState
STATE_ESTOPPED: AmigaControlState
NO_OPERATION: ConfigOperationIds
READ: ConfigOperationIds
WRITE: ConfigOperationIds
STORE: ConfigOperationIds
NO_VALUE: ConfigValueIds
VEL_MAX: ConfigValueIds
FLIP_JOYSTICK: ConfigValueIds
MAX_TURN_RATE: ConfigValueIds
MIN_TURN_RATE: ConfigValueIds
MAX_ANG_ACC: ConfigValueIds
M10_ON: ConfigValueIds
M11_ON: ConfigValueIds
M12_ON: ConfigValueIds
M13_ON: ConfigValueIds
BATT_LO: ConfigValueIds
BATT_HI: ConfigValueIds
TURTLE_V: ConfigValueIds
TURTLE_W: ConfigValueIds
WHEEL_TRACK: ConfigValueIds
WHEEL_GEAR_RATIO: ConfigValueIds
WHEEL_RADIUS: ConfigValueIds
PTO_CUR_DEV: ConfigValueIds
PTO_CUR_RPM: ConfigValueIds
PTO_MIN_RPM: ConfigValueIds
PTO_MAX_RPM: ConfigValueIds
PTO_DEF_RPM: ConfigValueIds
PTO_GEAR_RATIO: ConfigValueIds
STEERING_GAMMA: ConfigValueIds
NO_UNITS: ConfigValueUnits
UNITLESS: ConfigValueUnits
METERS: ConfigValueUnits
MPS: ConfigValueUnits
RADPS: ConfigValueUnits
RPM: ConfigValueUnits
MS2: ConfigValueUnits
RADS2: ConfigValueUnits
VOLTS: ConfigValueUnits

class AmigaTpdo1(_message.Message):
    __slots__ = ("node_id", "stamp", "control_state", "measured_speed", "measured_angular_rate", "pto_bits", "hbridge_bits", "state_of_charge")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    CONTROL_STATE_FIELD_NUMBER: _ClassVar[int]
    MEASURED_SPEED_FIELD_NUMBER: _ClassVar[int]
    MEASURED_ANGULAR_RATE_FIELD_NUMBER: _ClassVar[int]
    PTO_BITS_FIELD_NUMBER: _ClassVar[int]
    HBRIDGE_BITS_FIELD_NUMBER: _ClassVar[int]
    STATE_OF_CHARGE_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    stamp: float
    control_state: AmigaControlState
    measured_speed: float
    measured_angular_rate: float
    pto_bits: int
    hbridge_bits: int
    state_of_charge: int
    def __init__(self, node_id: _Optional[int] = ..., stamp: _Optional[float] = ..., control_state: _Optional[_Union[AmigaControlState, str]] = ..., measured_speed: _Optional[float] = ..., measured_angular_rate: _Optional[float] = ..., pto_bits: _Optional[int] = ..., hbridge_bits: _Optional[int] = ..., state_of_charge: _Optional[int] = ...) -> None: ...

class AmigaPdo2(_message.Message):
    __slots__ = ("node_id", "stamp", "motor_a_rpm", "motor_b_rpm", "motor_c_rpm", "motor_d_rpm")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    MOTOR_A_RPM_FIELD_NUMBER: _ClassVar[int]
    MOTOR_B_RPM_FIELD_NUMBER: _ClassVar[int]
    MOTOR_C_RPM_FIELD_NUMBER: _ClassVar[int]
    MOTOR_D_RPM_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    stamp: float
    motor_a_rpm: int
    motor_b_rpm: int
    motor_c_rpm: int
    motor_d_rpm: int
    def __init__(self, node_id: _Optional[int] = ..., stamp: _Optional[float] = ..., motor_a_rpm: _Optional[int] = ..., motor_b_rpm: _Optional[int] = ..., motor_c_rpm: _Optional[int] = ..., motor_d_rpm: _Optional[int] = ...) -> None: ...

class AmigaV6CanbusState(_message.Message):
    __slots__ = ("amiga_tpdo1", "motor_states", "battery_charge_level", "send_error", "recv_error")
    AMIGA_TPDO1_FIELD_NUMBER: _ClassVar[int]
    MOTOR_STATES_FIELD_NUMBER: _ClassVar[int]
    BATTERY_CHARGE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    SEND_ERROR_FIELD_NUMBER: _ClassVar[int]
    RECV_ERROR_FIELD_NUMBER: _ClassVar[int]
    amiga_tpdo1: AmigaTpdo1
    motor_states: _canbus_pb2.MotorStates
    battery_charge_level: float
    send_error: bool
    recv_error: bool
    def __init__(self, amiga_tpdo1: _Optional[_Union[AmigaTpdo1, _Mapping]] = ..., motor_states: _Optional[_Union[_canbus_pb2.MotorStates, _Mapping]] = ..., battery_charge_level: _Optional[float] = ..., send_error: bool = ..., recv_error: bool = ...) -> None: ...

class PendantState(_message.Message):
    __slots__ = ("node_id", "stamp", "x", "y", "buttons")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    stamp: float
    x: float
    y: float
    buttons: int
    def __init__(self, node_id: _Optional[int] = ..., stamp: _Optional[float] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., buttons: _Optional[int] = ...) -> None: ...

class ConfigRequestReply(_message.Message):
    __slots__ = ("node_id", "stamp", "op_id", "val_id", "unit", "success", "int_value", "double_value", "bool_value")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    OP_ID_FIELD_NUMBER: _ClassVar[int]
    VAL_ID_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    stamp: float
    op_id: ConfigOperationIds
    val_id: ConfigValueIds
    unit: ConfigValueUnits
    success: bool
    int_value: int
    double_value: float
    bool_value: bool
    def __init__(self, node_id: _Optional[int] = ..., stamp: _Optional[float] = ..., op_id: _Optional[_Union[ConfigOperationIds, str]] = ..., val_id: _Optional[_Union[ConfigValueIds, str]] = ..., unit: _Optional[_Union[ConfigValueUnits, str]] = ..., success: bool = ..., int_value: _Optional[int] = ..., double_value: _Optional[float] = ..., bool_value: bool = ...) -> None: ...
