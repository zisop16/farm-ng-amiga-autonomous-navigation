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
    def updateVideoQueue(self):
        new_frames = self.video_queue.tryGetAll()
        for frame in new_frames:
            self.server_stream_queue.put(frame.getRaw().data, block=False)

    def __init__(self, device_info: dai.DeviceInfo, stream_port: str, FPS: int, STREAM_FPS: int):
        self.FPS = FPS
        self.STREAM_FPS = STREAM_FPS

        self._create_pipeline()
        self.device = dai.Device(self.pipeline, device_info)  # Initialize camera
        self.device.setIrLaserDotProjectorBrightness(0)  # Not using active stereo
        self.image_queue = self.device.getOutputQueue(
            name="image", maxSize=10, blocking=False  # pyright: ignore[reportCallIssue]
        )
        self.depth_queue = self.device.getOutputQueue(
            name="depth", maxSize=10, blocking=False  # pyright: ignore[reportCallIssue]
        )
        self.video_queue = self.device.getOutputQueue(
            name="video", maxSize=10, blocking=False  # pyright: ignore[reportCallIssue]
        )
        self.video_queue.addCallback(self.updateVideoQueue)
        self.server_stream_queue = Queue(maxsize=10) # Queue for IPC
        self.sync_queue = SyncQueue(["image", "depth"])

        self.device_info = device_info
        self.camera_ip = device_info.name
        self.stream_port = stream_port

        self.image_frame = None
        self.depth_frame = None
        self.point_cloud = o3d.geometry.PointCloud()

        self._load_calibration()

        print("=== Connected to " + self.device_info.name)

        # Start streams as seperate processes
        self.streamingServer = Process(
            target=startStreamingServer,
            daemon=True,
            args=(self.server_stream_queue, STREAM_FPS, device_info.name, stream_port),
        )
        self.streamingServer.start()

    def __del__(self):
        self.streamingServer.terminate()
        self.device.close()
        print("=== Closed " + self.device_info.getMxId())

    def _load_calibration(self):
        path = f"{CALIBRATION_DATA_DIR}/extrinsics_{self.camera_ip}.npz"
        try:
            extrinsics = np.load(path)
            self.cam_to_world = extrinsics["cam_to_world"]
            self.world_to_cam = extrinsics["world_to_cam"]
        except:
            # TODO: figure out how to handle b/c calibration data is mandatory
            # raise RuntimeError(f"Could not load calibration data for camera {self.camera_ip} from {path}!")
            print("No extrinsic calibration data for camera")

        calibration = self.device.readCalibration()
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
                f"{CALIBRATION_DATA_DIR}/alignment_{self.camera_ip}.npy"
            )
        except:
            self.alignment = np.eye(4)  # Default to no alignment correction

        print(self.pinhole_camera_intrinsic)

    def save_point_cloud_alignment(self):
        np.save(
            f"{CALIBRATION_DATA_DIR}/alignment_{self.camera_ip}.npy", self.alignment
        )

    def _create_pipeline(self):
        pipeline = dai.Pipeline()

        # Video encoder node for frontend stream
        videoEnc = pipeline.create(dai.node.VideoEncoder)
        videoEnc.setDefaultProfilePreset(self.FPS, dai.VideoEncoderProperties.Profile.MJPEG)
        videoEnc.setFrameRate(self.STREAM_FPS)
        xout_image = pipeline.createXLinkOut()
        xout_image.setStreamName("video")
        videoEnc.bitstream.link(xout_image.input)

        # Output frontend streaming server node
        # server = pipeline.create(dai.node.Script)
        # videoEnc.bitstream.link(server.inputs['frame'])

        # server.setProcessor(dai.ProcessorType.LEON_CSS)
        # server.inputs['frame'].setBlocking(False)
        # server.inputs['frame'].setQueueSize(1)
        #
        # server.setScript(f"""
        # import time
        # import socket
        # from http.server import BaseHTTPRequestHandler, HTTPServer
        #
        # class HTTPHandler(BaseHTTPRequestHandler):
        #     def do_GET(self):
        #         if self.path == '/rgb':
        #             try:
        #                 delay = {1/FPS}
        #                 self.send_response(200)
        #                 self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
        #                 self.end_headers()
        #                 while True:
        #                     frame = node.io['frame'].get()
        #
        #                     self.wfile.write("--jpgboundary".encode())
        #                     self.wfile.write(bytes([13, 10]))
        #                     self.send_header('Content-type', 'image/jpeg')
        #                     self.send_header('Content-length', str(len(frame.getData())))
        #                     self.end_headers()
        #                     self.wfile.write(frame.getData())
        #                     self.end_headers()
        #                     time.sleep(delay)
        #
        #             except Exception as ex:
        #                 node.warn("Client disconnected")
        #
        # class ThreadingSimpleServer(HTTPServer):
        #     pass
        #
        # with ThreadingSimpleServer(("", {stream_port}), HTTPHandler) as httpd:
        #     node.warn(f"Serving RGB MJPEG stream at {camera_ip + ":" + stream_port + "/rgb"}")
        #     httpd.serve_forever()
        # """)

        # Time of Flight to depth node
        tof = pipeline.create(dai.node.ToF)
        tofConfig = tof.initialConfig.get()
        # TODO: Figure out optimal settings
        # see ToF node docs on how to reduce/eliminate motion blur.
        tofConfig.enableOpticalCorrection = True
        tofConfig.enablePhaseShuffleTemporalFilter = True
        tofConfig.phaseUnwrappingLevel = 1
        tofConfig.phaseUnwrapErrorThreshold = 200
        # tofConfig.enableTemperatureCorrection = False # Not yet supported
        xinTofConfig = pipeline.create(dai.node.XLinkIn)
        xinTofConfig.setStreamName("tofConfig")
        xinTofConfig.out.link(tof.inputConfig)

        tof.initialConfig.set(tofConfig)

        # Raw ToF camera node
        cam_tof = pipeline.create(dai.node.Camera)
        cam_tof.setFps(self.FPS * 2)  # ToF node will produce depth frames at /2 of this rate
        cam_tof.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        cam_tof.raw.link(tof.input)

        # Output depth node
        xout = pipeline.create(dai.node.XLinkOut)
        xout.setStreamName("depth")
        tof.depth.link(xout.input)

        # RGB cam
        xout_image = pipeline.createXLinkOut()
        xout_image.setStreamName("image")
        cam_rgb = pipeline.createColorCamera()
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.CAM_C)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_800_P)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        cam_rgb.setIspScale(1, 2)
        cam_rgb.setFps(self.FPS)
        cam_rgb.setVideoSize(640, 400)
        # cam_rgb.initialControl.setManualFocus(130)

        cam_rgb.isp.link(xout_image.input)
        cam_rgb.video.link(videoEnc.input)

        self.image_size = cam_rgb.getIspSize()
        self.pipeline = pipeline

    def update(self):
        for queue in [self.depth_queue, self.image_queue]:
            new_msgs = queue.tryGetAll()
            if new_msgs is not None:
                for new_msg in new_msgs:
                    self.sync_queue.add(queue.getName(), new_msg)

        msg_sync = self.sync_queue.get()
        if msg_sync is None:
            return

        self.depth_frame = msg_sync["depth"].getFrame()
        self.image_frame = msg_sync["image"].getCvFrame()
        rgb = cv2.cvtColor(self.image_frame, cv2.COLOR_BGR2RGB)
        self.rgbd_to_point_cloud(self.depth_frame, rgb)

    def rgbd_to_point_cloud(
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
