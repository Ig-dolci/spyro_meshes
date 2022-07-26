# Mesh a cylinder
from mpi4py import MPI
import meshio

import SeismicMesh

comm = MPI.COMM_WORLD

hmin = 0.10

cylinder = SeismicMesh.Cylinder(h=1.0, r=0.5)

points, cells = SeismicMesh.generate_mesh(
    domain=cylinder,
    edge_length=hmin,
)

points, cells = SeismicMesh.sliver_removal(
    points=points,
    domain=cylinder,
    edge_length=hmin,
)

if comm.rank == 0:
    meshio.write_points_cells(
        "Cylinder.vtk",
        points,
        [("tetra", cells)],
        file_format="vtk",
    )