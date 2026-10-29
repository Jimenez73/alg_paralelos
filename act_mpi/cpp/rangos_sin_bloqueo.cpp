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

    // Arreglos de requests para operaciones no bloqueantes
    std::vector<MPI_Request> send_requests(size);
    std::vector<MPI_Request> recv_requests(size);

    // Iniciar todas las recepciones no bloqueantes
    for (int i = 0; i < size; i++) {
        if (i != rank) {
            MPI_Irecv(&all_ranks[i], 1, MPI_INT, i, 0,
                      MPI_COMM_WORLD, &recv_requests[i]);
        }
    }

    // Iniciar todos los envios no bloqueantes
    for (int i = 0; i < size; i++) {
        if (i != rank) {
            MPI_Isend(&rank, 1, MPI_INT, i, 0,
                      MPI_COMM_WORLD, &send_requests[i]);
        }
    }

    // Esperar a que todas las operaciones terminen
    for (int i = 0; i < size; i++) {
        if (i != rank) {
            MPI_Wait(&send_requests[i], MPI_STATUS_IGNORE);
            MPI_Wait(&recv_requests[i], MPI_STATUS_IGNORE);
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
