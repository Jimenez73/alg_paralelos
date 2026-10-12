#!/bin/bash

# Asegurarse de que el binario existe y compilar si es necesario
alg_bin=./bin/alg_1

if [ ! -f "$alg_bin" ]; then
    echo "Compilando alg_1.cpp..."
    g++ -O3 -march=native -fopenmp src/alg_1.cpp -o bin/alg_1
fi

RESULTS_DIR="results"
mkdir -p "$RESULTS_DIR"

csv_file="alg_1.csv"

ARCHIVO_SALIDA="$RESULTS_DIR/$csv_file"

# Escribir el encabezado del archivo CSV
echo "N,p,tiempo_ms,checksum" > "$ARCHIVO_SALIDA"

valores_N=(1024 2048 4096)
valores_p=(1 2 4 8)

echo "Iniciando ejecuciones para el ítem (a) con N=$N..."

for N in "${valores_N[@]}"; do
    for p in "${valores_p[@]}"; do
        # Usar p hilos en la ejecución
        export OMP_NUM_THREADS=$p 
        echo "Ejecutando $alg_bin $N $p..."

        output=$($alg_bin $N)
        tiempo=$(echo "$output" | grep -oP 'tiempo=\K[0-9.]+')
        checksum=$(echo "$output" | grep -oP 'checksum=\K[0-9.]+')
        
        echo "$N,$p,$tiempo,$checksum" >> "$ARCHIVO_SALIDA"
    done
done

echo "¡Listo! Los resultados han sido guardados en $ARCHIVO_SALIDA"
