import meshio
import SeismicMesh

bbox          = (-1.5, 0.0, -0.5, 1.5)
square        = SeismicMesh.Rectangle(bbox)
points, cells = SeismicMesh.generate_mesh(domain=square, edge_length=0.02)

print(len(points))
meshio.write_points_cells(
    "square.msh",
    points,
    [("triangle", cells)],
    file_format="gmsh22",
    binary=False
)


