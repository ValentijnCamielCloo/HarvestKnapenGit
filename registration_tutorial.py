import open3d as o3d    #Version 0.18.0
import numpy as np      #Version 1.26.4
import copy


# Function to visualize the registration
def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    
    # Paint the point clouds with different colors
    source_temp.paint_uniform_color([1, 0.706, 0])  # Orange for source
    target_temp.paint_uniform_color([0, 0.651, 0.929])  # Blue for target
    
    # Apply the transformation to the source point cloud
    source_temp.transform(transformation)
    
    # Use Open3D's built-in visualization to display the point clouds
    o3d.visualization.draw_geometries([source_temp, target_temp])

# # Define an initial transformation matrix
trans_init = np.asarray([[0.862, 0.011, -0.507, 0.5],
                         [-0.139, 0.967, -0.215, 0.7],
                         [0.487, 0.255, 0.835, -1.4],
                         [0.0, 0.0, 0.0, 1.0]])

# Read Source and Target PCD
demo_pcds = o3d.data.DemoICPPointClouds()
source = o3d.io.read_point_cloud(demo_pcds.paths[0])
target = o3d.io.read_point_cloud(demo_pcds.paths[1])

# Visualize the source and target point clouds with the initial transformation
# draw_registration_result(source, target, trans_init)

threshold=0.02
print("Initial alignment")
evaluation = o3d.pipelines.registration.evaluate_registration(
    source, target, threshold, trans_init)
print(evaluation)

# # threshold (=max_correspondence_distance) = maximum correspondence point-par distance
# threshold=0.02
# print("Apply point-to-point ICP")
# # Registration Point to Point: registration::TransformationEstimationPointToPoint
# # Registration Point to Plane:registration::TransformationEstimationPointToPlane
# reg_p2p = o3d.pipelines.registration.registration_icp(
#     source, target, threshold, trans_init,
#     o3d.pipelines.registration.TransformationEstimationPointToPlane())
# print(reg_p2p)
# print("Transformation is:")
# print(reg_p2p.transformation)
# draw_registration_result(source, target, reg_p2p.transformation)

#Function for downsampling the point cloud
def preprocess_point_cloud(pcd, voxel_size):
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh

voxel_size = 0.05
source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)