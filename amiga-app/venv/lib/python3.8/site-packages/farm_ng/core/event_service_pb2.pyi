from farm_ng.core import uri_pb2 as _uri_pb2
from farm_ng.core import event_pb2 as _event_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubscribeRequest(_message.Message):
    __slots__ = ("uri", "every_n")
    URI_FIELD_NUMBER: _ClassVar[int]
    EVERY_N_FIELD_NUMBER: _ClassVar[int]
    uri: _uri_pb2.Uri
    every_n: int
    def __init__(self, uri: _Optional[_Union[_uri_pb2.Uri, _Mapping]] = ..., every_n: _Optional[int] = ...) -> None: ...

class SubscribeReply(_message.Message):
    __slots__ = ("event", "payload")
    EVENT_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    event: _event_pb2.Event
    payload: bytes
    def __init__(self, event: _Optional[_Union[_event_pb2.Event, _Mapping]] = ..., payload: _Optional[bytes] = ...) -> None: ...

class RequestReplyRequest(_message.Message):
    __slots__ = ("event", "payload")
    EVENT_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    event: _event_pb2.Event
    payload: bytes
    def __init__(self, event: _Optional[_Union[_event_pb2.Event, _Mapping]] = ..., payload: _Optional[bytes] = ...) -> None: ...

class RequestReplyReply(_message.Message):
    __slots__ = ("event", "payload")
    EVENT_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    event: _event_pb2.Event
    payload: bytes
    def __init__(self, event: _Optional[_Union[_event_pb2.Event, _Mapping]] = ..., payload: _Optional[bytes] = ...) -> None: ...

class RequestReply(_message.Message):
    __slots__ = ("request", "reply")
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    REPLY_FIELD_NUMBER: _ClassVar[int]
    request: RequestReplyRequest
    reply: RequestReplyReply
    def __init__(self, request: _Optional[_Union[RequestReplyRequest, _Mapping]] = ..., reply: _Optional[_Union[RequestReplyReply, _Mapping]] = ...) -> None: ...

class ListUrisRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListUrisReply(_message.Message):
    __slots__ = ("uris",)
    URIS_FIELD_NUMBER: _ClassVar[int]
    uris: _containers.RepeatedCompositeFieldContainer[_uri_pb2.Uri]
    def __init__(self, uris: _Optional[_Iterable[_Union[_uri_pb2.Uri, _Mapping]]] = ...) -> None: ...

class EventServiceConfig(_message.Message):
    __slots__ = ("name", "port", "host", "subscriptions", "uris", "args", "log_level")
    class LogLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NOTSET: _ClassVar[EventServiceConfig.LogLevel]
        CRITICAL: _ClassVar[EventServiceConfig.LogLevel]
        FATAL: _ClassVar[EventServiceConfig.LogLevel]
        ERROR: _ClassVar[EventServiceConfig.LogLevel]
        WARNING: _ClassVar[EventServiceConfig.LogLevel]
        WARN: _ClassVar[EventServiceConfig.LogLevel]
        INFO: _ClassVar[EventServiceConfig.LogLevel]
        DEBUG: _ClassVar[EventServiceConfig.LogLevel]
    NOTSET: EventServiceConfig.LogLevel
    CRITICAL: EventServiceConfig.LogLevel
    FATAL: EventServiceConfig.LogLevel
    ERROR: EventServiceConfig.LogLevel
    WARNING: EventServiceConfig.LogLevel
    WARN: EventServiceConfig.LogLevel
    INFO: EventServiceConfig.LogLevel
    DEBUG: EventServiceConfig.LogLevel
    NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    URIS_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    name: str
    port: int
    host: str
    subscriptions: _containers.RepeatedCompositeFieldContainer[SubscribeRequest]
    uris: _containers.RepeatedCompositeFieldContainer[_uri_pb2.Uri]
    args: _containers.RepeatedScalarFieldContainer[str]
    log_level: EventServiceConfig.LogLevel
    def __init__(self, name: _Optional[str] = ..., port: _Optional[int] = ..., host: _Optional[str] = ..., subscriptions: _Optional[_Iterable[_Union[SubscribeRequest, _Mapping]]] = ..., uris: _Optional[_Iterable[_Union[_uri_pb2.Uri, _Mapping]]] = ..., args: _Optional[_Iterable[str]] = ..., log_level: _Optional[_Union[EventServiceConfig.LogLevel, str]] = ...) -> None: ...

class EventServiceConfigList(_message.Message):
    __slots__ = ("configs",)
    CONFIGS_FIELD_NUMBER: _ClassVar[int]
    configs: _containers.RepeatedCompositeFieldContainer[EventServiceConfig]
    def __init__(self, configs: _Optional[_Iterable[_Union[EventServiceConfig, _Mapping]]] = ...) -> None: ...
