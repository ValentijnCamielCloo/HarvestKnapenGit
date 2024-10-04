import numpy as np
import open3d as o3d
import os

# Define the folder path where your PLY files are stored and where the filtered PLY will be saved
input_folder = r'C:\Users\sarah\PycharmProjects\CoreKnapenGit\out_01-10'
output_folder = r'C:\Users\sarah\PycharmProjects\CoreKnapenGit\filtered_point_clouds'

os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

# Specify the PLY file name to load
ply_file_path = os.path.join(input_folder, "point_cloud_20241001_132244.ply")

# Step 1: Load the point cloud from the PLY file
pcd = o3d.io.read_point_cloud(ply_file_path)

# Convert the points of the point cloud to a NumPy array
points = np.asarray(pcd.points)

# Step 2: Remove points where z = 0
non_zero_points = points[points[:, 2] != 0]  # Removing points with z = 0

# Step 3: Filter points based on z-value (between 1.3 and 1.7 meters)
filtered_points = non_zero_points[(non_zero_points[:, 2] >= 1.4) & (non_zero_points[:, 2] <= 1.6)]

print(f"Number of points before filtering: {len(points)}")
print(f"Number of points after filtering: {len(filtered_points)}")

# Step 4: Create a new point cloud from the filtered points
filtered_pcd = o3d.geometry.PointCloud()
filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)

# Step 5: Perform Voxel Downsampling
voxel_size = 0.02  # Adjust the voxel size as needed
downsampled_pcd = filtered_pcd.voxel_down_sample(voxel_size)

print(f"Number of points after downsampling: {len(downsampled_pcd.points)}")

# Step 6: Remove outliers using Statistical Outlier Removal
# Here we can define the number of neighbors and the standard deviation multiplier
nb_neighbors = 20  # Number of neighbors to consider
std_ratio = 0.2    # Standard deviation ratio

# Perform outlier removal
cl, ind = downsampled_pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)

# Select inliers (non-outliers)
inlier_pcd = downsampled_pcd.select_by_index(ind)

print(f"Number of points after outlier removal: {len(inlier_pcd.points)}")

# Step 7: Visualize the filtered point cloud with outlier removal (optional)
o3d.visualization.draw_geometries([inlier_pcd])

# Step 8: Save the filtered point cloud to a new PLY file
output_file = os.path.join(output_folder, "filtered_point_cloud.ply")
o3d.io.write_point_cloud(output_file, inlier_pcd)

print(f"Filtered point cloud saved to: {output_file}")

