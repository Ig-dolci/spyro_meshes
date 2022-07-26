import numpy as np
import segyio
spec = segyio.spec()
filename = "helloworld.segy"
a = np.zeros((100, 100)) + 5000.0
spec.sorting = 2
spec.format = 1
spec.samples = range(100)
spec.ilines = range(100)
spec.xlines = range(100)
with segyio.create(filename, spec) as f:
    for tr, il in enumerate(spec.ilines):
        f.trace[tr] = a[:, tr]