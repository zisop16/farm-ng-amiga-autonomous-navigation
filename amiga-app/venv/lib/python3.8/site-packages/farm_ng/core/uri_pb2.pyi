from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Uri(_message.Message):
    __slots__ = ("scheme", "authority", "path", "query")
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    scheme: str
    authority: str
    path: str
    query: str
    def __init__(self, scheme: _Optional[str] = ..., authority: _Optional[str] = ..., path: _Optional[str] = ..., query: _Optional[str] = ...) -> None: ...
