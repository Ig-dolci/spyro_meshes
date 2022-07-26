# mesh a cuboid/cube
import meshio
import SeismicMesh

bbox = (-1.0, 0.0, 0.0, 1.0, 0.0, 1.0)
cube = SeismicMesh.Cube(bbox)
points, cells = SeismicMesh.generate_mesh(domain=cube, edge_length=0.05)
points, cells = SeismicMesh.sliver_removal(points=points, domain=cube, edge_length=0.05)

meshio.write_points_cells(
    "cube.msh",
    points,
    [("tetra", cells)],
    file_format="gmsh22",
    binary=False,
)