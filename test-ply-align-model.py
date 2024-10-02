import numpy as np
import open3d as o3d
import os
from functions_registration import *

# Define the folder path where your PLY files are stored
folder_path = r'C:\Users\sarah\PycharmProjects\CoreKnapenGit\out_01-10'

# Specify the PLY file names
path = os.path.join(folder_path, "point_cloud_20241001_132244.ply")
# Read the point clouds with Open3D
# pcd = o3d.io.read_point_cloud(ply_file_path)

# o3d.visualization.draw_geometries([pcd])
# print(np.asarray(pcd.points)[0][0])

pcd = o3d.io.read_point_cloud(path)
print(np.asarray(pcd.points))