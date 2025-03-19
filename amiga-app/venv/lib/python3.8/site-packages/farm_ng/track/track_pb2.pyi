from farm_ng.core import lie_pb2 as _lie_pb2
from farm_ng.core import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DrivingDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIRECTION_UNSPECIFIED: _ClassVar[DrivingDirection]
    DIRECTION_FORWARD: _ClassVar[DrivingDirection]
    DIRECTION_REVERSE: _ClassVar[DrivingDirection]

class WaypointOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_UNSPECIFIED: _ClassVar[WaypointOrder]
    ORDER_STANDARD: _ClassVar[WaypointOrder]
    ORDER_REVERSED: _ClassVar[WaypointOrder]

class TrackStatusEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRACK_UNSPECIFIED: _ClassVar[TrackStatusEnum]
    TRACK_EMPTY: _ClassVar[TrackStatusEnum]
    TRACK_LOADED: _ClassVar[TrackStatusEnum]
    TRACK_FOLLOWING: _ClassVar[TrackStatusEnum]
    TRACK_PAUSED: _ClassVar[TrackStatusEnum]
    TRACK_COMPLETE: _ClassVar[TrackStatusEnum]
    TRACK_FAILED: _ClassVar[TrackStatusEnum]
    TRACK_ABORTED: _ClassVar[TrackStatusEnum]
    TRACK_CANCELLED: _ClassVar[TrackStatusEnum]
DIRECTION_UNSPECIFIED: DrivingDirection
DIRECTION_FORWARD: DrivingDirection
DIRECTION_REVERSE: DrivingDirection
ORDER_UNSPECIFIED: WaypointOrder
ORDER_STANDARD: WaypointOrder
ORDER_REVERSED: WaypointOrder
TRACK_UNSPECIFIED: TrackStatusEnum
TRACK_EMPTY: TrackStatusEnum
TRACK_LOADED: TrackStatusEnum
TRACK_FOLLOWING: TrackStatusEnum
TRACK_PAUSED: TrackStatusEnum
TRACK_COMPLETE: TrackStatusEnum
TRACK_FAILED: TrackStatusEnum
TRACK_ABORTED: TrackStatusEnum
TRACK_CANCELLED: TrackStatusEnum

class Track(_message.Message):
    __slots__ = ("waypoints",)
    WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    waypoints: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    def __init__(self, waypoints: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ...) -> None: ...

class TrackFollowRequest(_message.Message):
    __slots__ = ("track", "driving_direction")
    TRACK_FIELD_NUMBER: _ClassVar[int]
    DRIVING_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    track: Track
    driving_direction: DrivingDirection
    def __init__(self, track: _Optional[_Union[Track, _Mapping]] = ..., driving_direction: _Optional[_Union[DrivingDirection, str]] = ...) -> None: ...

class TrackFollowerState(_message.Message):
    __slots__ = ("status", "progress", "poses", "commands")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    POSES_FIELD_NUMBER: _ClassVar[int]
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    status: TrackFollowerStatus
    progress: TrackFollowerProgress
    poses: TrackFollowerPoseTree
    commands: _lie_pb2.Isometry3F64Tangent
    def __init__(self, status: _Optional[_Union[TrackFollowerStatus, _Mapping]] = ..., progress: _Optional[_Union[TrackFollowerProgress, _Mapping]] = ..., poses: _Optional[_Union[TrackFollowerPoseTree, _Mapping]] = ..., commands: _Optional[_Union[_lie_pb2.Isometry3F64Tangent, _Mapping]] = ...) -> None: ...

class TrackFollowerStatus(_message.Message):
    __slots__ = ("track_status", "robot_status", "driving_direction", "waypoint_order")
    TRACK_STATUS_FIELD_NUMBER: _ClassVar[int]
    ROBOT_STATUS_FIELD_NUMBER: _ClassVar[int]
    DRIVING_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    WAYPOINT_ORDER_FIELD_NUMBER: _ClassVar[int]
    track_status: TrackStatusEnum
    robot_status: RobotStatus
    driving_direction: DrivingDirection
    waypoint_order: WaypointOrder
    def __init__(self, track_status: _Optional[_Union[TrackStatusEnum, str]] = ..., robot_status: _Optional[_Union[RobotStatus, _Mapping]] = ..., driving_direction: _Optional[_Union[DrivingDirection, str]] = ..., waypoint_order: _Optional[_Union[WaypointOrder, str]] = ...) -> None: ...

class RobotStatus(_message.Message):
    __slots__ = ("controllable", "failure_modes")
    class FailureMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FAILURE_UNSPECIFIED: _ClassVar[RobotStatus.FailureMode]
        CANBUS_TIMEOUT: _ClassVar[RobotStatus.FailureMode]
        AUTO_MODE_DISABLED: _ClassVar[RobotStatus.FailureMode]
        CANBUS_SEND_ERROR: _ClassVar[RobotStatus.FailureMode]
        FILTER_TIMEOUT: _ClassVar[RobotStatus.FailureMode]
        FILTER_DIVERGED: _ClassVar[RobotStatus.FailureMode]
    FAILURE_UNSPECIFIED: RobotStatus.FailureMode
    CANBUS_TIMEOUT: RobotStatus.FailureMode
    AUTO_MODE_DISABLED: RobotStatus.FailureMode
    CANBUS_SEND_ERROR: RobotStatus.FailureMode
    FILTER_TIMEOUT: RobotStatus.FailureMode
    FILTER_DIVERGED: RobotStatus.FailureMode
    CONTROLLABLE_FIELD_NUMBER: _ClassVar[int]
    FAILURE_MODES_FIELD_NUMBER: _ClassVar[int]
    controllable: bool
    failure_modes: _containers.RepeatedScalarFieldContainer[RobotStatus.FailureMode]
    def __init__(self, controllable: bool = ..., failure_modes: _Optional[_Iterable[_Union[RobotStatus.FailureMode, str]]] = ...) -> None: ...

class TrackFollowerProgress(_message.Message):
    __slots__ = ("track_size", "goal_waypoint_index", "closest_waypoint_index", "distance_total", "distance_remaining", "duration_total", "duration_remaining")
    TRACK_SIZE_FIELD_NUMBER: _ClassVar[int]
    GOAL_WAYPOINT_INDEX_FIELD_NUMBER: _ClassVar[int]
    CLOSEST_WAYPOINT_INDEX_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_TOTAL_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_REMAINING_FIELD_NUMBER: _ClassVar[int]
    DURATION_TOTAL_FIELD_NUMBER: _ClassVar[int]
    DURATION_REMAINING_FIELD_NUMBER: _ClassVar[int]
    track_size: int
    goal_waypoint_index: int
    closest_waypoint_index: int
    distance_total: float
    distance_remaining: float
    duration_total: float
    duration_remaining: float
    def __init__(self, track_size: _Optional[int] = ..., goal_waypoint_index: _Optional[int] = ..., closest_waypoint_index: _Optional[int] = ..., distance_total: _Optional[float] = ..., distance_remaining: _Optional[float] = ..., duration_total: _Optional[float] = ..., duration_remaining: _Optional[float] = ...) -> None: ...

class TrackFollowerPoseTree(_message.Message):
    __slots__ = ("world_from_robot", "robot_from_goal", "robot_from_closest_waypoint")
    WORLD_FROM_ROBOT_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FROM_GOAL_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FROM_CLOSEST_WAYPOINT_FIELD_NUMBER: _ClassVar[int]
    world_from_robot: _pose_pb2.Pose
    robot_from_goal: _pose_pb2.Pose
    robot_from_closest_waypoint: _pose_pb2.Pose
    def __init__(self, world_from_robot: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., robot_from_goal: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., robot_from_closest_waypoint: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...
