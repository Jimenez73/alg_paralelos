#!/usr/bin/env bash
# Uso: ./scripts/run_perf_all.sh <directorio_bin> [<n1> <n2> ...]

BINDIR="${1:?Uso: $0 <directorio_bin> [n1 n2 ...]}"
shift

# Usamos los mismos tamaños por defecto que en run_timing.sh
SIZES=(${@:-64 256 1024 2048})

RESULTS_DIR="results"
CSV="$RESULTS_DIR/perf_stats.csv"

mkdir -p "$RESULTS_DIR"

# Preparamos el encabezado del archivo CSV
if [[ ! -f "$CSV" ]]; then
    echo "kernel,n,bindir,instructions,cycles,cache-references,cache-misses" > "$CSV"
fi

for KERNEL in "$BINDIR"/*; do
    [[ -x "$KERNEL" ]] || continue
    NAME="$(basename "$KERNEL")"
    
    for N in "${SIZES[@]}"; do
        echo -n "  $NAME (perf) n=$N ... "
        
        # Archivo temporal para guardar la salida de perf
        TMP_PERF=$(mktemp)
        
        # Ejecutamos perf stat.
        # > /dev/null ignora la salida normal del programa (el print del checksum).
        # 2> "$TMP_PERF" redirige los resultados de perf al archivo temporal.
        perf stat -e instructions,cycles,cache-references,cache-misses "$KERNEL" "$N" > /dev/null 2> "$TMP_PERF"
        
        # Extraemos los valores.
        # awk '{print $1}' toma la primera columna (el número).
        # tr -d ',' elimina las comas de los miles para que el CSV sea un número puro.
        INS=$(grep "instructions" "$TMP_PERF" | awk '{print $1}' | tr -d ',' | tr -d '.')
        CYC=$(grep "cycles" "$TMP_PERF" | awk '{print $1}' | tr -d ',' | tr -d '.')
        REF=$(grep "cache-references" "$TMP_PERF" | awk '{print $1}' | tr -d ',' | tr -d '.')
        MISS=$(grep "cache-misses" "$TMP_PERF" | awk '{print $1}' | tr -d ',' | tr -d '.')
        
        # Guardamos en el CSV
        echo "$NAME,$N,$BINDIR,$INS,$CYC,$REF,$MISS" >> "$CSV"
        echo "Listo"
        
        # Borramos el temporal
        rm "$TMP_PERF"
    done
done

echo "Resultados acumulados en $CSV"