import argparse
import time
import numpy as np
from sklearn.linear_model import LinearRegression
from joblib import Parallel, delayed

from config import N, K, B

rng = np.random.default_rng(42)

beta_real = rng.standard_normal(K+1)
datos = rng.standard_normal(size=(N, K))

X = np.insert(datos, 0, 1, axis=1)
y = X @ beta_real + rng.standard_normal(N)

def ajustar_un_resample(X, y, random_seed):
    rng = np.random.default_rng(random_seed)

    indices = rng.choice(N, size=N, replace=True)
    X_b = X[indices]
    y_b = y[indices]

    modelo = LinearRegression(fit_intercept=False)
    modelo.fit(X_b, y_b)

    return modelo.coef_

if __name__ == "__main__":
    # 1. Configurar la recepción de argumentos p y t
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="Número de procesos")
    args = parser.parse_args()

    semillas_base = np.random.SeedSequence(42).generate_state(B)

    # 2. Limitar los threads de NumPy y medir solo la sección paralela
    inicio = time.perf_counter()
    
    betas_bootstrap = Parallel(n_jobs=args.p)(
        delayed(ajustar_un_resample)(X, y, semillas_base[i]) for i in range(B)
    )
    
    fin = time.perf_counter()

    tiempo_total = fin - inicio

    # 3. Imprimir el resultado en formato CSV para que el orquestador lo guarde
    print(f"bs_sklearn,{args.p},,{tiempo_total}")