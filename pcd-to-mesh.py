# Import libraries
import numpy as np
import open3d as o3d
import os
from functions_registration import *

# Define the folder path where your PLY files are stored
folder_path = r'C:\Users\sarah\PycharmProjects\CoreKnapenGit\out_01-10'

# Specify the PLY file names
ply_file_path_read = os.path.join(folder_path, "point_cloud_20241001_132244.ply")

# Load a point cloud
# ply_file_path_read = "bunny-pcd.ply"
point_cloud = o3d.io.read_point_cloud(ply_file_path_read)

#Outlier removal
print("Statistical outlier removal")
cl, ind = point_cloud.remove_statistical_outlier(nb_neighbors=20,
                                                    std_ratio=4.0)
# display_inlier_outlier(source_down, ind)
pcd_inlier = point_cloud.select_by_index(ind)
o3d.visualization.draw_geometries([pcd_inlier])

# # Downsample the point cloud with Voxel Downsampling
voxel_size = 0.2
pcd_down, source_fpfh = preprocess_point_cloud(pcd_inlier, voxel_size)
o3d.visualization.draw_geometries([pcd_down])

# Compute normals if PCD does not have
if pcd_down.has_normals() == False:
    print("Estimating normals...")
    pcd_down.estimate_normals()
else:
    print("PCD already has normals. So, skip estimating normals")

# Orient the computed normals w.r.t to the tangent plane.
# This step will solve the normal direction issue. If this step is skipped, there might be holes in the mesh surfaces.
o3d.geometry.PointCloud.orient_normals_consistent_tangent_plane(pcd_down, 10)

# Estimate radius for rolling ball
distances = pcd_down.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 1.5 * avg_dist
print("Minimum neighbour distance = {:.6f}".format(np.min(distances)))
print("Maximum neighbour distance = {:.6f}".format(np.max(distances)))
print("Average neighbour distance = {:.6f}".format(np.mean(distances)))

mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
                                    pcd_down,
                                    o3d.utility.DoubleVector([radius, radius * 2]))

print("PCD Detail: {}".format(pcd_down))
print("Mesh Details: {}".format(mesh))

# Visualize and save the mesh generated from point cloud
#mesh.paint_uniform_color(np.array([0.5, 1.0, 0.5])) # to uniformly color the surface
o3d.visualization.draw_geometries([mesh], window_name='mesh with estimated normals', width=1200, height=800)
o3d.io.write_triangle_mesh("test-pcd-to-mesh.ply", mesh, write_ascii=True)