# Explicación para las Actividades

## Actividad A

### 1. Orden ijk (Rendimiento Medio-Bajo)

El bucle interno itera sobre $k$: 

- `C[i * n + j]`: Constante en el bucle interno (excelente).
- `A[i * n + k]`: El índice $k$ varía, por lo que el acceso es secuencial (excelente, aprovecha el caché).
- `B[k * n + j]`: El índice $k$ multiplica a $n$, provocando saltos enormes de tamaño $N$ en memoria (pésimo). Este acceso sufre de constantes cache misses.

### 2. Orden jki (Rendimiento Pésimo)

El bucle interno itera sobre $i$:

- `b_kj (B)`: Constante en el bucle interno (excelente).
- `A[i * n + k]`: El índice $i$ multiplica a $n$, provocando saltos de tamaño $N$ (pésimo).
- `C[i * n + j]`: Igual que $A$, salta de tamaño $N$ en memoria (pésimo). Al escribir y leer saltando, destruye la localidad espacial.

### 3. Orden ikj (El Ganador)

El bucle interno itera sobre $j$:

- `a_ik (A)`: Constante en el bucle interno (excelente).
- `B[k * n + j]`: El índice $j$ varía secuencialmente, accediendo de forma lineal (excelente, aprovecha la cache line perfectamente).
- `C[i * n + j]`: El índice $j$ varía secuencialmente, permitiendo escrituras lineales eficientes (excelente).

## Actividad B

### -O0 (sin optimizar)


### -O2 (redundancias)


### -O3fast (vectorizar y romper asociatividad)


### -march=native 