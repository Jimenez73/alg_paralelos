from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

all_ranks = np.empty(size, dtype='i')  # Arreglo para almacenar todos los rangos
all_ranks[rank] = rank                 # Cada proceso guarda su propio rango
my_rank = np.array([rank], dtype='i')

# Iniciar todas las recepciones y envios no bloqueantes
requests = []
for i in range(size):
    if i != rank:
        requests.append(comm.Irecv(all_ranks[i:i+1], source=i, tag=0))
        requests.append(comm.Isend(my_rank, dest=i, tag=0))

# Esperar a que todas las operaciones terminen
MPI.Request.Waitall(requests)

print(f"Proceso {rank} tiene los rangos: {all_ranks}")
