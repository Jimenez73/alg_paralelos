import argparse
import time
import numpy as np
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import LinearRegression

from config import N, K, B

rng = np.random.default_rng(42)

beta_real = rng.standard_normal(K+1)
datos = rng.standard_normal(size=(N, K))

X = np.insert(datos, 0, 1, axis=1)
y = X @ beta_real + rng.standard_normal(N)

if __name__ == "__main__":
    # 1. Configurar la recepción de argumentos p y t
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="Número de procesos")
    args = parser.parse_args()

    semillas_base = np.random.SeedSequence(42).generate_state(B)

    # 2. Limitar los threads de NumPy y medir solo la sección paralela
    inicio = time.perf_counter()
    
    base_model = LinearRegression(fit_intercept=False)
    bagging_model = BaggingRegressor(
        estimator=base_model, 
        n_estimators=B, 
        n_jobs=args.p,
        bootstrap=True,
        random_state=42
    )
    bagging_model.fit(X, y)
    
    fin = time.perf_counter()

    tiempo_total = fin - inicio

    # Intervalo de confianza
    betas_bootstrap = np.array([model.coef_ for model in bagging_model.estimators_])
    
    limite_inferior = np.percentile(betas_bootstrap, 2.5, axis=0)
    limite_superior = np.percentile(betas_bootstrap, 97.5, axis=0)

    porcentaje = np.mean((beta_real >= limite_inferior) & (beta_real <= limite_superior)) * 100

    # 3. Imprimir el resultado en formato CSV para que el orquestador lo guarde
    print(f"bs_auto,{args.p},,{tiempo_total},{porcentaje:.2f}")