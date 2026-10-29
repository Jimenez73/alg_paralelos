import sys
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
next = (rank + 1) % size
prev = (rank - 1) % size

a = np.full(N, rank, dtype='d')
b = np.empty(N, dtype='d')

# Quiz 11, solucion b): el proceso 0 recibe primero y rompe el ciclo de espera.
if rank == 0:
    comm.Recv(b, source=prev, tag=0)
    comm.Send(a, dest=next, tag=0)
else:
    comm.Send(a, dest=next, tag=0)
    comm.Recv(b, source=prev, tag=0)

print(f"Proceso {rank} recibio datos del proceso {int(b[0])}")
