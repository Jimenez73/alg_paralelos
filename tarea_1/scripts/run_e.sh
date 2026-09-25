#!/bin/bash

RESULTS_DIR="results"
ARCHIVO_SALIDA="$RESULTS_DIR/resultados_e.csv"

mkdir -p "$RESULTS_DIR"

# Crear el encabezado del archivo CSV
echo "version,p,t,tiempo,porcentaje,uso_cpu" > $ARCHIVO_SALIDA

# Definir el límite lógico de núcleos
P_MAX=12

echo "Iniciando experimentos..."

# Iterar sobre procesos y threads
for p in $(seq 1 $P_MAX); do
    echo "Ejecutando con p=$p"
    python src/bs_numpy.py -p $p -cpu true >> $ARCHIVO_SALIDA
done

echo "Experimentos finalizados. Resultados guardados en $ARCHIVO_SALIDA"s