#!/bin/bash

RESULTS_DIR="results"
mkdir -p "$RESULTS_DIR"

csv_file="alg_3.csv"

ARCHIVO_SALIDA="$RESULTS_DIR/$csv_file"

# Escribir el encabezado del archivo CSV
echo "N,p,tiempo_ms,checksum" > "$ARCHIVO_SALIDA"

valores_N=(1024 2048 4096)
valores_p=(1 2 4 8)

echo "Iniciando ejecuciones para el ítem (a) con N=$N..."

for N in "${valores_N[@]}"; do
    for p in "${valores_p[@]}"; do
        echo "Ejecutando src/alg_3.py $N $p..."
        python src/alg_3.py -N $N -p $p >> $ARCHIVO_SALIDA
    done
done

echo "¡Listo! Los resultados han sido guardados en $ARCHIVO_SALIDA"
