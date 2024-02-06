#include "mpi.h"
#include <iostream>
using namespace std;

int main(int argc, char *argv[]) 
{
    MPI_Status Stat;
    int numtask, rank;
    cout << "Hello, World 1!" << endl;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD,&numtask);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    cout << "Hello, World 2!" << endl;
    cout << "Hello, World 3!" << endl;
    if (rank == numtask -1 ){
        cout << "Hello, World 4!" << endl;
    }
    return 0;
    MPI_Finalize();

}
