from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Vec2I64(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class Vec2F32(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class Vec2F64(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class Vec3I64(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    z: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., z: _Optional[int] = ...) -> None: ...

class Vec3F32(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class Vec3F64(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class Mat2F32(_message.Message):
    __slots__ = ("col_0", "col_1")
    COL_0_FIELD_NUMBER: _ClassVar[int]
    COL_1_FIELD_NUMBER: _ClassVar[int]
    col_0: Vec2F32
    col_1: Vec2F32
    def __init__(self, col_0: _Optional[_Union[Vec2F32, _Mapping]] = ..., col_1: _Optional[_Union[Vec2F32, _Mapping]] = ...) -> None: ...

class Mat2F64(_message.Message):
    __slots__ = ("col_0", "col_1")
    COL_0_FIELD_NUMBER: _ClassVar[int]
    COL_1_FIELD_NUMBER: _ClassVar[int]
    col_0: Vec2F64
    col_1: Vec2F64
    def __init__(self, col_0: _Optional[_Union[Vec2F64, _Mapping]] = ..., col_1: _Optional[_Union[Vec2F64, _Mapping]] = ...) -> None: ...

class Mat3F32(_message.Message):
    __slots__ = ("col_0", "col_1", "col_2")
    COL_0_FIELD_NUMBER: _ClassVar[int]
    COL_1_FIELD_NUMBER: _ClassVar[int]
    COL_2_FIELD_NUMBER: _ClassVar[int]
    col_0: Vec3F32
    col_1: Vec3F32
    col_2: Vec3F32
    def __init__(self, col_0: _Optional[_Union[Vec3F32, _Mapping]] = ..., col_1: _Optional[_Union[Vec3F32, _Mapping]] = ..., col_2: _Optional[_Union[Vec3F32, _Mapping]] = ...) -> None: ...

class Mat3F64(_message.Message):
    __slots__ = ("col_0", "col_1", "col_2")
    COL_0_FIELD_NUMBER: _ClassVar[int]
    COL_1_FIELD_NUMBER: _ClassVar[int]
    COL_2_FIELD_NUMBER: _ClassVar[int]
    col_0: Vec3F64
    col_1: Vec3F64
    col_2: Vec3F64
    def __init__(self, col_0: _Optional[_Union[Vec3F64, _Mapping]] = ..., col_1: _Optional[_Union[Vec3F64, _Mapping]] = ..., col_2: _Optional[_Union[Vec3F64, _Mapping]] = ...) -> None: ...

class VecXF32(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, data: _Optional[_Iterable[float]] = ...) -> None: ...

class VecXF64(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, data: _Optional[_Iterable[float]] = ...) -> None: ...

class MatXF32(_message.Message):
    __slots__ = ("rows", "cols", "data")
    ROWS_FIELD_NUMBER: _ClassVar[int]
    COLS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    rows: int
    cols: int
    data: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, rows: _Optional[int] = ..., cols: _Optional[int] = ..., data: _Optional[_Iterable[float]] = ...) -> None: ...

class MatXF64(_message.Message):
    __slots__ = ("rows", "cols", "data")
    ROWS_FIELD_NUMBER: _ClassVar[int]
    COLS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    rows: int
    cols: int
    data: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, rows: _Optional[int] = ..., cols: _Optional[int] = ..., data: _Optional[_Iterable[float]] = ...) -> None: ...
