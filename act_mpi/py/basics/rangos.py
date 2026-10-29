from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

all_ranks = np.empty(size, dtype='i')  # Arreglo para almacenar todos los rangos
all_ranks[rank] = rank                 # Cada proceso guarda su propio rango
my_rank = np.array([rank], dtype='i')

# Cada proceso envia su rango a todos los demas
for i in range(size):
    if i != rank:
        comm.Send(my_rank, dest=i, tag=0)

# Cada proceso recibe el rango de todos los demas
for i in range(size):
    if i != rank:
        comm.Recv(all_ranks[i:i+1], source=i, tag=0)

print(f"Proceso {rank} tiene los rangos: {all_ranks}")
