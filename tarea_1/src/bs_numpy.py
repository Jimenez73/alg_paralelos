import argparse
import time
import numpy as np
from joblib import Parallel, delayed
from threadpoolctl import threadpool_limits

from config import N, K, B

rng = np.random.default_rng(42)

beta_real = rng.standard_normal(K+1)
datos = rng.standard_normal(size=(N, K))

X = np.insert(datos, 0, 1, axis=1)
y = X @ beta_real + rng.standard_normal(N)


def ajustar_un_resample_numpy(X, y, random_seed):
    rng = np.random.default_rng(random_seed)

    indices = rng.choice(N, size=N, replace=True)
    X_b = X[indices]
    y_b = y[indices]

    A = X_b.T @ X_b
    B = X_b.T @ y_b
    beta_b = np.linalg.solve(A, B)
    
    return beta_b

if __name__ == "__main__":
    # 1. Configurar la recepción de argumentos p y t
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="Número de procesos")
    parser.add_argument("-t", type=int, default=12, help="Número de threads por proceso")
    args = parser.parse_args()

    semillas_base = np.random.SeedSequence(42).generate_state(B)

    # 2. Limitar los threads de NumPy y medir solo la sección paralela
    with threadpool_limits(limits=args.t):
        inicio = time.perf_counter()
        
        betas_bootstrap = Parallel(n_jobs=args.p)(
            delayed(ajustar_un_resample_numpy)(X, y, semillas_base[i]) for i in range(B)
        )
        
        fin = time.perf_counter()

    tiempo_total = fin - inicio

    # 3. Imprimir el resultado en formato CSV para que el orquestador lo guarde
    print(f"bs_numpy,{args.p},{args.t},{tiempo_total}")