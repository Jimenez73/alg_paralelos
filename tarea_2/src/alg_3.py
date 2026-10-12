import numpy as np
from numba import njit, prange, set_num_threads
import time
import os
import argparse

@njit
def init_matrix(N, offset):
    M = np.empty((N, N), dtype=np.float64)
    for i in range(N):
        for j in range(N):
            M[i, j] = np.sin(i * 0.1 + j * 0.3 + offset)
    return M

@njit(parallel=True)
def multiply_numba(A, B, N):
    C = np.zeros((N, N), dtype=np.float64)
    for i in prange(N):
        for k in range(N):
            a = A[i, k]
            for j in range(N):
                C[i, j] += a * B[k, j]
    return C


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-N", type=int, default=2048, help="Tamaño de las matrices")
    parser.add_argument("-p", type=int, default=1, help="Cantidad de hilos")
    args = parser.parse_args()
    
    set_num_threads(args.p)
    
    # 1. Warm-up
    A_warm = init_matrix(2, 1.0)
    B_warm = init_matrix(2, 2.0)
    _ = multiply_numba(A_warm, B_warm, 2)

    # 2. Inicialización real
    A = init_matrix(args.N, 1.0)
    B = init_matrix(args.N, 2.0)

    # 3. Medición del tiempo
    t0 = time.time()
    C = multiply_numba(A, B, args.N)
    t1 = time.time()

    ms = (t1 - t0) * 1000.0
    checksum = np.sum(C)

    # N,p,tiempo(ms),checksum
    print(f"{args.N},{args.p},{ms:.2f},{checksum:.6f}")