Warmup 
## 1
### 1.1 (Ex. 2.18)
while the serial initialization part sets all elements of a to zero without issue, the parallel update portion can lead to inefficient execution due to cache conflicts and cache misses as multiple threads simultaneously update different elements of the array a that may reside on the same cache line. This inefficiency reduces the overall performance of the parallel section.
### 1.2 (Ex. 2.19)
Using a chunksize of 1 in this context is a bad strategy because it leads to false sharing. False sharing occurs when multiple threads modify variables that are close enough in memory to reside on the same cache line, even if they are not actually sharing data. This results in inefficient use of the cache, as one thread's update invalidates the cache line for other threads, causing unnecessary cache misses and memory traffic. This pattern of distribution (0, t, 2t, ... to the first thread, 1, 1+t, 1+2t, ... to the second, etc.) exacerbates false sharing because consecutive iterations, which are likely to modify adjacent elements of `a[]`, are assigned to different threads, increasing the likelihood that these elements are on the same cache line.

A better chunksize would be larger than 1, ideally large enough to ensure that the work assigned to each thread covers a block of data that fits within a single cache line or spans multiple cache lines without overlap between threads. This reduces the risk of false sharing by aligning work with cache line boundaries and improving cache utilization. The optimal chunksize depends on the specific cache line size of the system and the nature of the calculation, but it should be chosen to minimize cross-thread cache line invalidation while maximizing the utilization of each thread.

### 1.3 (Ex. 2.21)
### 1.4 (Ex. 2.22)
### 1.5 (Ex. 2.23)
### 1.6 (Ex. 2.27)

## 2