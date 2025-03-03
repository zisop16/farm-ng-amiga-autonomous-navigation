from farm_ng.core import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GpsFrameStatus(_message.Message):
    __slots__ = ("time_fully_resolved", "gnss_fix_ok", "diff_soln", "heading_vehicle_valid")
    TIME_FULLY_RESOLVED_FIELD_NUMBER: _ClassVar[int]
    GNSS_FIX_OK_FIELD_NUMBER: _ClassVar[int]
    DIFF_SOLN_FIELD_NUMBER: _ClassVar[int]
    HEADING_VEHICLE_VALID_FIELD_NUMBER: _ClassVar[int]
    time_fully_resolved: bool
    gnss_fix_ok: bool
    diff_soln: bool
    heading_vehicle_valid: bool
    def __init__(self, time_fully_resolved: bool = ..., gnss_fix_ok: bool = ..., diff_soln: bool = ..., heading_vehicle_valid: bool = ...) -> None: ...

class UtcStamp(_message.Message):
    __slots__ = ("iTOW", "year", "month", "day", "hour", "min", "sec", "nano", "tAcc", "valid_date", "valid_time", "fully_resolved")
    ITOW_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    SEC_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    TACC_FIELD_NUMBER: _ClassVar[int]
    VALID_DATE_FIELD_NUMBER: _ClassVar[int]
    VALID_TIME_FIELD_NUMBER: _ClassVar[int]
    FULLY_RESOLVED_FIELD_NUMBER: _ClassVar[int]
    iTOW: int
    year: int
    month: int
    day: int
    hour: int
    min: int
    sec: int
    nano: int
    tAcc: int
    valid_date: bool
    valid_time: bool
    fully_resolved: bool
    def __init__(self, iTOW: _Optional[int] = ..., year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ..., hour: _Optional[int] = ..., min: _Optional[int] = ..., sec: _Optional[int] = ..., nano: _Optional[int] = ..., tAcc: _Optional[int] = ..., valid_date: bool = ..., valid_time: bool = ..., fully_resolved: bool = ...) -> None: ...

class GpsFrame(_message.Message):
    __slots__ = ("stamp", "gps_time", "longitude", "latitude", "altitude", "heading_vehicle", "heading_motion", "heading_accuracy", "ground_speed", "speed_accuracy", "vel_north", "vel_east", "vel_down", "horizontal_accuracy", "vertical_accuracy", "position_mode", "p_dop", "height", "status", "utc_stamp", "num_satellites")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    GPS_TIME_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    HEADING_VEHICLE_FIELD_NUMBER: _ClassVar[int]
    HEADING_MOTION_FIELD_NUMBER: _ClassVar[int]
    HEADING_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    GROUND_SPEED_FIELD_NUMBER: _ClassVar[int]
    SPEED_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    VEL_NORTH_FIELD_NUMBER: _ClassVar[int]
    VEL_EAST_FIELD_NUMBER: _ClassVar[int]
    VEL_DOWN_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    POSITION_MODE_FIELD_NUMBER: _ClassVar[int]
    P_DOP_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UTC_STAMP_FIELD_NUMBER: _ClassVar[int]
    NUM_SATELLITES_FIELD_NUMBER: _ClassVar[int]
    stamp: _timestamp_pb2.Timestamp
    gps_time: _timestamp_pb2.Timestamp
    longitude: float
    latitude: float
    altitude: float
    heading_vehicle: float
    heading_motion: float
    heading_accuracy: float
    ground_speed: float
    speed_accuracy: float
    vel_north: float
    vel_east: float
    vel_down: float
    horizontal_accuracy: float
    vertical_accuracy: float
    position_mode: int
    p_dop: float
    height: float
    status: GpsFrameStatus
    utc_stamp: UtcStamp
    num_satellites: int
    def __init__(self, stamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., gps_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., longitude: _Optional[float] = ..., latitude: _Optional[float] = ..., altitude: _Optional[float] = ..., heading_vehicle: _Optional[float] = ..., heading_motion: _Optional[float] = ..., heading_accuracy: _Optional[float] = ..., ground_speed: _Optional[float] = ..., speed_accuracy: _Optional[float] = ..., vel_north: _Optional[float] = ..., vel_east: _Optional[float] = ..., vel_down: _Optional[float] = ..., horizontal_accuracy: _Optional[float] = ..., vertical_accuracy: _Optional[float] = ..., position_mode: _Optional[int] = ..., p_dop: _Optional[float] = ..., height: _Optional[float] = ..., status: _Optional[_Union[GpsFrameStatus, _Mapping]] = ..., utc_stamp: _Optional[_Union[UtcStamp, _Mapping]] = ..., num_satellites: _Optional[int] = ...) -> None: ...

class RelativePositionFrame(_message.Message):
    __slots__ = ("stamp", "gps_time", "base_station_id", "relative_pose_north", "relative_pose_east", "relative_pose_down", "relative_pose_heading", "relative_pose_length", "rel_pos_valid", "rel_heading_valid", "accuracy_north", "accuracy_east", "accuracy_down", "accuracy_length", "accuracy_heading", "carr_soln", "is_moving", "ref_obs_miss", "ref_pos_miss", "ref_pos_normalized", "gnss_fix_ok", "base_coords_known", "base_coords")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    GPS_TIME_FIELD_NUMBER: _ClassVar[int]
    BASE_STATION_ID_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_POSE_NORTH_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_POSE_EAST_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_POSE_DOWN_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_POSE_HEADING_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_POSE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    REL_POS_VALID_FIELD_NUMBER: _ClassVar[int]
    REL_HEADING_VALID_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_NORTH_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_EAST_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_DOWN_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_LENGTH_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_HEADING_FIELD_NUMBER: _ClassVar[int]
    CARR_SOLN_FIELD_NUMBER: _ClassVar[int]
    IS_MOVING_FIELD_NUMBER: _ClassVar[int]
    REF_OBS_MISS_FIELD_NUMBER: _ClassVar[int]
    REF_POS_MISS_FIELD_NUMBER: _ClassVar[int]
    REF_POS_NORMALIZED_FIELD_NUMBER: _ClassVar[int]
    GNSS_FIX_OK_FIELD_NUMBER: _ClassVar[int]
    BASE_COORDS_KNOWN_FIELD_NUMBER: _ClassVar[int]
    BASE_COORDS_FIELD_NUMBER: _ClassVar[int]
    stamp: _timestamp_pb2.Timestamp
    gps_time: _timestamp_pb2.Timestamp
    base_station_id: int
    relative_pose_north: float
    relative_pose_east: float
    relative_pose_down: float
    relative_pose_heading: float
    relative_pose_length: float
    rel_pos_valid: bool
    rel_heading_valid: bool
    accuracy_north: float
    accuracy_east: float
    accuracy_down: float
    accuracy_length: float
    accuracy_heading: float
    carr_soln: int
    is_moving: bool
    ref_obs_miss: bool
    ref_pos_miss: bool
    ref_pos_normalized: bool
    gnss_fix_ok: bool
    base_coords_known: bool
    base_coords: GpsCoordinates
    def __init__(self, stamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., gps_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., base_station_id: _Optional[int] = ..., relative_pose_north: _Optional[float] = ..., relative_pose_east: _Optional[float] = ..., relative_pose_down: _Optional[float] = ..., relative_pose_heading: _Optional[float] = ..., relative_pose_length: _Optional[float] = ..., rel_pos_valid: bool = ..., rel_heading_valid: bool = ..., accuracy_north: _Optional[float] = ..., accuracy_east: _Optional[float] = ..., accuracy_down: _Optional[float] = ..., accuracy_length: _Optional[float] = ..., accuracy_heading: _Optional[float] = ..., carr_soln: _Optional[int] = ..., is_moving: bool = ..., ref_obs_miss: bool = ..., ref_pos_miss: bool = ..., ref_pos_normalized: bool = ..., gnss_fix_ok: bool = ..., base_coords_known: bool = ..., base_coords: _Optional[_Union[GpsCoordinates, _Mapping]] = ...) -> None: ...

class GpsCoordinates(_message.Message):
    __slots__ = ("longitude", "latitude", "altitude")
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    longitude: float
    latitude: float
    altitude: float
    def __init__(self, longitude: _Optional[float] = ..., latitude: _Optional[float] = ..., altitude: _Optional[float] = ...) -> None: ...

class EcefCoordinates(_message.Message):
    __slots__ = ("stamp", "gps_time", "x", "y", "z", "accuracy", "flags")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    GPS_TIME_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    stamp: _timestamp_pb2.Timestamp
    gps_time: _timestamp_pb2.Timestamp
    x: float
    y: float
    z: float
    accuracy: float
    flags: EcefFlags
    def __init__(self, stamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., gps_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., accuracy: _Optional[float] = ..., flags: _Optional[_Union[EcefFlags, _Mapping]] = ...) -> None: ...

class EcefFlags(_message.Message):
    __slots__ = ("INVALID_ECEF",)
    INVALID_ECEF_FIELD_NUMBER: _ClassVar[int]
    INVALID_ECEF: bool
    def __init__(self, INVALID_ECEF: bool = ...) -> None: ...
