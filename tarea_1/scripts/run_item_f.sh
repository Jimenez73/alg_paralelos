#!/bin/bash

RESULTS_DIR="results"
ARCHIVO_SALIDA="$RESULTS_DIR/resultados_item_f.csv"

mkdir -p "$RESULTS_DIR"

# Crear el encabezado del archivo CSV
echo "version,p,t,tiempo" > $ARCHIVO_SALIDA

# Definir el límite lógico de núcleos
P_MAX=12
CARPETA="src"

echo "Iniciando experimentos..."

# Recorrer todos los archivos .py en la carpeta
for archivo in "$CARPETA"/*.py; do

    # Verificar si el archivo existe (por si no hay archivos .py)
    if [ -f "$archivo" ]; then
    
        # Saltar config.py
        nombre_base=$(basename "$archivo")
        if [ "$nombre_base" = "config.py" ]; then
            echo "Saltando: $nombre_base (Excluido)"
            continue
        fi

        for p in $(seq 1 $P_MAX); do
            echo "Ejecutando $nombre_base con p=$p..."
            python $archivo -p $p >> $ARCHIVO_SALIDA
        done
    fi
done



echo "Experimentos finalizados. Resultados guardados en $ARCHIVO_SALIDA"




