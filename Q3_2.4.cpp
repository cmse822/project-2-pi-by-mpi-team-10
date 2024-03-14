#include "mpi.h"
#include <cstdio>
using namespace std;


int main(int argc, char *argv[]) 
{
    MPI_Init(&argc, &argv);

    int size, rank;

    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    printf("Process: %d out of %d\n", rank, size);

    MPI_Finalize();
    return 0;
}
