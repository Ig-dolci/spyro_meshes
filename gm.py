from mpi4py import MPI
import meshio

from SeismicMesh import get_sizing_function_from_segy, generate_mesh, Rectangle
from SeismicMesh.sizing.mesh_size_function import write_velocity_model
comm = MPI.COMM_WORLD

fname = "c3_2020.npy"

# Bounding box describing domain extents (corner coordinates)
bbox = (-7552.0, 0.0, 0.0, 17312.0)

# Desired minimum mesh size in domain
freq = 7
wl   = 2.41 # Ne # wl para ordem 2
hmin = 1500/(wl*freq)
write_velocity_model(fname,bbox=bbox,domain_pad=700, pad_style='edge')
# write_velocity_model(fname)
rectangle = Rectangle(bbox)

# Construct mesh sizing object from velocity model
ef = get_sizing_function_from_segy(
    fname,
    bbox,
    hmin=hmin,
    wl=wl,
    freq=freq,
    dt=0.001,
    grade=0.1,
    domain_pad=1e3,
    pad_style="edge",
)

points, cells = generate_mesh(domain=rectangle, edge_length=ef)

if comm.rank == 0:
    meshio.write_points_cells(
        "gm.msh",
        points / 1000,
        [("triangle", cells)],
        file_format="gmsh22",
        binary=False
    )


