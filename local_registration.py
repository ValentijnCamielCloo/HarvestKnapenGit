import open3d as o3d
import numpy as np
import copy


# Function to visualize the registration
def draw_registration_result(source, target):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    
    # Paint the point clouds with different colors
    source_temp.paint_uniform_color([1, 0.706, 0])  # Orange for source
    target_temp.paint_uniform_color([0, 0.651, 0.929])  # Blue for target
    
    # Apply the transformation to the source point cloud
    # source_temp.transform(transformation)
    
    # Use Open3D's built-in visualization to display the point clouds
    o3d.visualization.draw_geometries([source_temp, target_temp])

# # Define an initial transformation matrix
# trans_init = np.asarray([[0.862, 0.011, -0.507, 0.5],
#                          [-0.139, 0.967, -0.215, 0.7],
#                          [0.487, 0.255, 0.835, -1.4],
#                          [0.0, 0.0, 0.0, 1.0]])

# Read Source and Target PCD
demo_pcds = o3d.data.DemoICPPointClouds()
source = o3d.io.read_point_cloud(demo_pcds.paths[0])
target = o3d.io.read_point_cloud(demo_pcds.paths[1])


# Visualize the source and target point clouds with the initial transformation
draw_registration_result(source, target)