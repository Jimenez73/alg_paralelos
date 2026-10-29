import sys
import time
import numpy as np
from numba import njit

G = 1.0
EPS = 0.1  # suavizado: evita fuerzas muy grandes cuando dos particulas se acercan
dt = 5e-3


@njit
def aceleraciones(pos, m):
    n = pos.shape[0]
    acc = np.zeros((n, 2))
    for i in range(n):
        for j in range(n):
            if j != i:
                dx = pos[j, 0] - pos[i, 0]
                dy = pos[j, 1] - pos[i, 1]
                r2 = dx * dx + dy * dy + EPS * EPS
                f = G * m[j] / (r2 * np.sqrt(r2))
                acc[i, 0] += f * dx
                acc[i, 1] += f * dy
    return acc


@njit
def energia(pos, vel, m):
    n = pos.shape[0]
    e = 0.0
    for i in range(n):
        e += 0.5 * m[i] * (vel[i, 0] ** 2 + vel[i, 1] ** 2)
        for j in range(n):
            if j != i:
                dx = pos[j, 0] - pos[i, 0]
                dy = pos[j, 1] - pos[i, 1]
                e -= 0.5 * G * m[i] * m[j] / np.sqrt(dx * dx + dy * dy + EPS * EPS)
    return e


def galaxia(n, centro, velocidad, rng):
    r = 0.2 + 0.8 * rng.random(n)
    theta = 2 * np.pi * rng.random(n)
    v = np.sqrt(G / r)
    pos = np.column_stack((r * np.cos(theta), r * np.sin(theta)))
    vel = np.column_stack((-v * np.sin(theta), v * np.cos(theta)))
    pos[0] = 0.0
    vel[0] = 0.0
    m = np.full(n, 0.1 / n)
    m[0] = 1.0
    return pos + centro, vel + velocidad, m


def condicion_inicial(n):
    rng = np.random.default_rng(0)
    pos1, vel1, m1 = galaxia(n // 2, [-2.0, -0.7], [0.25, 0.0], rng)
    pos2, vel2, m2 = galaxia(n - n // 2, [2.0, 0.7], [-0.25, 0.0], rng)
    return np.vstack((pos1, pos2)), np.vstack((vel1, vel2)), np.concatenate((m1, m2))


def simular(pos, vel, m, pasos, cada):
    frames = []
    acc = aceleraciones(pos, m)
    for k in range(pasos):
        vel += 0.5 * dt * acc
        pos += dt * vel
        acc = aceleraciones(pos, m)
        vel += 0.5 * dt * acc
        if k % cada == 0:
            frames.append(pos.copy())
    return energia(pos, vel, m), frames


if __name__ == "__main__":
    n = int(sys.argv[1])
    pasos = int(sys.argv[2])

    pos, vel, m = condicion_inicial(n)

    aceleraciones(pos, m)
    e0 = energia(pos, vel, m)

    t0 = time.perf_counter()
    e, frames = simular(pos, vel, m, pasos, 20)
    elapsed = time.perf_counter() - t0

    np.save("frames.npy", np.array(frames))
    print(f"serial, n={n}, pasos={pasos}, dE/E={abs((e - e0) / e0):.2e}, tiempo={elapsed:.4f}")
