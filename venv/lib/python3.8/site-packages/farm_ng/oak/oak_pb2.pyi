from farm_ng.core import linalg_pb2 as _linalg_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EncoderProfile(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    H264_BASELINE: _ClassVar[EncoderProfile]
    H264_HIGH: _ClassVar[EncoderProfile]
    H264_MAIN: _ClassVar[EncoderProfile]
    H265_MAIN: _ClassVar[EncoderProfile]
    MJPEG: _ClassVar[EncoderProfile]

class RateControlMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CBR: _ClassVar[RateControlMode]
    VBR: _ClassVar[RateControlMode]

class PixelFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[PixelFormat]
    YUV420: _ClassVar[PixelFormat]
    RAW8: _ClassVar[PixelFormat]
    Encoded: _ClassVar[PixelFormat]
H264_BASELINE: EncoderProfile
H264_HIGH: EncoderProfile
H264_MAIN: EncoderProfile
H265_MAIN: EncoderProfile
MJPEG: EncoderProfile
CBR: RateControlMode
VBR: RateControlMode
UNKNOWN: PixelFormat
YUV420: PixelFormat
RAW8: PixelFormat
Encoded: PixelFormat

class CameraSettings(_message.Message):
    __slots__ = ("auto_exposure", "exposure_time", "iso_value", "lens_pos")
    AUTO_EXPOSURE_FIELD_NUMBER: _ClassVar[int]
    EXPOSURE_TIME_FIELD_NUMBER: _ClassVar[int]
    ISO_VALUE_FIELD_NUMBER: _ClassVar[int]
    LENS_POS_FIELD_NUMBER: _ClassVar[int]
    auto_exposure: bool
    exposure_time: int
    iso_value: int
    lens_pos: int
    def __init__(self, auto_exposure: bool = ..., exposure_time: _Optional[int] = ..., iso_value: _Optional[int] = ..., lens_pos: _Optional[int] = ...) -> None: ...

class EncoderOptions(_message.Message):
    __slots__ = ("profile", "rate_control_mode", "cbr_preferred_bitrate_kbps", "vbr_or_mjpeg_quality", "frames_per_keyframe")
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    RATE_CONTROL_MODE_FIELD_NUMBER: _ClassVar[int]
    CBR_PREFERRED_BITRATE_KBPS_FIELD_NUMBER: _ClassVar[int]
    VBR_OR_MJPEG_QUALITY_FIELD_NUMBER: _ClassVar[int]
    FRAMES_PER_KEYFRAME_FIELD_NUMBER: _ClassVar[int]
    profile: EncoderProfile
    rate_control_mode: RateControlMode
    cbr_preferred_bitrate_kbps: int
    vbr_or_mjpeg_quality: int
    frames_per_keyframe: int
    def __init__(self, profile: _Optional[_Union[EncoderProfile, str]] = ..., rate_control_mode: _Optional[_Union[RateControlMode, str]] = ..., cbr_preferred_bitrate_kbps: _Optional[int] = ..., vbr_or_mjpeg_quality: _Optional[int] = ..., frames_per_keyframe: _Optional[int] = ...) -> None: ...

class Resolution(_message.Message):
    __slots__ = ("width", "height")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class OakImageMeta(_message.Message):
    __slots__ = ("category", "instance_num", "sequence_num", "timestamp", "timestamp_device", "timestamp_recv", "settings", "encoder_options", "resolution", "pixel_format")
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_NUM_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUM_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_DEVICE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_RECV_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ENCODER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    PIXEL_FORMAT_FIELD_NUMBER: _ClassVar[int]
    category: int
    instance_num: int
    sequence_num: int
    timestamp: float
    timestamp_device: float
    timestamp_recv: float
    settings: CameraSettings
    encoder_options: EncoderOptions
    resolution: Resolution
    pixel_format: PixelFormat
    def __init__(self, category: _Optional[int] = ..., instance_num: _Optional[int] = ..., sequence_num: _Optional[int] = ..., timestamp: _Optional[float] = ..., timestamp_device: _Optional[float] = ..., timestamp_recv: _Optional[float] = ..., settings: _Optional[_Union[CameraSettings, _Mapping]] = ..., encoder_options: _Optional[_Union[EncoderOptions, _Mapping]] = ..., resolution: _Optional[_Union[Resolution, _Mapping]] = ..., pixel_format: _Optional[_Union[PixelFormat, str]] = ...) -> None: ...

class OakFrame(_message.Message):
    __slots__ = ("meta", "image_data")
    META_FIELD_NUMBER: _ClassVar[int]
    IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    meta: OakImageMeta
    image_data: bytes
    def __init__(self, meta: _Optional[_Union[OakImageMeta, _Mapping]] = ..., image_data: _Optional[bytes] = ...) -> None: ...

class OakGyro(_message.Message):
    __slots__ = ("gyro", "sequence_num", "accuracy", "timestamp", "timestamp_device", "timestamp_recv")
    GYRO_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUM_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_DEVICE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_RECV_FIELD_NUMBER: _ClassVar[int]
    gyro: _linalg_pb2.Vec3F32
    sequence_num: int
    accuracy: str
    timestamp: float
    timestamp_device: float
    timestamp_recv: float
    def __init__(self, gyro: _Optional[_Union[_linalg_pb2.Vec3F32, _Mapping]] = ..., sequence_num: _Optional[int] = ..., accuracy: _Optional[str] = ..., timestamp: _Optional[float] = ..., timestamp_device: _Optional[float] = ..., timestamp_recv: _Optional[float] = ...) -> None: ...

class OakAccelero(_message.Message):
    __slots__ = ("accelero", "sequence_num", "accuracy", "timestamp", "timestamp_device", "timestamp_recv")
    ACCELERO_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUM_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_DEVICE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_RECV_FIELD_NUMBER: _ClassVar[int]
    accelero: _linalg_pb2.Vec3F32
    sequence_num: int
    accuracy: str
    timestamp: float
    timestamp_device: float
    timestamp_recv: float
    def __init__(self, accelero: _Optional[_Union[_linalg_pb2.Vec3F32, _Mapping]] = ..., sequence_num: _Optional[int] = ..., accuracy: _Optional[str] = ..., timestamp: _Optional[float] = ..., timestamp_device: _Optional[float] = ..., timestamp_recv: _Optional[float] = ...) -> None: ...

class OakImuPacket(_message.Message):
    __slots__ = ("gyro_packet", "accelero_packet")
    GYRO_PACKET_FIELD_NUMBER: _ClassVar[int]
    ACCELERO_PACKET_FIELD_NUMBER: _ClassVar[int]
    gyro_packet: OakGyro
    accelero_packet: OakAccelero
    def __init__(self, gyro_packet: _Optional[_Union[OakGyro, _Mapping]] = ..., accelero_packet: _Optional[_Union[OakAccelero, _Mapping]] = ...) -> None: ...

class OakImuPackets(_message.Message):
    __slots__ = ("packets",)
    PACKETS_FIELD_NUMBER: _ClassVar[int]
    packets: _containers.RepeatedCompositeFieldContainer[OakImuPacket]
    def __init__(self, packets: _Optional[_Iterable[_Union[OakImuPacket, _Mapping]]] = ...) -> None: ...

class OakTrackedFeaturePacket(_message.Message):
    __slots__ = ("xy", "id", "age", "harrisScore", "trackingError")
    XY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    HARRISSCORE_FIELD_NUMBER: _ClassVar[int]
    TRACKINGERROR_FIELD_NUMBER: _ClassVar[int]
    xy: _linalg_pb2.Vec2F32
    id: int
    age: int
    harrisScore: float
    trackingError: float
    def __init__(self, xy: _Optional[_Union[_linalg_pb2.Vec2F32, _Mapping]] = ..., id: _Optional[int] = ..., age: _Optional[int] = ..., harrisScore: _Optional[float] = ..., trackingError: _Optional[float] = ...) -> None: ...

class OakTrackedFeaturePackets(_message.Message):
    __slots__ = ("packets", "sequence_num", "timestamp", "timestamp_device", "timestamp_recv")
    PACKETS_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUM_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_DEVICE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_RECV_FIELD_NUMBER: _ClassVar[int]
    packets: _containers.RepeatedCompositeFieldContainer[OakTrackedFeaturePacket]
    sequence_num: int
    timestamp: float
    timestamp_device: float
    timestamp_recv: float
    def __init__(self, packets: _Optional[_Iterable[_Union[OakTrackedFeaturePacket, _Mapping]]] = ..., sequence_num: _Optional[int] = ..., timestamp: _Optional[float] = ..., timestamp_device: _Optional[float] = ..., timestamp_recv: _Optional[float] = ...) -> None: ...

class OakDeviceInfo(_message.Message):
    __slots__ = ("name", "mxid", "ip")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MXID_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    name: str
    mxid: str
    ip: str
    def __init__(self, name: _Optional[str] = ..., mxid: _Optional[str] = ..., ip: _Optional[str] = ...) -> None: ...

class OakSyncFrame(_message.Message):
    __slots__ = ("left", "right", "rgb", "disparity", "nn", "imu_packets", "sequence_num", "device_info")
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    RGB_FIELD_NUMBER: _ClassVar[int]
    DISPARITY_FIELD_NUMBER: _ClassVar[int]
    NN_FIELD_NUMBER: _ClassVar[int]
    IMU_PACKETS_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUM_FIELD_NUMBER: _ClassVar[int]
    DEVICE_INFO_FIELD_NUMBER: _ClassVar[int]
    left: OakFrame
    right: OakFrame
    rgb: OakFrame
    disparity: OakFrame
    nn: OakNNData
    imu_packets: OakImuPackets
    sequence_num: int
    device_info: OakDeviceInfo
    def __init__(self, left: _Optional[_Union[OakFrame, _Mapping]] = ..., right: _Optional[_Union[OakFrame, _Mapping]] = ..., rgb: _Optional[_Union[OakFrame, _Mapping]] = ..., disparity: _Optional[_Union[OakFrame, _Mapping]] = ..., nn: _Optional[_Union[OakNNData, _Mapping]] = ..., imu_packets: _Optional[_Union[OakImuPackets, _Mapping]] = ..., sequence_num: _Optional[int] = ..., device_info: _Optional[_Union[OakDeviceInfo, _Mapping]] = ...) -> None: ...

class OakNNData(_message.Message):
    __slots__ = ("meta", "num_channels", "height", "width", "data")
    META_FIELD_NUMBER: _ClassVar[int]
    NUM_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    meta: OakImageMeta
    num_channels: int
    height: int
    width: int
    data: bytes
    def __init__(self, meta: _Optional[_Union[OakImageMeta, _Mapping]] = ..., num_channels: _Optional[int] = ..., height: _Optional[int] = ..., width: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class Pair(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ("pairs",)
    PAIRS_FIELD_NUMBER: _ClassVar[int]
    pairs: _containers.RepeatedCompositeFieldContainer[Pair]
    def __init__(self, pairs: _Optional[_Iterable[_Union[Pair, _Mapping]]] = ...) -> None: ...

class OakDataSample(_message.Message):
    __slots__ = ("frame", "metadata")
    FRAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    frame: OakSyncFrame
    metadata: Metadata
    def __init__(self, frame: _Optional[_Union[OakSyncFrame, _Mapping]] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ...) -> None: ...

class RotationMatrix(_message.Message):
    __slots__ = ("rotation_matrix",)
    ROTATION_MATRIX_FIELD_NUMBER: _ClassVar[int]
    rotation_matrix: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, rotation_matrix: _Optional[_Iterable[float]] = ...) -> None: ...

class Extrinsics(_message.Message):
    __slots__ = ("rotation_matrix", "spec_translation", "to_camera_socket", "translation")
    ROTATION_MATRIX_FIELD_NUMBER: _ClassVar[int]
    SPEC_TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    TO_CAMERA_SOCKET_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    rotation_matrix: _containers.RepeatedScalarFieldContainer[float]
    spec_translation: _linalg_pb2.Vec3F32
    to_camera_socket: int
    translation: _linalg_pb2.Vec3F32
    def __init__(self, rotation_matrix: _Optional[_Iterable[float]] = ..., spec_translation: _Optional[_Union[_linalg_pb2.Vec3F32, _Mapping]] = ..., to_camera_socket: _Optional[int] = ..., translation: _Optional[_Union[_linalg_pb2.Vec3F32, _Mapping]] = ...) -> None: ...

class CameraData(_message.Message):
    __slots__ = ("camera_number", "camera_type", "distortion_coeff", "extrinsics", "height", "intrinsic_matrix", "lens_position", "spec_hfov_deg", "width")
    CAMERA_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CAMERA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISTORTION_COEFF_FIELD_NUMBER: _ClassVar[int]
    EXTRINSICS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    INTRINSIC_MATRIX_FIELD_NUMBER: _ClassVar[int]
    LENS_POSITION_FIELD_NUMBER: _ClassVar[int]
    SPEC_HFOV_DEG_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    camera_number: int
    camera_type: int
    distortion_coeff: _containers.RepeatedScalarFieldContainer[float]
    extrinsics: Extrinsics
    height: int
    intrinsic_matrix: _containers.RepeatedScalarFieldContainer[float]
    lens_position: int
    spec_hfov_deg: float
    width: int
    def __init__(self, camera_number: _Optional[int] = ..., camera_type: _Optional[int] = ..., distortion_coeff: _Optional[_Iterable[float]] = ..., extrinsics: _Optional[_Union[Extrinsics, _Mapping]] = ..., height: _Optional[int] = ..., intrinsic_matrix: _Optional[_Iterable[float]] = ..., lens_position: _Optional[int] = ..., spec_hfov_deg: _Optional[float] = ..., width: _Optional[int] = ...) -> None: ...

class StereoRectificationData(_message.Message):
    __slots__ = ("left_camera_socket", "rectified_rotation_left", "rectified_rotation_right", "right_camera_socket")
    LEFT_CAMERA_SOCKET_FIELD_NUMBER: _ClassVar[int]
    RECTIFIED_ROTATION_LEFT_FIELD_NUMBER: _ClassVar[int]
    RECTIFIED_ROTATION_RIGHT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_CAMERA_SOCKET_FIELD_NUMBER: _ClassVar[int]
    left_camera_socket: int
    rectified_rotation_left: _containers.RepeatedScalarFieldContainer[float]
    rectified_rotation_right: _containers.RepeatedScalarFieldContainer[float]
    right_camera_socket: int
    def __init__(self, left_camera_socket: _Optional[int] = ..., rectified_rotation_left: _Optional[_Iterable[float]] = ..., rectified_rotation_right: _Optional[_Iterable[float]] = ..., right_camera_socket: _Optional[int] = ...) -> None: ...

class OakCalibration(_message.Message):
    __slots__ = ("batch_name", "batch_time", "board_conf", "board_custom", "board_name", "board_options", "board_rev", "camera_data", "hardware_conf", "imu_extrinsics", "miscellaneous_data", "product_name", "stereo_rectification_data", "version")
    BATCH_NAME_FIELD_NUMBER: _ClassVar[int]
    BATCH_TIME_FIELD_NUMBER: _ClassVar[int]
    BOARD_CONF_FIELD_NUMBER: _ClassVar[int]
    BOARD_CUSTOM_FIELD_NUMBER: _ClassVar[int]
    BOARD_NAME_FIELD_NUMBER: _ClassVar[int]
    BOARD_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    BOARD_REV_FIELD_NUMBER: _ClassVar[int]
    CAMERA_DATA_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_CONF_FIELD_NUMBER: _ClassVar[int]
    IMU_EXTRINSICS_FIELD_NUMBER: _ClassVar[int]
    MISCELLANEOUS_DATA_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    STEREO_RECTIFICATION_DATA_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    batch_name: str
    batch_time: int
    board_conf: str
    board_custom: str
    board_name: str
    board_options: int
    board_rev: str
    camera_data: _containers.RepeatedCompositeFieldContainer[CameraData]
    hardware_conf: str
    imu_extrinsics: Extrinsics
    miscellaneous_data: _containers.RepeatedScalarFieldContainer[str]
    product_name: str
    stereo_rectification_data: StereoRectificationData
    version: int
    def __init__(self, batch_name: _Optional[str] = ..., batch_time: _Optional[int] = ..., board_conf: _Optional[str] = ..., board_custom: _Optional[str] = ..., board_name: _Optional[str] = ..., board_options: _Optional[int] = ..., board_rev: _Optional[str] = ..., camera_data: _Optional[_Iterable[_Union[CameraData, _Mapping]]] = ..., hardware_conf: _Optional[str] = ..., imu_extrinsics: _Optional[_Union[Extrinsics, _Mapping]] = ..., miscellaneous_data: _Optional[_Iterable[str]] = ..., product_name: _Optional[str] = ..., stereo_rectification_data: _Optional[_Union[StereoRectificationData, _Mapping]] = ..., version: _Optional[int] = ...) -> None: ...
