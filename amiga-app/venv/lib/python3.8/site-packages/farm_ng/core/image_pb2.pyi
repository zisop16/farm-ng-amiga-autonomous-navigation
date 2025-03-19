from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageSize(_message.Message):
    __slots__ = ("width", "height")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class ImageLayout(_message.Message):
    __slots__ = ("size", "pitch_bytes")
    SIZE_FIELD_NUMBER: _ClassVar[int]
    PITCH_BYTES_FIELD_NUMBER: _ClassVar[int]
    size: ImageSize
    pitch_bytes: int
    def __init__(self, size: _Optional[_Union[ImageSize, _Mapping]] = ..., pitch_bytes: _Optional[int] = ...) -> None: ...

class PixelFormat(_message.Message):
    __slots__ = ("number_type", "num_components", "num_bytes_per_component")
    NUMBER_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUM_COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    NUM_BYTES_PER_COMPONENT_FIELD_NUMBER: _ClassVar[int]
    number_type: str
    num_components: int
    num_bytes_per_component: int
    def __init__(self, number_type: _Optional[str] = ..., num_components: _Optional[int] = ..., num_bytes_per_component: _Optional[int] = ...) -> None: ...

class DynImage(_message.Message):
    __slots__ = ("layout", "pixel_format", "data")
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    PIXEL_FORMAT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    layout: ImageLayout
    pixel_format: PixelFormat
    data: bytes
    def __init__(self, layout: _Optional[_Union[ImageLayout, _Mapping]] = ..., pixel_format: _Optional[_Union[PixelFormat, _Mapping]] = ..., data: _Optional[bytes] = ...) -> None: ...
