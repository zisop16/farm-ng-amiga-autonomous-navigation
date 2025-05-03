import os
import open3d as o3d
import numpy as np
from scipy.stats import pearsonr
from typing import TypeAlias
import matplotlib.pyplot as plt
import json

def estimate_volume(point_cloud: o3d.geometry.PointCloud) -> tuple[float, float, o3d.geometry.PointCloud]:
    """_summary_ Estimate the volume of the point cloud

    Args:
        point_cloud (o3d.geometry.PointCloud):

    Returns:
        tuple[float, float, o3d.geometry.PointCloud]: Estimated volume, Percentage of points filtered, Bounded PointCloud
    """
    colors = np.asarray(point_cloud.colors)
    point_cloud = np.asarray(point_cloud.points)
    
    height_sort = np.argsort(point_cloud[:, 2])
    point_cloud = point_cloud[height_sort]
    colors = colors[height_sort]

    num_points = len(point_cloud)
    

    # Bounding box parameters
    # z_lower = point_cloud[round(num_points * .25), 2]
    # z_upper = point_cloud[round(num_points * .95), 2]
    z_lower = point_cloud[0, 2]
    z_upper = point_cloud[-1, 2]
    x_lower = -250
    x_upper = 450
    y_lower = -270
    y_upper = 330

    x_coords = point_cloud[:, 0]
    y_coords = point_cloud[:, 1]
    z_coords = point_cloud[:, 2]
    z_filter = (z_lower < z_coords) & (z_coords < z_upper)
    x_filter = (x_lower < x_coords) & (x_coords < x_upper)
    y_filter = (y_lower < y_coords) & (y_coords < y_upper)

    box_filter = z_filter & x_filter & y_filter
    filtered_area = (x_upper - x_lower) * (y_upper - y_lower)


    point_cloud = point_cloud[box_filter]
    colors = colors[box_filter]

    average_z = np.mean(point_cloud[:, 2])
    average_height = z_upper - average_z

    volume_estimate = average_height * filtered_area / 1000 # cm^3

    percent_size_change = (num_points - len(point_cloud)) / num_points

    point_cloud = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(point_cloud))
    point_cloud.colors = o3d.utility.Vector3dVector(colors)

    return volume_estimate, percent_size_change, point_cloud


if __name__ == '__main__':
    volume_estimates: list[float] = []
    pointcloud_directory = "./pointclouds/maytest/row_0"
    pointclouds = os.listdir(pointcloud_directory)
    
    first_cap = True
    cap_0 = f"{pointcloud_directory}/capture_0"
    n = 256000
    cloud_num = 0
    for filename in os.listdir(cap_0):
        if filename == "combined.ply":
            continue
        pc_path = f"{cap_0}/{filename}"
        point_cloud = o3d.io.read_point_cloud(pc_path)
        pts = np.asarray(point_cloud.points)
        clrs = np.asarray(point_cloud.colors)
        if cloud_num == 0:
            colors_0 = clrs
            points_0 = pts
        elif cloud_num == 1:
            colors_1 = clrs
            points_1 = pts
        else:
            colors_2 = clrs
            points_2 = pts
        cloud_num += 1

    cal_dir = "./calibration_data"
    cal_files = os.listdir(cal_dir)
    mat_num = 0
    for filename in cal_files:
        cal_path = f"{cal_dir}/{filename}"
        cal_file = np.load(cal_path)
        transform_matrix = cal_file["world_to_cam"]
        rot_mat = transform_matrix[:3, :3]
        trans_vec = np.array([transform_matrix[3, :3]]).T
        if mat_num == 0:
            rot_0 = rot_mat
            trans_0 = trans_vec
        elif mat_num == 1:
            rot_1 = rot_mat
            trans_1 = trans_vec
        else:
            rot_2 = rot_mat
            trans_2 = trans_vec
        mat_num += 1

    def apply_transform(points_0, points_1, points_2):
        points_0 = (rot_0 @ points_0.T + trans_0).T
        points_1 = (rot_1 @ points_1.T + trans_1).T
        points_2 = (rot_2 @ points_2.T + trans_2).T
        return points_0, points_1, points_2
    
    points_0, points_1, points_2 = apply_transform(points_0, points_1, points_2)

    all_points = np.concatenate([points_0, points_2], axis=0)
    all_colors = np.concatenate([colors_0, colors_2], axis=0)

    print(all_points.shape)
    point_cloud = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(all_points))
    point_cloud.colors = o3d.utility.Vector3dVector(all_colors)
    voxel_size = 2
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud, voxel_size=voxel_size)
    vis = o3d.visualization.Visualizer()
    vis.create_window(height=800, width=800)
    vis.add_geometry(voxel_grid)
    vis.run()


    for filename in pointclouds:
        break
        pointcloud_path = f"{pointcloud_directory}/{filename}/combined.ply"
        point_cloud = o3d.io.read_point_cloud(pointcloud_path)

        volume_estimate, percent_size_change, point_cloud = estimate_volume(point_cloud)
        volume_estimates.append(volume_estimate)

        visual = True
        print(f"Pointcloud {filename}: Filtered out {percent_size_change} of points, estimated volume {volume_estimate}")
        if visual:
            voxel_size = 2
            voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud, voxel_size=voxel_size)
            vis = o3d.visualization.Visualizer()
            vis.create_window(height=800, width=800)
            vis.add_geometry(voxel_grid)
            vis.run()