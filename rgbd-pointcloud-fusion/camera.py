import depthai as dai
import cv2
import numpy as np
import open3d as o3d
from typing import List
from matplotlib import colors
import config
from host_sync import HostSync

class Camera:
    def __init__(self, device_info: dai.DeviceInfo, friendly_id: int, show_video: bool = True, show_point_cloud: bool = True):
        self.show_video = show_video
        self.show_point_cloud = show_point_cloud
        self.show_depth = False
        self.device_info = device_info
        self.friendly_id = friendly_id
        self.mxid = device_info.name
        self._create_pipeline()
        self.device = dai.Device(self.pipeline, self.device_info)

        self.device.setIrLaserDotProjectorBrightness(1200)

        self.intrinsic_mat = np.array(self.device.readCalibration().getCameraIntrinsics(dai.CameraBoardSocket.RGB, 3840, 2160))
        print(self.intrinsic_mat)


        self.image_queue = self.device.getOutputQueue(name="image", maxSize=10, blocking=False)
        self.depth_queue = self.device.getOutputQueue(name="depth", maxSize=10, blocking=False)
        self.host_sync = HostSync(["image", "depth"])

        self.image_frame = None
        self.depth_frame = None
        self.depth_visualization_frame = None
        self.point_cloud = o3d.geometry.PointCloud()

        # camera window
        self.window_name = f"[{self.friendly_id}] Camera - mxid: {self.mxid}"
        if show_video:
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(self.window_name, 640, 360)

        # point cloud window
        if show_point_cloud:
            self.point_cloud_window = o3d.visualization.Visualizer()
            self.point_cloud_window.create_window(window_name=f"[{self.friendly_id}] Point Cloud - mxid: {self.mxid}")
            self.point_cloud_window.add_geometry(self.point_cloud)
            origin = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.3, origin=[0, 0, 0])
            self.point_cloud_window.add_geometry(origin)
            self.point_cloud_window.get_view_control().set_constant_z_far(config.max_range*2)

        self._load_calibration()

        print("=== Connected to " + self.device_info.getMxId())

    def __del__(self):
        self.device.close()
        print("=== Closed " + self.device_info.getMxId())

    def _load_calibration(self):
        path = f"{config.calibration_data_dir}/extrinsics_{self.mxid}.npz"
        try:
            extrinsics = np.load(path)
            self.cam_to_world = extrinsics["cam_to_world"]
            self.world_to_cam = extrinsics["world_to_cam"]
        except:
            raise RuntimeError(f"Could not load calibration data for camera {self.mxid} from {path}!")

        calibration = self.device.readCalibration()
        self.intrinsics = calibration.getCameraIntrinsics(
            dai.CameraBoardSocket.RGB if config.COLOR else dai.CameraBoardSocket.RIGHT, 
            dai.Size2f(*self.image_size)
        )

        self.pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(
            *self.image_size, self.intrinsics[0][0], self.intrinsics[1][1], self.intrinsics[0][2], self.intrinsics[1][2]
        )

        try:
            self.point_cloud_alignment = np.load(f"{config.calibration_data_dir}/point_cloud_alignment_{self.mxid}.npy")
        except:
            self.point_cloud_alignment = np.eye(4)

        print(self.pinhole_camera_intrinsic)

    def save_point_cloud_alignment(self):
        np.save(f"{config.calibration_data_dir}/point_cloud_alignment_{self.mxid}.npy", self.point_cloud_alignment)
    

    def _create_pipeline(self):
        pipeline = dai.Pipeline()

        # Time of Flight to dppth node
        tof = pipeline.create(dai.node.ToF)
        tofConfig = tof.initialConfig.get()
        # TODO: Figure out optimal settings
        # Optional. Best accuracy, but adds motion blur.
        # see ToF node docs on how to reduce/eliminate motion blur.
        tofConfig.enableOpticalCorrection = True
        tofConfig.enablePhaseShuffleTemporalFilter = True
        tofConfig.phaseUnwrappingLevel = 1
        tofConfig.phaseUnwrapErrorThreshold = 230
        # tofConfig.enableTemperatureCorrection = False # Not yet supported
        xinTofConfig = pipeline.create(dai.node.XLinkIn)
        xinTofConfig.setStreamName("tofConfig")
        xinTofConfig.out.link(tof.inputConfig)

        tof.initialConfig.set(tofConfig)


        # Raw ToF camera node
        cam_tof = pipeline.create(dai.node.Camera)
        cam_tof.setFps(60) # ToF node will produce depth frames at /2 of this rate
        cam_tof.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        cam_tof.raw.link(tof.input)


        # Output depth node
        xout = pipeline.create(dai.node.XLinkOut)
        xout.setStreamName("depth")
        tof.depth.link(xout.input)


        # RGB cam
        cam_rgb = pipeline.create(dai.node.ColorCamera)
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.CAM_C)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_800_P)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        cam_rgb.setIspScale(1, 2)
        cam_rgb.setFps(30)
        cam_rgb.setVideoSize(640, 400)
        # cam_rgb.initialControl.setManualFocus(130)

        xout_image = pipeline.createXLinkOut()
        xout_image.setStreamName("image")
        cam_rgb.isp.link(xout_image.input)

        self.image_size = cam_rgb.getIspSize()
        print("Size", cam_rgb.getIspSize())
        self.pipeline = pipeline


    def update(self):
        for queue in [self.depth_queue, self.image_queue]:
            new_msgs = queue.tryGetAll()
            if new_msgs is not None:
                for new_msg in new_msgs:
                    self.host_sync.add(queue.getName(), new_msg)

        msg_sync = self.host_sync.get()
        if msg_sync is None:
            return
        
        self.depth_frame = msg_sync["depth"].getFrame()
        self.image_frame = msg_sync["image"].getCvFrame()
        self.depth_visualization_frame = cv2.normalize(self.depth_frame, None, 255, 0, cv2.NORM_INF, cv2.CV_8UC1)
        self.depth_visualization_frame = cv2.equalizeHist(self.depth_visualization_frame)
        self.depth_visualization_frame = cv2.applyColorMap(self.depth_visualization_frame, cv2.COLORMAP_HOT)

        if self.show_video:
            if self.show_depth:
                cv2.imshow(self.window_name, self.depth_visualization_frame)
            else:
                cv2.imshow(self.window_name, self.image_frame)

        rgb = cv2.cvtColor(self.image_frame, cv2.COLOR_BGR2RGB)
        self.rgbd_to_point_cloud(self.depth_frame, rgb)

        if self.show_point_cloud:
            self.point_cloud_window.update_geometry(self.point_cloud)
            self.point_cloud_window.poll_events()
            self.point_cloud_window.update_renderer()


    def filter_non_green_points(self, point_cloud: o3d.geometry.PointCloud, visualize: bool = False) -> o3d.geometry.PointCloud:

        pc_points = np.asarray(point_cloud.points)
        pc_colors = np.asarray(point_cloud.colors)

        colors_hsv = colors.rgb_to_hsv(pc_colors)

        HUE = 0
        SAT = 1
        VAL = 2
        green_lower_hue = 65/360.
        green_upper_hue = 165/360.
        lower_sat = .10
        lower_value = .20

        hues = colors_hsv[:, HUE]
        saturations = colors_hsv[:, SAT]
        values = colors_hsv[:, VAL]


        mask = (hues >= green_lower_hue) and (hues <= green_upper_hue) and (saturations > lower_sat) and (values > lower_value)

        filtered_points = pc_points[mask]
        filtered_colors = pc_colors[mask]

        filtered_cloud = o3d.geometry.PointCloud()
        filtered_cloud.points = o3d.utility.Vector3dVector(filtered_points)
        filtered_cloud.colors = o3d.utility.Vector3dVector(filtered_colors)
        # if visualize:
        #     o3d.visualization.draw_geometries([point_cloud])
        #     o3d.visualization.draw_geometries([filtered_cloud])

        return filtered_cloud


    def rgbd_to_point_cloud(self, depth_frame, image_frame, downsample=False, remove_noise=False):
        depth_frame = depth_frame[:400, :]
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
            point_cloud = point_cloud.remove_statistical_outlier(nb_neighbors=30, std_ratio=0.1)[0]

        self.point_cloud.points = point_cloud.points
        self.point_cloud.colors = point_cloud.colors

        # correct upside down z axis
        T = np.eye(4)
        T[2,2] = -1
        self.point_cloud.transform(T)

        # apply point cloud alignment transform
        self.point_cloud.transform(self.point_cloud_alignment)

        return self.filter_non_green_points( self.point_cloud )
