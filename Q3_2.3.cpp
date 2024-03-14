#include "mpi.h"
#include <cstdio>
using namespace std;


int main(int argc, char *argv[]) 
{
    MPI_Init(&argc, &argv);
    
    int name_lenght = MPI_MAX_PROCESSOR_NAME;
    char process_name[name_lenght];
    MPI_Get_processor_name(process_name, &name_lenght);
    printf("Proc Name: %s\n", process_name);    
    

    MPI_Finalize();
    return 0;
}
