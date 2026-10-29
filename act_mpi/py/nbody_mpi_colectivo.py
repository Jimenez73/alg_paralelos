import sys
import time
import numpy as np
from numba import njit
from mpi4py import MPI

G = 1.0
EPS = 0.1  # suavizado: evita fuerzas muy grandes cuando dos particulas se acercan
dt = 5e-3


# La función pasa de calcular la acelaración de todo el sistema a solo rango de particulas
@njit
def aceleraciones_local(pos, m, inicio, fin):
    n = pos.shape[0]
    n_local = fin - inicio
    acc = np.zeros((n_local, 2))    # Inicializa con n_local

    for i in range(n_local):
        global_i = inicio + i
        for j in range(n):
            if j != global_i:
                dx = pos[j, 0] - pos[global_i, 0]   # Accede a las posiciones globales
                dy = pos[j, 1] - pos[global_i, 1]
                r2 = dx * dx + dy * dy + EPS * EPS
                f = G * m[j] / (r2 * np.sqrt(r2))
                acc[i, 0] += f * dx                 # Pero guarda las aceleraciones localmente
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


def simular_mpi_colectivas(pos, vel, m, pasos, cada, inicio, fin, comm, rank, size):
    frames = []
    acc_local = aceleraciones_local(pos, m, inicio, fin)
    vel_local = vel[inicio:fin].copy() # Extraer segmento local

    for k in range(pasos):
        # 1. Medio paso de velocidad y paso completo de posición local
        vel_local += 0.5 * dt * acc_local
        pos[inicio:fin] += dt * vel_local

        # 2. Operación colectiva: Sincronizar las posiciones globales
        # Usamos ascontiguousarray porque mpi4py requiere buffers contiguos en memoria
        sendbuf = np.ascontiguousarray(pos[inicio:fin])
        comm.Allgather(sendbuf, pos)

        # 3. Nuevas aceleraciones con el 'pos' global actualizado
        acc_local = aceleraciones_local(pos, m, inicio, fin)    # Actualizo solo lo que me dijeron
        vel_local += 0.5 * dt * acc_local

        if k % cada == 0 and rank == 0:
            frames.append(pos.copy())


    # === RECOLECCIÓN FINAL DE VELOCIDADES ===
    # Solo el rank 0 necesita el arreglo completo de velocidades
    vel_final = np.zeros_like(vel) if rank == 0 else None

    sendbuf_vel = np.ascontiguousarray(vel_local)
    comm.Gather(sendbuf_vel, vel_final, root=0)

    # Solo un proceso retorna toda la información
    if rank == 0:
        e_final = energia(pos, vel_final, m)
        return e_final, frames
    
    else:
        return None, None

if __name__ == "__main__":
    n     = int(sys.argv[1])
    pasos = int(sys.argv[2])

    pos, vel, m = condicion_inicial(n)

    # Compilar
    aceleraciones_local(pos, m, 0, n)

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Calcular índices locales para este proceso
    local_n = n // size
    inicio = rank * local_n
    fin = inicio + local_n

    # Solo el rank 0 calcula la energía inicial e0
    if rank == 0:
        e0 = energia(pos, vel, m)

    # Sincronizar todos antes de tomar el tiempo inicial
    comm.Barrier()
    t0 = time.perf_counter()

    # Ejecutar simulación
    e, frames = simular_mpi_colectivas(pos, vel, m, pasos, 20, inicio, fin, comm, rank, size)

    # Sincronizar antes de calcular el tiempo total
    comm.Barrier()
    elapsed = time.perf_counter() - t0

    # Solo el rank 0 imprime los resultados y guarda el archivo
    if rank == 0:
        np.save("frames.npy", np.array(frames))
        print(f"MPI_colectivas, n={n}, pasos={pasos}, dE/E={abs((e - e0) / e0):.2e}, tiempo={elapsed:.4f}, p={size}")
