from farm_ng.core import uri_pb2 as _uri_pb2
from farm_ng.core import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Event(_message.Message):
    __slots__ = ("uri", "timestamps", "payload_length", "sequence")
    URI_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    uri: _uri_pb2.Uri
    timestamps: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    payload_length: int
    sequence: int
    def __init__(self, uri: _Optional[_Union[_uri_pb2.Uri, _Mapping]] = ..., timestamps: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ..., payload_length: _Optional[int] = ..., sequence: _Optional[int] = ...) -> None: ...
