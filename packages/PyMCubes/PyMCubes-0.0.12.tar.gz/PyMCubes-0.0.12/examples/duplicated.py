
import numpy as np
import mcubes

# def sphere(x, y, z):
#     return np.sqrt((x - 4)**2 + (y - 4)**2 + (z - 4)**2) - 4

# # d = (9-2)/19

# # lower = (2, 2, 9-6*d)
# # upper = (2+2*d, 2+2*d, 9)

# vertices, triangles = mcubes.marching_cubes_func((2, 2, 2), (9, 9, 9), 20, 20, 20, sphere, 0)
# # vertices, triangles = mcubes.marching_cubes_func(lower, upper, 3, 3, 7, sphere, 0)

# import IPython
# IPython.embed()

# test = np.random.randint(0, 10, (5, 10, 2)) == 0
x, y, z = np.mgrid[:2, :2, :2]
test = (x + y + z) % 2
vert, tri = mcubes.marching_cubes(test, 0.5)

print(len(vert))
print(len(np.unique(vert, axis=0)))
print(len(tri))

print(tri)

mcubes.export_obj(vert, tri, "duplicate.obj")
