import Basis
import numpy as np
import matplotlib.pyplot as plt

basis = Basis.Basis(np.array([[2.25, 1.1, 1.1], [2.3, 2.2, 9.4], [0.3, 2.0, 2.4]]))

print(f"The orthogonalization of basis\n{basis.basis} is\n{basis.orthogonol()}")
print(f"The orthonormalization of basis\n{basis.basis} is\n{basis.orthonormal()}")

fig = plt.figure(figsize=(8, 8))
ax = plt.subplot(projection="3d")
for v in basis.basis:
    ax.quiver(0, 0, 0, v[0], v[1], v[2], arrow_length_ratio=0.1)
for v in basis.orthonormal():
    ax.quiver(0, 0, 0, v[0], v[1], v[2], arrow_length_ratio=0.1, color="r")
v = basis.orthonormal()

# only use in 3d vecorts
ax.set_xlim((-2, 2))
ax.set_ylim((-2, 2))
ax.set_zlim((-2, 2))
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.show()