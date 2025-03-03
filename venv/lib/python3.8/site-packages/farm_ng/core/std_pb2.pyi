from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OptionalG0Float(_message.Message):
    __slots__ = ("value", "has_value")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    HAS_VALUE_FIELD_NUMBER: _ClassVar[int]
    value: float
    has_value: bool
    def __init__(self, value: _Optional[float] = ..., has_value: bool = ...) -> None: ...

class OptionalG0Double(_message.Message):
    __slots__ = ("value", "has_value")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    HAS_VALUE_FIELD_NUMBER: _ClassVar[int]
    value: float
    has_value: bool
    def __init__(self, value: _Optional[float] = ..., has_value: bool = ...) -> None: ...

class OptionalG0Int32(_message.Message):
    __slots__ = ("value", "has_value")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    HAS_VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    has_value: bool
    def __init__(self, value: _Optional[int] = ..., has_value: bool = ...) -> None: ...

class OptionalG0Int64(_message.Message):
    __slots__ = ("value", "has_value")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    HAS_VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    has_value: bool
    def __init__(self, value: _Optional[int] = ..., has_value: bool = ...) -> None: ...

class OptionalG0Bool(_message.Message):
    __slots__ = ("value", "has_value")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    HAS_VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bool
    has_value: bool
    def __init__(self, value: bool = ..., has_value: bool = ...) -> None: ...

class OptionalG0String(_message.Message):
    __slots__ = ("value", "has_value")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    HAS_VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    has_value: bool
    def __init__(self, value: _Optional[str] = ..., has_value: bool = ...) -> None: ...

class FileSystemPath(_message.Message):
    __slots__ = ("path_string",)
    PATH_STRING_FIELD_NUMBER: _ClassVar[int]
    path_string: str
    def __init__(self, path_string: _Optional[str] = ...) -> None: ...
