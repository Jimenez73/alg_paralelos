import numpy as np
import time

XMIN = -2.0
XMAX = 0.5
YMIN = -1.25
YMAX = 1.25
BOX_AREA = (XMAX - XMIN) * (YMAX - YMIN)

def mandelbrot_area_numpy(n, max_iter):
    # 1. Generar todos los puntos simultáneamente (vectorización pura)
    cx = np.random.uniform(XMIN, XMAX, n)
    cy = np.random.uniform(YMIN, YMAX, n)
    
    x = np.zeros(n)
    y = np.zeros(n)
    
    # Máscara para rastrear qué puntos no han escapado (True = dentro)
    active = np.ones(n, dtype=bool)
    
    for _ in range(max_iter):
        # Extraer solo los valores que siguen activos en esta iteración
        x_act = x[active]
        y_act = y[active]
        
        x2 = x_act * x_act
        y2 = y_act * y_act
        
        # Determinar cuáles de los activos se mantienen dentro del límite
        keep = (x2 + y2) <= 4.0
        
        # Actualizar la máscara global para desactivar los que recién escaparon
        active[active] = keep
        
        # Romper el ciclo si ya no queda ningún punto dentro del límite
        if not active.any():
            break
            
        # Calcular los nuevos x e y EXCLUSIVAMENTE para los puntos que sobrevivieron
        y[active] = 2.0 * x_act[keep] * y_act[keep] + cy[active]
        x[active] = x2[keep] - y2[keep] + cx[active]
        
    count = active.sum()
    return BOX_AREA * count / n

if __name__ == "__main__":
    inicio = time.perf_counter()
    area = mandelbrot_area_numpy(n=1_000_000, max_iter=5_000)
    fin = time.perf_counter()

    tiempo_total = fin - inicio
    print(f"Área (NumPy): {area:.4f}\nTiempo (NumPy): {tiempo_total:.4f}")

# Área (NumPy): 1.5094
# Tiempo (NumPy): 155.5082
