import numpy as np
import open3d as o3d
import os
from functions_registration import *
import copy

# Define the folder path where your PLY files are stored
folder_path = r'C:\Users\sarah\PycharmProjects\CoreKnapenGit\out_01-10'

# Specify the PLY file names
path = os.path.join(folder_path, "point_cloud_20241001_132244.ply")

# Read the point cloud with Open3D
pcd = o3d.io.read_point_cloud(path)

# Outlier removal
print("Statistical outlier removal")
cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=5.0)

# Select inliers only
inlier_pcd = pcd.select_by_index(ind)

# Downsample the point cloud with Voxel Downsampling
voxel_size = 0.01
pcd_down, source_fpfh = preprocess_point_cloud(inlier_pcd, voxel_size)

# Make a deep copy of the point cloud for 2D conversion
pcd_2d = copy.deepcopy(pcd_down)

# Convert the points of the point cloud to a NumPy array
points = np.asarray(pcd_2d.points)

# Set the z-values to 0 (flatten onto xy-plane)
points[:, 2] = 0

# Convert the modified NumPy array back into a point cloud object
pcd_2d.points = o3d.utility.Vector3dVector(points)

# Print the modified points
print("Points converted to 2D: ", np.asarray(pcd_2d.points))

# Optionally visualize the result
o3d.visualization.draw_geometries([pcd_2d])
