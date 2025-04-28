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
    dirs = sorted(next(os.walk("amigaCameraCode/ToFCameraPLY/CilantroFieldRun2"))[1])

    for folder_name in dirs:
        pc_filename = f"amigaCameraCode/ToFCameraPLY/CilantroFieldRun2/{folder_name}/tof_pointcloud.ply"
        point_cloud = o3d.io.read_point_cloud(pc_filename)

        volume_estimate, percent_size_change, point_cloud = estimate_volume(point_cloud)
        volume_estimates.append(volume_estimate)

        visual = True
        
        if visual:
            voxel_size = 2
            voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud, voxel_size=voxel_size)
            vis = o3d.visualization.Visualizer()
            vis.create_window(height=800, width=800)
            vis.add_geometry(voxel_grid)
            vis.run()


    with open("volumes_estimate.json", "w") as estimate_file:
        json.dump(volume_estimates, estimate_file)
    


    weights: list[int] = []
    with open(
        f"amigaCameraCode/ToFCameraPLY/CilantroFieldRun2/CilantroWeights.csv", "r"
    ) as f:
        for line in f:
            weights.append(int(line.split(",")[1]))

    corr, _ = pearsonr(volume_estimates, weights)
    corr = round(corr, 4)

    plt.scatter(volume_estimates, weights)
    plt.xlabel("Volume Estimation (cm^3)")
    plt.ylabel("Weight (g)")
    m, b = np.polyfit(volume_estimates, weights, 1)
    plt.plot(volume_estimates, m * np.array(volume_estimates) + b, color="red")

    average_error = 0.0
    for i in range(len(weights)):
        average_error += abs(m * volume_estimates[i] + b - weights[i]) / weights[i]
    average_error /= len(weights)
    average_error = round(average_error, 4)

    plt.rc("font", size=8)
    plt.title(f"Correlation Coefficient: {corr} \nAverage Error: {average_error}")
    plt.savefig("volume_weight_graph.png")
    plt.show()
