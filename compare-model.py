import open3d as o3d
import numpy as np
import pyvista as pv
import os

def area_mesh(ply_file_path):
    # Load the mesh from the PLY file
    mesh = pv.read(ply_file_path)

    # Use PyVista's built-in method to calculate the area
    total_area = mesh.area
    return total_area

def add_progress_bar(plotter, percentage):
    # Display progress as text with valid position
    plotter.add_text(f"Progress: {percentage:.2f}%", position='upper_right', font_size=10, color='black')

def visualize_meshes_with_progress(file_path_model, file_path_scan, area_model, area_scan):
    # Calculate the percentage built
    percentage_built = (area_scan / area_model) * 100

    # Create a plotter object for visualization
    plotter = pv.Plotter()

    # Load the meshes
    mesh_model = pv.read(file_path_model)
    mesh_scan = pv.read(file_path_scan)

    # Add the model mesh (yellow)
    plotter.add_mesh(mesh_model, color='yellow', opacity=0.5)

    # Add the scan mesh (red)
    plotter.add_mesh(mesh_scan, color='red')

    # Add progress bar as text
    add_progress_bar(plotter, percentage_built)

    # Set background and add additional information
    plotter.set_background("white")
    plotter.add_text(f"Yellow: Model, area: {round(area_model,2)} m2", position='lower_left', color='black', font_size=10)
    plotter.add_text(f"Red: Scan, area: {round(area_scan,2)} m2", position='lower_right', color='black', font_size=10)

    # Display the plot
    plotter.show()

# File paths
file_path_model = r'C:\Users\sarah\PycharmProjects\CoreKnapenGit\comparing_model\test.ply'
file_path_scan = r'C:\Users\sarah\PycharmProjects\CoreKnapenGit\saved_meshes\mesh_from_pcd.ply'

# Calculate area for both meshes
area_mesh_model = area_mesh(file_path_model)
print(f"Total mesh area model: {round(area_mesh_model, 2)} m2")

area_mesh_scan = area_mesh(file_path_scan)
print(f"Total mesh area scan: {round(area_mesh_scan, 2)} m2")

# Visualize meshes and display progress
visualize_meshes_with_progress(file_path_model, file_path_scan, area_mesh_model, area_mesh_scan)
