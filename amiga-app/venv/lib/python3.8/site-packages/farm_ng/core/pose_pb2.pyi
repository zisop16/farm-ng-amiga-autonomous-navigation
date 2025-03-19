from farm_ng.core import lie_pb2 as _lie_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Pose(_message.Message):
    __slots__ = ("a_from_b", "frame_a", "frame_b", "tangent_of_b_in_a")
    A_FROM_B_FIELD_NUMBER: _ClassVar[int]
    FRAME_A_FIELD_NUMBER: _ClassVar[int]
    FRAME_B_FIELD_NUMBER: _ClassVar[int]
    TANGENT_OF_B_IN_A_FIELD_NUMBER: _ClassVar[int]
    a_from_b: _lie_pb2.Isometry3F64
    frame_a: str
    frame_b: str
    tangent_of_b_in_a: _lie_pb2.Isometry3F64Tangent
    def __init__(self, a_from_b: _Optional[_Union[_lie_pb2.Isometry3F64, _Mapping]] = ..., frame_a: _Optional[str] = ..., frame_b: _Optional[str] = ..., tangent_of_b_in_a: _Optional[_Union[_lie_pb2.Isometry3F64Tangent, _Mapping]] = ...) -> None: ...

class PoseTree(_message.Message):
    __slots__ = ("poses",)
    POSES_FIELD_NUMBER: _ClassVar[int]
    poses: _containers.RepeatedCompositeFieldContainer[Pose]
    def __init__(self, poses: _Optional[_Iterable[_Union[Pose, _Mapping]]] = ...) -> None: ...
