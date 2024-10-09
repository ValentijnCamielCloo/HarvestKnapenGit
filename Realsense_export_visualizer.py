import open3d as o3d
import numpy as np
import os

def visualize_pointcloud_from_ply(file_path):
    """
    Visualizes a point cloud from a PLY file using Open3D.

    Args:
        file_path (str): Path to the PLY file.
    """
    # Load the point cloud from the PLY file
    pcd = o3d.io.read_point_cloud(file_path)

    # Check if the point cloud is empty
    if pcd.is_empty():
        print("Point cloud is empty. Please check the file.")
        return

    # Visualize the point cloud
    o3d.visualization.draw_geometries([pcd],
                                      window_name="Point Cloud Visualization",
                                      width=800, height=600)

if __name__ == "__main__":
    # Path to the output directory where PLY files are saved
    output_dir = "./output"

    # Get the list of PLY files in the output directory
    existing_files = [f for f in os.listdir(output_dir) if f.endswith(".ply")]
    
    if not existing_files:
        print("No PLY files found in the output directory.")
    else:
        # Sort the files to get the most recent one
        existing_files.sort()  # This will sort alphabetically; adjust if needed for numerical sort
        latest_file = os.path.join(output_dir, existing_files[-1])  # Get the latest file

        # Visualize the point cloud from the latest PLY file
        print(f"Visualizing the point cloud from {latest_file}...")
        visualize_pointcloud_from_ply(latest_file)
