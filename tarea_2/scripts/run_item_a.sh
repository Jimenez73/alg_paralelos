#!/bin/bash

# Asegurarse de que el binario existe y compilar si es necesario
serial_bin=./bin/serial

if [ ! -f "$serial_bin" ]; then
    echo "Compilando serial.cpp..."
    g++ -O3 -march=native src/serial.cpp -o bin/serial
fi

RESULTS_DIR="results"
mkdir -p "$RESULTS_DIR"

csv_file="item_a.csv"

ARCHIVO_SALIDA="$RESULTS_DIR/$csv_file"

# Escribir el encabezado del archivo CSV
echo "N,n,tiempo_ms,checksum" > "$ARCHIVO_SALIDA"

N=2048
# Valores de n especificados en el ítem (a)
valores_n=(2048 1024 512 256 128 64 32)

echo "Iniciando ejecuciones para el ítem (a) con N=$N..."

for n in "${valores_n[@]}"; do
    echo "Ejecutando $serial_bin $N $n..."
    # Ejecutar y capturar la salida
    output=$($serial_bin $N $n)
    
    # Extraer los valores numéricos usando expresiones regulares (grep)
    # Formato esperado: N=2048 n=256 tiempo=12.34 ms checksum=56.789000
    tiempo=$(echo "$output" | grep -oP 'tiempo=\K[0-9.]+')
    checksum=$(echo "$output" | grep -oP 'checksum=\K[0-9.]+')
    
    # Agregar los datos extraídos al archivo CSV
    echo "$N,$n,$tiempo,$checksum" >> "$ARCHIVO_SALIDA"
done

echo "¡Listo! Los resultados han sido guardados en $ARCHIVO_SALIDA"
