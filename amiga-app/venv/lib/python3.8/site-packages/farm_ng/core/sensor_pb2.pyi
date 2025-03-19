from farm_ng.core import image_pb2 as _image_pb2
from farm_ng.core import lie_pb2 as _lie_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraModel(_message.Message):
    __slots__ = ("image_size", "distortion_type", "params")
    IMAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    DISTORTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    image_size: _image_pb2.ImageSize
    distortion_type: str
    params: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, image_size: _Optional[_Union[_image_pb2.ImageSize, _Mapping]] = ..., distortion_type: _Optional[str] = ..., params: _Optional[_Iterable[float]] = ...) -> None: ...

class CameraModels(_message.Message):
    __slots__ = ("camera_models",)
    CAMERA_MODELS_FIELD_NUMBER: _ClassVar[int]
    camera_models: _containers.RepeatedCompositeFieldContainer[CameraModel]
    def __init__(self, camera_models: _Optional[_Iterable[_Union[CameraModel, _Mapping]]] = ...) -> None: ...

class ClippingPlanes(_message.Message):
    __slots__ = ("near", "far")
    NEAR_FIELD_NUMBER: _ClassVar[int]
    FAR_FIELD_NUMBER: _ClassVar[int]
    near: float
    far: float
    def __init__(self, near: _Optional[float] = ..., far: _Optional[float] = ...) -> None: ...

class RigidCamera(_message.Message):
    __slots__ = ("intrinsics", "rig_from_camera")
    INTRINSICS_FIELD_NUMBER: _ClassVar[int]
    RIG_FROM_CAMERA_FIELD_NUMBER: _ClassVar[int]
    intrinsics: CameraModel
    rig_from_camera: _lie_pb2.Isometry3F64
    def __init__(self, intrinsics: _Optional[_Union[CameraModel, _Mapping]] = ..., rig_from_camera: _Optional[_Union[_lie_pb2.Isometry3F64, _Mapping]] = ...) -> None: ...

class GyroModel(_message.Message):
    __slots__ = ("model_type", "params")
    MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    model_type: str
    params: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, model_type: _Optional[str] = ..., params: _Optional[_Iterable[float]] = ...) -> None: ...

class AcceleroModel(_message.Message):
    __slots__ = ("model_type", "params")
    MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    model_type: str
    params: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, model_type: _Optional[str] = ..., params: _Optional[_Iterable[float]] = ...) -> None: ...

class ImuModel(_message.Message):
    __slots__ = ("gyro_model", "accelero_model")
    GYRO_MODEL_FIELD_NUMBER: _ClassVar[int]
    ACCELERO_MODEL_FIELD_NUMBER: _ClassVar[int]
    gyro_model: GyroModel
    accelero_model: AcceleroModel
    def __init__(self, gyro_model: _Optional[_Union[GyroModel, _Mapping]] = ..., accelero_model: _Optional[_Union[AcceleroModel, _Mapping]] = ...) -> None: ...
