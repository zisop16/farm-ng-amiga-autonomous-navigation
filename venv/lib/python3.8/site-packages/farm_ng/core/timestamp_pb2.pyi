from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Timestamp(_message.Message):
    __slots__ = ("stamp", "clock_name", "semantics")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    CLOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    SEMANTICS_FIELD_NUMBER: _ClassVar[int]
    stamp: float
    clock_name: str
    semantics: str
    def __init__(self, stamp: _Optional[float] = ..., clock_name: _Optional[str] = ..., semantics: _Optional[str] = ...) -> None: ...
