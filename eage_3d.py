from mpi4py import MPI
import meshio

from SeismicMesh import get_sizing_function_from_segy, generate_mesh, Rectangle
from SeismicMesh.sizing.mesh_size_function import write_velocity_model
comm = MPI.COMM_WORLD

# Name of SEG-Y file containg velocity model.
fname = "overthrust.vites"

# Bounding box describing domain extents (corner coordinates)
bbox = (-4.5,0.0, 0.0, 20.0, 0.0, 20.0)


# Desired minimum mesh size in domain
freq = 7
wl   = 2.0 # Ne # wl para ordem 2
hmin = 1500/(wl*freq)
write_velocity_model(fname,bbox=bbox,
domain_pad=0, pad_style='edge', nx=801, ny=801, nz=187, byte_order='little')

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
    grade=0.2,
    domain_pad=0,
    pad_style="edge",
    nx=801, ny=801, nz=187, byte_order='little'
)


points, cells = generate_mesh(domain=rectangle, edge_length=ef)

if comm.rank == 0:
    meshio.write_points_cells(
        "seam.msh",
        points ,
        [("tetra", cells)],
        file_format="gmsh22",
        binary=False
    )


