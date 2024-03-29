from mpi4py import MPI
import meshio

from SeismicMesh import get_sizing_function_from_segy, generate_mesh, Rectangle
from SeismicMesh.sizing.mesh_size_function import write_velocity_model
comm = MPI.COMM_WORLD

# Name of SEG-Y file containg velocity model.
fname = "Mar2_Vp_1.25m.segy"

# Bounding box describing domain extents (corner coordinates)
bbox = (-3500.0, 0.0, 0., 17000.0)

# Desired minimum mesh size in domain
freq = 7
wl   = 20 # Ne # wl para ordem 2
hmin = 1500/(wl*freq)
write_velocity_model(fname,bbox=bbox,domain_pad=1000, pad_style='edge')
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
    grade=0.15,
    domain_pad=1000,
    pad_style="edge",
)


points, cells = generate_mesh(domain=rectangle, edge_length=ef)

if comm.rank == 0:
    meshio.write_points_cells(
        "mm1.msh",
        points / 1000,
        [("triangle", cells)],
        # file_format="vtk"
        file_format="gmsh22",
        binary=False
    )


