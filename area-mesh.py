import pyvista as pv
import os
import math

# Define the folder path where your PLY files are stored
folder_path = r'C:\Users\sarah\PycharmProjects\CoreKnapenGit\saved_meshes'

# Specify the PLY file names
ply_file = os.path.join(folder_path, "mesh_from_pcd.ply")

# Load the mesh from the PLY file
mesh = pv.read(ply_file)

# Extract vertices
vertices = mesh.points  # This will give you an Nx3 array of vertices

# Extract faces (triangles)
faces = mesh.faces.reshape((-1, 4))[:, 1:]  # The first element of each face indicates the number of points (should be 3)

# Now you can calculate the area of the mesh as before
total_area = mesh.area
print(f"Total mesh area: {total_area}")

# Calculate one side from a square
side = math.sqrt(total_area)
print(f"Length one side (when square): {side}")

def area_mesh(ply_file_path):
    # Load the mesh from the PLY file
    mesh = pv.read(ply_file_path)

    # Extract vertices
    vertices = mesh.points  # This will give you an Nx3 array of vertices

    # Extract faces (triangles)
    faces = mesh.faces.reshape((-1, 4))[:,1:]  # The first element of each face indicates the number of points (should be 3)

    # Now you can calculate the area of the mesh as before
    total_area = mesh.area
    print(f"Total mesh area: {total_area}")
    return total_area