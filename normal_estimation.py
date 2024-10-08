import open3d as o3d

# Step 1: Read the PLY file
point_cloud = o3d.io.read_point_cloud(r"C:\Users\sarah\PycharmProjects\CoreKnapenGit\out_01-10\point_cloud_20241001_132244.ply")  # Replace with your file path

# Step 2: Voxel downsampling
voxel_size = 0.02  # Adjust voxel size based on your needs
downsampled_pc = point_cloud.voxel_down_sample(voxel_size=voxel_size)

# Step 3: Estimate normals on the downsampled point cloud
downsampled_pc.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

# Step 4: Flip normals towards a specific direction (e.g., towards the camera or origin)
downsampled_pc.orient_normals_towards_camera_location(camera_location=[0, 0, 0])  # Origin [0, 0, 0]

# Step 5: Visualize the downsampled point cloud with flipped normals
o3d.visualization.draw_geometries([downsampled_pc], point_show_normal=True)
