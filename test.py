import open3d as o3d
import os
import pyvista as pv

input_folder = r'C:\Users\sarah\PycharmProjects\CoreKnapenGit\saved_meshes'
file_path_scan = os.path.join(input_folder, "mesh_from_pcd_right.ply")
point_cloud = o3d.io.read_point_cloud(file_path_scan)

plotter = pv.Plotter()
mesh_scan = pv.read(file_path_scan)

o3d.visualization.draw_geometries([mesh_scan],
                                  zoom=0.4459,
                                  front=[0.9288, -0.2951, -0.2242],
                                  lookat=[1.6784, 2.0612, 1.4451],
                                  up=[-0.3402, -0.9189, -0.1996])