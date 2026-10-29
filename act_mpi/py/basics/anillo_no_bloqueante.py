from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = 1_000_000
next = (rank + 1) % size
prev = (rank - 1) % size

a = np.full(N, rank, dtype='d')
b = np.empty(N, dtype='d')

reqs = [comm.Irecv(b, source=prev, tag=0),
        comm.Isend(a, dest=next, tag=0)]
MPI.Request.Waitall(reqs)

print(f"Proceso {rank} recibió datos del proceso {int(b[0])}")
