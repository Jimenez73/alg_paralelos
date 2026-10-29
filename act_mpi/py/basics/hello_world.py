#!/usr/bin/env python3
"""
Ejemplo Hello World: Primer programa con mpi4py

El ejemplo más simple de MPI: cada proceso imprime su rango.

Uso: mpirun -n 4 python3 hello_world.py
"""

from mpi4py import MPI

# Obtener el comunicador global
comm = MPI.COMM_WORLD

# Obtener el rango y tamaño
rank = comm.Get_rank()
size = comm.Get_size()

# Cada proceso imprime un mensaje
print(f"Hola desde el proceso {rank} de {size}")
