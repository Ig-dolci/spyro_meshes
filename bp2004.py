from mpi4py import MPI
import meshio

from SeismicMesh import get_sizing_function_from_segy, generate_mesh, Rectangle

comm = MPI.COMM_WORLD

"""
Build a mesh of the BP2004 benchmark velocity model in serial or parallel
Takes roughly 1 minute with 2 processors and less than 1 GB of RAM.
"""

# Name of SEG-Y file containg velocity model.
fname = "vel_z6.25m_x12.5m_exact.segy"

# Bounding box describing domain extents (corner coordinates)
bbox = (-12000.0, 0.0, 0.0, 67000.0)

# Desired minimum mesh size in domain
hmin = 75.0

rectangle = Rectangle(bbox)

# Construct mesh sizing object from velocity model
ef = get_sizing_function_from_segy(
    fname,
    bbox,
    hmin=hmin,
    wl=10,
    freq=2,
    dt=0.001,
    grade=0.15,
    domain_pad=1e3,
    pad_style="edge",
)

points, cells = generate_mesh(domain=rectangle, edge_length=ef)

if comm.rank == 0:
    # Write the mesh in a vtk format for visualization in ParaView
    # NOTE: SeismicMesh outputs assumes the domain is (z,x) so for visualization
    # in ParaView, we swap the axes so it appears as in the (x,z) plane.
    meshio.write_points_cells(
        "BP2004.vtk",
        points[:, [1, 0]] / 1000,
        [("triangle", cells)],
        file_format="vtk",
    )