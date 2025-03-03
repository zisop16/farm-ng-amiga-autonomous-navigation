from farm_ng.core import linalg_pb2 as _linalg_pb2
from farm_ng.core import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DivergenceCriteria(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_DIVERGENCE_STATE: _ClassVar[DivergenceCriteria]
    GPS_ERROR_X_HIGH: _ClassVar[DivergenceCriteria]
    GPS_ERROR_Y_HIGH: _ClassVar[DivergenceCriteria]
    STD_DEV_X_HIGH: _ClassVar[DivergenceCriteria]
    STD_DEV_Y_HIGH: _ClassVar[DivergenceCriteria]
    STD_DEV_W_HIGH: _ClassVar[DivergenceCriteria]
    NO_GYRO_MEASUREMENTS: _ClassVar[DivergenceCriteria]
    GYRO_MEASUREMENTS_DELAYED: _ClassVar[DivergenceCriteria]
    INVALID_GPS_MESSAGE: _ClassVar[DivergenceCriteria]
    NO_GPS_MEASUREMENTS: _ClassVar[DivergenceCriteria]
    GPS_MEASUREMENTS_DELAYED: _ClassVar[DivergenceCriteria]
    NO_WHEEL_ODOMETRY_MEASUREMENTS: _ClassVar[DivergenceCriteria]
    WHEEL_ODOMETRY_MEASUREMENTS_DELAYED: _ClassVar[DivergenceCriteria]
    OTHER_DIVERGENCE_REASON: _ClassVar[DivergenceCriteria]
UNKNOWN_DIVERGENCE_STATE: DivergenceCriteria
GPS_ERROR_X_HIGH: DivergenceCriteria
GPS_ERROR_Y_HIGH: DivergenceCriteria
STD_DEV_X_HIGH: DivergenceCriteria
STD_DEV_Y_HIGH: DivergenceCriteria
STD_DEV_W_HIGH: DivergenceCriteria
NO_GYRO_MEASUREMENTS: DivergenceCriteria
GYRO_MEASUREMENTS_DELAYED: DivergenceCriteria
INVALID_GPS_MESSAGE: DivergenceCriteria
NO_GPS_MEASUREMENTS: DivergenceCriteria
GPS_MEASUREMENTS_DELAYED: DivergenceCriteria
NO_WHEEL_ODOMETRY_MEASUREMENTS: DivergenceCriteria
WHEEL_ODOMETRY_MEASUREMENTS_DELAYED: DivergenceCriteria
OTHER_DIVERGENCE_REASON: DivergenceCriteria

class FilterState(_message.Message):
    __slots__ = ("pose", "has_converged", "is_calibrated", "uncertainty_diagonal", "innovation", "heading", "divergence_criteria")
    POSE_FIELD_NUMBER: _ClassVar[int]
    HAS_CONVERGED_FIELD_NUMBER: _ClassVar[int]
    IS_CALIBRATED_FIELD_NUMBER: _ClassVar[int]
    UNCERTAINTY_DIAGONAL_FIELD_NUMBER: _ClassVar[int]
    INNOVATION_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    DIVERGENCE_CRITERIA_FIELD_NUMBER: _ClassVar[int]
    pose: _pose_pb2.Pose
    has_converged: bool
    is_calibrated: bool
    uncertainty_diagonal: _linalg_pb2.VecXF64
    innovation: _linalg_pb2.VecXF64
    heading: float
    divergence_criteria: _containers.RepeatedScalarFieldContainer[DivergenceCriteria]
    def __init__(self, pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., has_converged: bool = ..., is_calibrated: bool = ..., uncertainty_diagonal: _Optional[_Union[_linalg_pb2.VecXF64, _Mapping]] = ..., innovation: _Optional[_Union[_linalg_pb2.VecXF64, _Mapping]] = ..., heading: _Optional[float] = ..., divergence_criteria: _Optional[_Iterable[_Union[DivergenceCriteria, str]]] = ...) -> None: ...

class FilterTrack(_message.Message):
    __slots__ = ("states", "name")
    STATES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    states: _containers.RepeatedCompositeFieldContainer[FilterState]
    name: str
    def __init__(self, states: _Optional[_Iterable[_Union[FilterState, _Mapping]]] = ..., name: _Optional[str] = ...) -> None: ...
