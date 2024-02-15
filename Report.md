Warmup 
## 1
### 1.1 (Ex. 2.18)
while the serial initialization part sets all elements of a to zero without issue, the parallel update portion can lead to inefficient execution due to cache conflicts and cache misses as multiple threads simultaneously update different elements of the array a that may reside on the same cache line. This inefficiency reduces the overall performance of the parallel section.
### 1.2 (Ex. 2.19)
Using a chunksize of 1 in this context is a bad strategy because it leads to false sharing. False sharing occurs when multiple threads modify variables that are close enough in memory to reside on the same cache line, even if they are not actually sharing data. This results in inefficient use of the cache, as one thread's update invalidates the cache line for other threads, causing unnecessary cache misses and memory traffic. This pattern of distribution (0, t, 2t, ... to the first thread, 1, 1+t, 1+2t, ... to the second, etc.) exacerbates false sharing because consecutive iterations, which are likely to modify adjacent elements of `a[]`, are assigned to different threads, increasing the likelihood that these elements are on the same cache line.

A better chunksize would be larger than 1, ideally large enough to ensure that the work assigned to each thread covers a block of data that fits within a single cache line or spans multiple cache lines without overlap between threads. This reduces the risk of false sharing by aligning work with cache line boundaries and improving cache utilization. The optimal chunksize depends on the specific cache line size of the system and the nature of the calculation, but it should be chosen to minimize cross-thread cache line invalidation while maximizing the utilization of each thread.

### 1.3 (Ex. 2.21)
```c
// Global Version
for (i = 0; i < ProblemSize; i++) {
    if (i == 0)
        a[i] = (b[i] + b[i + 1]) / 2;
    else if (i == ProblemSize - 1)
        a[i] = (b[i] + b[i - 1]) / 2;
    else
        a[i] = (b[i] + b[i - 1] + b[i + 1]) / 3;
}

// Parallel Version with boundary fix
MPI_Comm_rank(MPI_COMM_WORLD, &myTaskID);
MPI_Comm_size(MPI_COMM_WORLD, &nTasks);
if (myTaskID == 0)
    leftproc = MPI_PROC_NULL;
else
    leftproc = myTaskID - 1;
if (myTaskID == nTasks - 1)
    rightproc = MPI_PROC_NULL;
else
    rightproc = myTaskID + 1;
MPI_Sendrecv(&b[LocalProblemSize - 1], &bfromleft, rightproc);
MPI_Sendrecv(&b[0], &bfromright, leftproc);
// get bfromleft and bfromright from neighbour processors, then
for (i = 0; i < LocalProblemSize; i++) {
    if (i == 0)
        bleft = bfromleft;
    else
        bleft = b[i - 1];
    if (i == LocalProblemSize - 1)
        bright = bfromright;
    else
        bright = b[i + 1];
    // handle if we are first operation
    if (myTaskID == 0 && i == 0) {
        a[i] = (b[i] + bright) / 2;
    }
    // handle if we are the very last operation
    else if (myTaskID == nTasks && i == LocalProblemSize - 1) {
        a[i] = (b[i] + bleft) / 2;
    } else {
        a[i] = (b[i] + bleft + bright) / 3;
    }
}
```
### 1.4 (Ex. 2.22)

Equation 2.5
$
\begin{cases}
y_i ← y_i + x_{i−1} & i = 1 . . . n − 1 \\
y_0 ← y_0 + x_{n−1} & i = 0
\end{cases}
$

```c
int main(int argc, char *argv[])
{
    MPI_INIT(&argc, &argv);
    int x, y = array elements of x[rank] and y[rank];
    int myTaskID, nTasks;
    MPI_Comm_rank(MPI_COMM_WORLD, &myTaskID);
    MPI_Comm_size(MPI_COMM_WORLD, &nTasks);

    // Send out x value to my right neighbor, as long as I'm not the last processor.
    if(myTaskId != nTasks-1){
        MPI_ISend(x[myTaskId], 1, MPI_INT, myTaskID+1, 0, MPI_COMM_WORLD, &sendhandle);
    }
    

    //check what process number I am
    int recieved = 0;
    if(myTaskId == 0){
        // I am first process, recieve from last processor 
        MPI_IReceive(recieved, 1, MPI_INT, nTasks-1, 0, MPI_COMM_WORLD, &recvhandle);
    }
    else {
        // I am not the first, recieve from left processor
        MPI_IReceive(recieved, 1, MPI_INT, nTasks-1, 0, MPI_COMM_WORLD, &recvhandle);
    }
    MPI_Wait(recvhandle);

    //Do work with recieved value.
    y[myTaskId] = y[myTaskId] + recieved;

    
    MPI_Wait(sendhandle);
    MPI_FINALIZE();
}

```
The disadvantge of this code compared to the blocking code is that it has to allocate more memory to buffers as it can't reuse the send buffer again since it doesn't know if the send has completed by the time we are looking to recieve an element from the left neighbor.  Manually managing the completion of the sending and recieving operations also leads to increased complexity.

### 1.5 (Ex. 2.23)
Considering that we have a communciation between two nodes with bandwith that only allows for one message to pass it would be beneficial to reduce the amount of messages sent. In the hybrid model we would be able to save bandwidth by sending one bundle of messages through between the nodes.  In addition we would be able to save out on the message latency that comes from communication between processors on the same node as they would be able to use the alternative communication and not have to go through the network.


### 1.6 (Ex. 2.27)
In parallel computing, overlapping computation and communication can greatly enhance performance, depending on the specific tasks involved. Let's consider the potential gains in various scenarios:

When there's only communication and no computation, the benefits of overlapping are limited since there's no computation to overlap with. However, it can still ensure efficient resource utilization by keeping processors busy during communication tasks.

On the other hand, if we are dealing with a situation with only computation and no communication, overlapping won't directly reduce overall execution time even though it helps maximize processor utilization by initiating communication tasks during computational downtime.

In real-world scenarios we are generally in the situation where both computation and communication occur, overlapping becomes crucial. By executing these tasks concurrently, idle periods are minimized, leading to faster overall execution times. The degree of benefit depends on factors such as communication efficiency, task parallelism, and the ability to overlap tasks without introducing overhead.
## 2
