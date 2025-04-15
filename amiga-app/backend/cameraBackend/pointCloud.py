# Modified code from
# https://github.com/luxonis/depthai-experiments/blob/master/gen2-multiple-devices/rgbd-pointcloud-fusion/point_cloud_visualizer.py


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import open3d as o3d
from .camera import Camera
from typing import List
import numpy as np
import datetime
from config import POINTCLOUD_DATA_DIR


class PointCloudFusion:
    def __init__(self, cameras: List[Camera]):
        self.cameras = cameras

    def align_point_clouds(self):
        voxel_radius = [0.04, 0.02, 0.01]
        max_iter = [50, 30, 14]

        master_point_cloud = self.cameras[0].point_cloud  # arbitrary?

        # Figure out alignment for each camera relative to master camera
        for camera in self.cameras[1:]:
            for iter, radius in zip(max_iter, voxel_radius):
                target_down = master_point_cloud.voxel_down_sample(radius)
                target_down.estimate_normals(
                    o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30)
                )

                source_down = camera.point_cloud.voxel_down_sample(radius)
                source_down.estimate_normals(
                    o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30)
                )

                result_icp = o3d.pipelines.registration.registration_colored_icp(
                    source_down,
                    target_down,
                    radius,
                    camera.alignment,
                    o3d.pipelines.registration.TransformationEstimationForColoredICP(),
                    o3d.pipelines.registration.ICPConvergenceCriteria(
                        relative_fitness=1e-6, relative_rmse=1e-6, max_iteration=iter
                    ),
                )

                camera.alignment = result_icp.transformation

            camera.save_point_cloud_alignment()

    def reset_alignment(self):
        for camera in self.cameras:
            camera.alignment = np.identity(4)
            camera.save_point_cloud_alignment()

    def save_point_cloud(self):
        for camera in self.cameras:
            camera.update()
            o3d.io.write_point_cloud(
                f"{POINTCLOUD_DATA_DIR}/{datetime.datetime.now()}_{camera.camera_ip}.ply",
                camera.point_cloud
            )

        fused_point_cloud = self.cameras[0].point_cloud + self.cameras[1].point_cloud
        o3d.io.write_point_cloud(
            f"{POINTCLOUD_DATA_DIR}/{datetime.datetime.now()}_fused.ply", fused_point_cloud)

    def get_point_cloud(self):
        for camera in self.cameras:
            camera.update()
        fused_point_cloud = self.cameras[0].point_cloud + self.cameras[1].point_cloud
        return fused_point_cloud

    def quit(self):
        self.running = False
