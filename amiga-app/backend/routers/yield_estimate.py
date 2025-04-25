import os
import open3d as o3d
import numpy as np
from scipy.stats import pearsonr
from typing import TypeAlias
import matplotlib.pyplot as plt
import json


from pathlib import Path

from backend.config import *
from backend.robot_utils import walk_towards, format_track
from fastapi import BackgroundTasks
from fastapi import APIRouter
from fastapi import Request

router = APIRouter()

def estimate_volume(point_cloud: o3d.geometry.PointCloud) -> float:
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
    z_lower = point_cloud[round(num_points * .25), 2]
    z_upper = point_cloud[round(num_points * .95), 2]
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

    return volume_estimate

async def generate_yield_estimate(line_name: str) -> float:
    """_summary_
    Args:
        line_name (str):

    Returns:
        float: Estimated mass of pointclouds captured for the line_name
    """
    # Linear regression parameters placeholder
    m, b = linear_regression_parameters
    pointclouds_dir = f"{POINTCLOUD_DATA_DIR}/{line_name}"
    row_directories = [f.path for f in os.scandir(pointclouds_dir) if f.is_dir()]
    total_volume = 0
    for row_directory in row_directories:
        pointcloud_files = os.listdir(row_directory)
        for pointcloud_filename in pointcloud_files:
            point_cloud = o3d.io.read_point_cloud(pointcloud_filename)
            total_volume += estimate_volume(point_cloud)

    return m * total_volume + b

@router.get("get_yield/{line_name}")
async def get_yield(line_name: str, request: Request):
    pointclouds_dir = f"{POINTCLOUD_DATA_DIR}/{line_name}"
    if not os.path.exists(pointclouds_dir):
        return {"error": "Line Directory not found"}
    cached_estimate_path = f"{pointclouds_dir}/estimate.txt"
    yield_estimate: float
    if os.path.exists(f"{pointclouds_dir}/estimate.txt"):
        with open(cached_estimate_path, 'r') as estimate_file:
            yield_estimate = float(estimate_file.read())
    else:
        yield_estimate = generate_yield_estimate(line_name)
        with open(cached_estimate_path, 'w') as estimate_file:
            estimate_file.write(str(yield_estimate))
    return {"message": yield_estimate}