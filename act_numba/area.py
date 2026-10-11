import numpy as np
import time
from numba import njit, prange, set_num_threads

N = 8
set_num_threads(N)

XMIN = -2
XMAX = 0.5

YMIN = -1.25
YMAX = 1.25

BOX_AREA = (XMAX-XMIN) * (YMAX-YMIN)

@njit
def in_mandelbrot(cx, cy, max_iter):
    x = 0.0
    y = 0.0
    for i in range(max_iter):
        x2 = x * x
        y2 = y * y
        if x2 + y2 > 4.0:
            return False
        
        y = 2.0 * x * y + cy
        x = x2 - y2 + cx

    return True

@njit(parallel=True)
def mandelbrot_area(n, max_iter):
    count = 0
    for i in prange(n):
        cx = XMIN + (XMAX - XMIN) * np.random.random()
        cy = YMIN + (YMAX - YMIN) * np.random.random()
        if in_mandelbrot(cx, cy, max_iter):
            count += 1

    return BOX_AREA * count / n


if __name__ == "__main__":
    inicio = time.perf_counter()
    area = mandelbrot_area(n=1_000_000, max_iter=5_000) # Valores recomendados por el profe
    fin = time.perf_counter()

    tiempo_total = fin - inicio
    # print(f"Área: {area:.4f}\nTiempo: {tiempo_total:.4f}")
    print(f"{N}: {tiempo_total:4f}")

# Resultados

# Sin uso de nada:
    # Muy lento!!
    
# Con @njit 
    # Área: 1.5093
    # Tiempo: 8.5057

# Con @njit(parallel=True) y prange
    # Área: 1.5046
    # Tiempo: 2.4924
