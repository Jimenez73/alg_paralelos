import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

frames = np.load("frames.npy")

fig, ax = plt.subplots(figsize=(5, 5))
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect("equal")
puntos = ax.scatter(frames[0, :, 0], frames[0, :, 1], s=1)


def actualizar(k):
    puntos.set_offsets(frames[k])
    return (puntos,)


anim = FuncAnimation(fig, actualizar, frames=len(frames), interval=50)
anim.save("nbody.gif", writer="pillow")
