#include <iostream>
#include <vector>
#include <mpi.h>

int main(int argc, char** argv) {
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    std::vector<int> all_ranks(size);  // Arreglo para almacenar todos los rangos
    all_ranks[rank] = rank;            // Cada proceso guarda su propio rango

    // Cada proceso envia su rango a todos los demas
    for (int i = 0; i < size; i++) {
        if (i != rank) {
            MPI_Send(&rank, 1, MPI_INT, i, 0, MPI_COMM_WORLD);
        }
    }

    // Cada proceso recibe el rango de todos los demas
    for (int i = 0; i < size; i++) {
        if (i != rank) {
            MPI_Recv(&all_ranks[i], 1, MPI_INT, i, 0,
                     MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
    }

    // Imprimir resultado
    std::cout << "Proceso " << rank << " tiene los rangos: ";
    for (int i = 0; i < size; i++) {
        std::cout << all_ranks[i] << " ";
    }
    std::cout << "\n";

    MPI_Finalize();
    return 0;
}
