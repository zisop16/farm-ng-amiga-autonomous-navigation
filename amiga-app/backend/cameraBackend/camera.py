# Modified code from
# https://github.com/luxonis/depthai-experiments/blob/master/gen2-multiple-devices/rgbd-pointcloud-fusion/camera.py
# https://github.com/luxonis/depthai-python/blob/main/examples/ToF/tof_depth.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from multiprocessing import Process, Queue
import depthai as dai
import cv2
import numpy as np
import open3d as o3d
from .syncQueue import SyncQueue
from .streamingServer import startStreamingServer

from config import CALIBRATION_DATA_DIR


class Camera:
    """
    Manages a DepthAI camera device, captures RGB-D point clouds, and hosts
    an HTTP MJPEG stream.

    On initialization, builds and starts a DepthAI pipeline with:

      - A VideoEncoder node to produce MJPEG frames at VIDEO_FPS, forwarded to a
        background streaming server process on localhost at the given TCP port.
      - A ToF node configured to emit depth frames at TOF_FPS.
      - An RGB camera producing ISP frames at TOF_FPS for color data.
      - Queues to receive video, image, and depth frames from the camera.

    Calibration data (intrinsics, extrinsics, and alignment) are loaded from disk
    to project depth + color into a Open3D PointCloud.

    Args:
        device_info (dai.DeviceInfo):
            DepthAI object containing information about the camera.
        stream_port (int):
            TCP port on which to serve the MJPEG video stream. Has to be unique.
        TOF_FPS (int):
            Frames per second for the time-of-flight sensor.
        VIDEO_FPS (int):
            Frames per second for the MJPEG video encoder.

    Attributes:
        _camera_ip (str):
            Network address of the camera. Only for identification.
        stream_port (int):
            Port for the MJPEG HTTP server.
        TOF_FPS (int):
            Depth frame rate.
        VIDEO_FPS (int):
            Video frame rate.
        _pipeline (dai.Pipeline):
            DepthAI pipeline to be uploaded to the camera.
        _device (dai.Device):
            Active DepthAI device instance.
        _image_queue, _depth_queue, _video_queue (dai.Queue):
            Non-blocking queues for frames.
        server_stream_queue (multiprocessing.Queue):
            IPC queue feeding the streaming server.
        _sync_queue (SyncQueue):
            Helper to synchronize depth + image pairs.
        _image_frame (ndarray):
            Latest RGB frame.
        _depth_frame (ndarray):
            Latest depth frame.
        point_cloud (o3d.geometry.PointCloud):
            Latest fused point cloud.
        streamingServer (multiprocessing.Process):
            Background MJPEG server process.

    Methods:
        _updateVideoQueue():
            Callback invoked on new encoded video frames; enqueues raw JPEG bytes
            into the server_stream_queue for HTTP serving.
        update():
            Polls image & depth queues, synchronizes frames, converts to point cloud.
        _rgbd_to_point_cloud(depth_frame, image_frame, downsample=False, remove_noise=False):
            Builds an Open3D PointCloud from aligned RGB + depth data with optional
            voxel-downsampling and denoising.
        save_point_cloud_alignment():
            Saves the current 'alignment' matrix to disk for later reuse.
        shutdown():
            Gracefully terminates the streaming server process and closes the device.
    """

    def _updateVideoQueue(self):
        new_frame = self._video_queue.tryGet()
        if new_frame is not None:
            try:
                self.server_stream_queue.put(new_frame.getRaw().data.tobytes(), block=False)
            except:
                return

    def __init__(
        self,
        device_info: dai.DeviceInfo,
        stream_port: int,
        TOF_FPS: int,
        VIDEO_FPS: int,
    ):
        self.TOF_FPS = TOF_FPS
        self.VIDEO_FPS = VIDEO_FPS

        self._camera_ip: str = device_info.name
        self.stream_port: int = stream_port
        self._create_pipeline()
        self._device = dai.Device(self.pipeline, device_info)  # Initialize camera
        self._device.setIrLaserDotProjectorBrightness(0)  # Not using active stereo
        self._device_info = device_info

        self._image_queue: dai.DataOutputQueue = self._device.getOutputQueue(
            name="image", maxSize=10, blocking=False  # pyright: ignore[reportCallIssue]
        )
        self._depth_queue: dai.DataOutputQueue = self._device.getOutputQueue(
            name="depth", maxSize=10, blocking=False  # pyright: ignore[reportCallIssue]
        )
        self._video_queue: dai.DataOutputQueue = self._device.getOutputQueue(
            name="video", maxSize=1, blocking=False  # pyright: ignore[reportCallIssue]
        )
        self._video_queue.addCallback(self._updateVideoQueue)
        self.server_stream_queue = Queue(maxsize=1)  # Queue for IPC
        self._sync_queue = SyncQueue(["image", "depth"])

        self._image_frame = None
        self._depth_frame = None
        self.point_cloud = o3d.geometry.PointCloud()

        self._load_calibration()

        print("=== Connected to " + self._device_info.name)

        # Start streams as seperate processes
        self.streamingServer = Process(
            target=startStreamingServer,
            daemon=True,
            args=(self.server_stream_queue, VIDEO_FPS, stream_port),
            name=f"{self._camera_ip}-stream",
        )
        self.streamingServer.start()
        print(
            f"Starting streaming server for camera {device_info.name} with PID {self.streamingServer.pid}"
        )

    def shutdown(self):
        self.streamingServer.terminate()
        self._device.close()
        print("=== Closed " + self._device_info.name)

    def __del__(self):
        try:
            self.shutdown()
        except:
            return

    def _load_calibration(self):
        path = f"{CALIBRATION_DATA_DIR}/extrinsics_{self._camera_ip}.npz"
        try:
            extrinsics = np.load(path)
            self.cam_to_world = extrinsics["cam_to_world"]
            self.world_to_cam = extrinsics["world_to_cam"]
        except:
            # TODO: figure out how to handle b/c calibration data is mandatory
            # raise RuntimeError(f"Could not load calibration data for camera {self.camera_ip} from {path}!")
            print("No extrinsic calibration data for camera")

        calibration = self._device.readCalibration()
        intrinsics = calibration.getCameraIntrinsics(
            # TODO: Figure out if this is the correct socket
            dai.CameraBoardSocket.RGB,
            dai.Size2f(*self.image_size),  # type: ignore
        )

        self.pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(
            *self.image_size,
            intrinsics[0][0],
            intrinsics[1][1],
            intrinsics[0][2],
            intrinsics[1][2],
        )

        try:
            self.alignment = np.load(
                f"{CALIBRATION_DATA_DIR}/alignment_{self._camera_ip}.npy"
            )
        except:
            self.alignment = np.eye(4)  # Default to no alignment correction

        # print(self.pinhole_camera_intrinsic)

    def save_point_cloud_alignment(self):
        np.save(
            f"{CALIBRATION_DATA_DIR}/alignment_{self._camera_ip}.npy", self.alignment
        )

    def _create_pipeline(self):
        pipeline = dai.Pipeline()

        # Video encoder (MJPEG) for frontend
        video_enc = pipeline.create(dai.node.VideoEncoder)
        video_enc.setDefaultProfilePreset(
            self.VIDEO_FPS, dai.VideoEncoderProperties.Profile.MJPEG
        )
        video_enc.setFrameRate(self.VIDEO_FPS)

        # Link video encoder output to XLinkOut("video")
        xout_video = pipeline.createXLinkOut()
        xout_video.setStreamName("video")
        xout_video.setFpsLimit(self.VIDEO_FPS)
        xout_video.input.setBlocking(False)
        xout_video.input.setQueueSize(1)
        video_enc.bitstream.link(xout_video.input)

        # Time‐of‐flight / depth pipeline
        # Create ToF config
        xin_tof_cfg = pipeline.create(dai.node.XLinkIn)
        xin_tof_cfg.setStreamName("tofConfig")

        tof = pipeline.create(dai.node.ToF)

        xin_tof_cfg.out.link(tof.inputConfig)

        # Apply ToF settings
        cfg = tof.initialConfig.get()
        cfg.enableOpticalCorrection = True
        cfg.enablePhaseShuffleTemporalFilter = True
        cfg.phaseUnwrappingLevel = 1
        cfg.phaseUnwrapErrorThreshold = 200
        tof.initialConfig.set(cfg)

        # Raw ToF camera feed
        cam_tof = pipeline.create(dai.node.Camera)
        cam_tof.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        cam_tof.setFps(self.TOF_FPS * 2)  # ToF outputs at half this rate
        cam_tof.raw.link(tof.input)

        # ToF to depth output
        xout_depth = pipeline.create(dai.node.XLinkOut)
        xout_depth.setStreamName("depth")
        tof.depth.link(xout_depth.input)

        # RGB camera
        cam_rgb = pipeline.createColorCamera()
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.CAM_C)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_800_P)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        cam_rgb.setIspScale(1, 2)
        cam_rgb.setFps(self.TOF_FPS)
        cam_rgb.setVideoSize(640, 400)

        # RGB image outputs
        xout_image = pipeline.createXLinkOut()
        xout_image.setStreamName("image")
        cam_rgb.isp.link(xout_image.input)
        cam_rgb.video.link(video_enc.input)

        self.image_size = cam_rgb.getIspSize()
        self.pipeline = pipeline

    def update(self):
        for queue in [self._depth_queue, self._image_queue]:
            new_frames = queue.tryGetAll()
            if new_frames is not None:
                for new_frame in new_frames:
                    self._sync_queue.add(queue.getName(), new_frame)

        frame_sync = self._sync_queue.get()
        if frame_sync is None:
            return

        self._depth_frame = frame_sync["depth"].getFrame()
        self._image_frame = frame_sync["image"].getCvFrame()
        rgb = cv2.cvtColor(self._image_frame, cv2.COLOR_BGR2RGB)
        self._rgbd_to_point_cloud(self._depth_frame, rgb)

    def _rgbd_to_point_cloud(
        self, depth_frame, image_frame, downsample=False, remove_noise=False
    ):
        depth_frame = depth_frame[:400, :]  # TODO: Check if this is correct
        rgb_o3d = o3d.geometry.Image(image_frame)
        df = np.copy(depth_frame).astype(np.float32)
        # df -= 20
        depth_o3d = o3d.geometry.Image(df)
        rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
            rgb_o3d, depth_o3d, convert_rgb_to_intensity=(len(image_frame.shape) != 3)
        )

        point_cloud = o3d.geometry.PointCloud.create_from_rgbd_image(
            rgbd_image, self.pinhole_camera_intrinsic, self.world_to_cam
        )

        if downsample:
            point_cloud = point_cloud.voxel_down_sample(voxel_size=0.01)

        if remove_noise:
            point_cloud = point_cloud.remove_statistical_outlier(
                nb_neighbors=30, std_ratio=0.1
            )[0]

        self.point_cloud.points = point_cloud.points
        self.point_cloud.colors = point_cloud.colors

        # correct upside down z axis
        T = np.eye(4)
        T[2, 2] = -1
        self.point_cloud.transform(T)

        # apply point cloud alignment transform
        self.point_cloud.transform(self.alignment)

        return self.point_cloud
