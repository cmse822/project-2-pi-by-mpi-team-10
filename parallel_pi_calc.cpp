#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

void srandom (unsigned seed);  
double dboard (int darts);

int main(int argc, char *argv[])
{
  double pi;
  double avepi;
  double averages[4];
  int darts = 10000;
  int rounds = 100;
  int root = 0;
  int i, n, tasks, rank;

  // Accept new values for darts and rounds from command line
  if (argc == 3)
  {
    darts = strtol(argv[1], NULL, 10);
    rounds = strtol(argv[2], NULL, 10);
  }

  // Start MPI
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &tasks);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);

  // Ensure inputs are valid, if not, exit
  if (tasks > 4 || tasks < 1 || darts < 1 || rounds < 1)
  {
    if (rank == 0)
    {
      printf("Invalid inputs\n");
    }
    MPI_Finalize();
    return 1;
  }

  // Initial display, main task only (rank = 0)
  if (rank == 0)
  {
    printf("Starting parallel version of pi calculation using dartboard algorithm (darts = %d, rounds = %d)...\n\n", darts, rounds);
  }

  // Set different seed for each process (will be the same each instance for testing)
  srandom((rank + 1));

  // Calculate running average for (rounds / # processes)
  avepi = 0;
  for (i = 0; i < rounds / tasks; i++) {
    pi = dboard(darts);
    avepi = ((avepi * i) + pi)/(i + 1);

    // Feel free to uncomment, but due to how buffering stdout works, this will not always come out nicely
    // printf("Process %d | After %3d throws, average value of pi = %10.8f\n", rank, (darts * (i + 1)), avepi);
  }

  // Gather each average in the array (won't always be full, max 4 tasks)
  // (send buffer, send count, send type, receive buffer, receive count, receive type, root, comm)
  MPI_Gather(&avepi, 1, MPI_DOUBLE, &averages, 1, MPI_DOUBLE, root, MPI_COMM_WORLD);
  MPI_Barrier(MPI_COMM_WORLD);

  // Average each process' average and display from the main thread (rank 0)
  if (rank == 0)
  {
    double pi = 0.0;
    for (int i = 0; i < tasks; ++i)
    {
      pi += averages[i];
      printf("Process finished, average is: %10.8f\n", averages[i]);
    }
    pi /= (double)tasks;
    printf("\nFinal approximation of PI: %10.8f\n", pi);
    printf("\nReal value of PI: 3.1415926535897\n");
  }

  // Stop MPI and exit
  MPI_Finalize();
  return 0;
}


/*****************************************************************************
 * dboard
 *****************************************************************************/
#define sqr(x)	((x)*(x))
long random(void);

double dboard(int darts)
{
   double x_coord,       /* x coordinate, between -1 and 1  */
          y_coord,       /* y coordinate, between -1 and 1  */
          pi,            /* pi  */
          r;             /* random number scaled between 0 and 1  */
   int score,            /* number of darts that hit circle */
       n;
   unsigned int cconst;  /* must be 4-bytes in size */
/*************************************************************************
 * The cconst variable must be 4 bytes. We check this and bail if it is
 * not the right size
 ************************************************************************/
   if (sizeof(cconst) != 4) {
      printf("Wrong data size for cconst variable in dboard routine!\n");
      printf("See comments in source file. Quitting.\n");
      exit(1);
      }
   /* 2 bit shifted to MAX_RAND later used to scale random number between 0 and 1 */
   cconst = 2 << (31 - 1);
   score = 0;

/***********************************************************************
 * Throw darts at board.  Done by generating random numbers
 * between 0 and 1 and converting them to values for x and y
 * coordinates and then testing to see if they "land" in
 * the circle."  If so, score is incremented.  After throwing the
 * specified number of darts, pi is calculated.  The computed value
 * of pi is returned as the value of this function, dboard.
 ************************************************************************/

   for (n = 1; n <= darts; n++) {
      /* generate random numbers for x and y coordinates */
      r = (double)random()/cconst;
      x_coord = (2.0 * r) - 1.0;
      r = (double)random()/cconst;
      y_coord = (2.0 * r) - 1.0;

      /* if dart lands in circle, increment score */
      if ((sqr(x_coord) + sqr(y_coord)) <= 1.0)
         score++;
      }

   /* calculate pi */
   pi = 4.0 * (double)score/(double)darts;
   return(pi);
} 
