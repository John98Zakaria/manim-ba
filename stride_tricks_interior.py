import numpy as np
from numpy.lib.stride_tricks import as_strided

a = np.ones((5, 5), dtype=np.uint8)
a[1:-1, 1:-1] = 10

print(as_strided(a, (5, 2), (5, 4)))
