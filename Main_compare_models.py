from filter_pcd import *
from translate_pcd import *
from pcd_to_mesh import *
from compare_model import *

# Filter the point cloud, only keep point within certain distance from scanner
# For further filtering we use voxel downsampling and statistical outlier removal
filter_pcd('point_cloud_20241001_132244', 'filtered_pcd', 1.4, 1.7)

# Move all the points to one plane and let the corner (left or right) start in the origin (0,0)
translate_pcd('filtered_pcd','translated_pcd_right','Right')

# Create a mesh from the point cloud
pcd_to_mesh('translated_pcd_right', 'mesh_from_pcd_right')

# Compare the mesh from the scan to the final model
# Output: percentage built and m2 to be built
compare_model('test_right', 'mesh_from_pcd_right')