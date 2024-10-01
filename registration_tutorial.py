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

# Define an initial transformation matrix
trans_init = np.asarray([[0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]])

# Read Source and Target PCD
demo_pcds = o3d.data.DemoICPPointClouds()
source = o3d.io.read_point_cloud(demo_pcds.paths[0])
target = o3d.io.read_point_cloud(demo_pcds.paths[1])

# Visualize the source and target point clouds with the initial transformation
draw_registration_result(source, target, trans_init)

source.transform(trans_init)
# draw_registration_result(source, target, np.identity(4))

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

def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    print(result.transformation)
    return result

trans_global = execute_global_registration(source_down, target_down,
                                            source_fpfh, target_fpfh,
                                            voxel_size)
print("trans_global: ",trans_global)
draw_registration_result(source_down, target_down, trans_global.transformation)

# threshold (=max_correspondence_distance) = maximum correspondence point-par distance
threshold=0.02

# def icp_local(source, target, threshold, trans_global, type="PointToPlane"):
#     if type == "PointToPlane":
#         print("Apply point-to-plane ICP")
#         # Registration Point to Plane:registration::TransformationEstimationPointToPlane
#         reg_p2p = o3d.pipelines.registration.registration_icp(
#             source, target, threshold, trans_global,
#             o3d.pipelines.registration.TransformationEstimationPointToPlane())
#
#     else:
#         print("Apply point-to-point ICP")
#         # Registration Point to Plane:registration::TransformationEstimationPointToPoint
#         reg_p2p = o3d.pipelines.registration.registration_icp(
#             source, target, threshold, trans_init,
#             o3d.pipelines.registration.TransformationEstimationPointToPoint())
#
#     print(reg_p2p)
#     print("Transformation is:")
#     print(reg_p2p.transformation)
#     return reg_p2p


print("Apply point-to-plane ICP")
# Registration Point to Plane:registration::TransformationEstimationPointToPlane
reg_p2p = o3d.pipelines.registration.registration_icp(
    source_down, target_down, threshold, trans_global.transformation,
    o3d.pipelines.registration.TransformationEstimationPointToPlane())
print("Reg_p2p: ", reg_p2p)
# print("Transformation is:")
# print(reg_p2p.transformation)
#
# trans_local = icp_local(source, target, threshold, result_ransac)
draw_registration_result(source_down, target_down, reg_p2p.transformation)

# threshold=0.02
# print("Local alignment")
# evaluation = o3d.pipelines.registration.evaluate_registration(
#     source_down, target_down, threshold, reg_p2p.transformation)
# print(evaluation)