#!/bin/bash

RESULTS_DIR="results"
ARCHIVO_SALIDA="$RESULTS_DIR/resultados_i.csv"

mkdir -p "$RESULTS_DIR"

# Crear el encabezado del archivo CSV
echo "version,p,t,tiempo" > $ARCHIVO_SALIDA

# Definir el límite lógico de núcleos
P_MAX=12

echo "Iniciando experimentos..."

# Iterar sobre procesos y threads
for p in $(seq 1 $P_MAX); do
    for t in $(seq 1 $P_MAX); do
        
        # Validar la restricción p * t <= p_max[cite: 1]
        if (( p * t <= P_MAX )); then
            echo "Ejecutando con p=$p, t=$t..."
            python src/bs_numpy.py -p $p -t $t >> $ARCHIVO_SALIDA
        fi
        
    done
done

echo "Experimentos finalizados. Resultados guardados en $ARCHIVO_SALIDA"