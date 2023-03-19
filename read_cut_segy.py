import segyio
import numpy as np
from scipy.ndimage import gaussian_filter
case = "elastic"
deltax = deltaz = 1.25
x_max = 17000.0
y1 = 3500.0
x0 = 5000.0
x1 = 15000.0
y0 = 500
if case == "acoustic":
    with segyio.open('Mar2_Vp_1.25m.segy') as segyfile:
        vp_file = segyio.tools.cube(segyfile)[0, :, :]
    vp = vp_file[int(x0*deltax):int(x1*deltax)][:]
    np.save("mm_vp.npy", vp)
    vini = gaussian_filter(vp, sigma=100)
    np.save("mm_vp_guess.npy", vini)
    
else:
    with segyio.open('vp_mm.segy') as segyfile:
        vp_file = segyio.tools.cube(segyfile)[0, :, int(y0/deltax):int(y1/deltax)]
    print(len(vp_file), len(vp_file[0]))
    with segyio.open('vs_mm.segy') as segyfile:
        vs_file = segyio.tools.cube(segyfile)[0, :, int(y0/deltax):int(y1/deltax)]    
    with segyio.open('density_mm.segy') as segyfile:
        density_file = segyio.tools.cube(segyfile)[0, :, int(y0/deltax):int(y1/deltax)]
    vp = vp_file[int(x0/deltax):int(x1/deltax)][:]
    vs = vs_file[int(x0/deltax):int(x1/deltax)][:]
    print(int(y0/deltax))
    density = density_file[int(x0/deltax):int(x1/deltax)][:]
    # mu = vs*vs*density
    # print(np.amin(mu), np.amax(mu))
    vp_guess = gaussian_filter(vp, sigma=100)
    vs_guess = gaussian_filter(vs, sigma=100)
    np.save("mm_vp_guess.npy", vp_guess)
    np.save("mm_vs_guess.npy", vs_guess)
    np.save("mm_vp.npy", vp)
    np.save("mm_vs.npy", vs)
    np.save("rho.npy", density)