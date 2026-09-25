import numpy as np
from joblib import Parallel, delayed
from threadpoolctl import threadpool_limits

import argparse
import time
import psutil
import threading

from config import N, K, B

porcentajes_cpu = []
monitoreando = False

def registrar_cpu():
    # Revisa la CPU cada 0.1 segundos
    while monitoreando:
        porcentajes_cpu.append(psutil.cpu_percent(interval=0.1))

rng = np.random.default_rng(42)

beta_real = rng.standard_normal(K+1)
datos = rng.standard_normal(size=(N, K))

X = np.insert(datos, 0, 1, axis=1)
y = X @ beta_real + rng.standard_normal(N)


def ajustar_un_resample_numpy(X, y, random_seed):
    rng = np.random.default_rng(random_seed)

    # 1. Sortear índices y calcular frecuencias (pesos)
    indices = rng.choice(N, size=N, replace=True)
    pesos = np.bincount(indices, minlength=N)
    
    # 2. Convertir pesos a formato de columna (N, 1) para broadcasting
    pesos_col = pesos[:, np.newaxis]
    
    # 3. Aplicar pesos a X e y (equivale a la matriz W)
    # X_w tiene la misma dimensión que X, pero cada fila está multiplicada por su peso
    X_w = X * pesos_col 
    y_w = y * pesos
    
    # 4. Resolver el sistema de ecuaciones normales ponderado
    A = X.T @ X_w
    B = X.T @ y_w
    beta_b = np.linalg.solve(A, B)
    
    return beta_b


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="Número de procesos")
    parser.add_argument("-t", type=int, default=12, help="Número de threads por proceso")
    parser.add_argument("-cpu", type=bool, default=False, help="Imprimir uso de CPU")
    args = parser.parse_args()

    if args.cpu:
        monitoreando = True

    hilo_monitor = threading.Thread(target=registrar_cpu)
    hilo_monitor.start()

    semillas_base = np.random.SeedSequence(42).generate_state(B)

    with threadpool_limits(limits=args.t):  # Limitar los threads de NumPy
        inicio = time.perf_counter()        # Medir solo la sección paralela
        
        betas_bootstrap = Parallel(n_jobs=args.p)(
            delayed(ajustar_un_resample_numpy)(X, y, semillas_base[i]) for i in range(B)
        )
        
        fin = time.perf_counter()

    tiempo_total = fin - inicio

    monitoreando = False
    hilo_monitor.join()

    # Intervalo de confianza
    betas_array = np.array(betas_bootstrap)

    limite_inferior = np.percentile(betas_array, 2.5, axis=0)
    limite_superior = np.percentile(betas_array, 97.5, axis=0)

    porcentaje = np.mean((beta_real >= limite_inferior) & (beta_real <= limite_superior)) * 100

    # Imprimir el resultado en formato CSV para que el orquestador lo guarde
    resultados = f"bs_numpy,{args.p},{args.t},{tiempo_total},{porcentaje:.2f}"

    if args.cpu:
        resultados += f',"{porcentajes_cpu}"' # Porcentaje de CPU usado en intervalos de 0.1s

    print(resultados)