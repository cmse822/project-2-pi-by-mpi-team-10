import matplotlib.pyplot as plt
import math

# Test data folder path
path = "./data/"

# Data from initial tests (1-4 processes)
initial_files = ["Q4-2_output_1.txt", "Q4-2_output_2.txt", "Q4-2_output_3.txt", "Q4-2_output_4.txt"]
initial_times = []
initial_process_counts = []
initial_pi_calcs = []

for f in initial_files:
    with open(path + f, 'r') as file:
        times = []
        for line in file:
            parts = line.split()
            if parts[0] == "I:":
                initial_process_counts.append(int(parts[1]))
            elif parts[0] == "P:":
                times.append(float(parts[2]))
            elif parts[0] == "F:":
                initial_pi_calcs.append(float(parts[1]))
        initial_times.append(max(times))

print("Data for initial tests, 100000 Darts")
print("Process:", initial_process_counts)
print("Times:", initial_times)
print("PIs:", initial_pi_calcs)

# Plot initial data
plt.figure(figsize=(10, 6))
plt.plot(initial_process_counts, initial_times, marker='o', linestyle='-')
plt.title('Parallel PI Calculation Performance')
plt.xlabel('Processor Count')
plt.ylabel('Performance (seconds)')
plt.grid(True)
plt.savefig(path + "Q4-2_plot.png")

# Data from tests on HPCC with 1000 darts (1-64 processes)

hpcc_files_1000 = ["Q4-4_output_1-1000.txt",
              "Q4-4_output_2-1000.txt",
              "Q4-4_output_4-1000.txt",
              "Q4-4_output_8-1000.txt",
              "Q4-4_output_16-1000.txt",
              "Q4-4_output_32-1000.txt",
              "Q4-4_output_64-1000.txt"]
hpcc_times_1000 = []
hpcc_process_counts_1000 = []
hpcc_pi_calcs_1000 = []

for f in hpcc_files_1000:
    with open(path + f, 'r') as file:
        times = []
        for line in file:
            # Split the line into components: Matrix Size, Time Taken, Performance
            parts = line.split()
            if parts[0] == "I:":
                hpcc_process_counts_1000.append(int(parts[1]))
            elif parts[0] == "P:":
                times.append(float(parts[2]))
            elif parts[0] == "F:":
                hpcc_pi_calcs_1000.append(float(parts[1]))
        hpcc_times_1000.append(max(times))

print("Data for HPCC, 1000 Darts")
print("Process:", hpcc_process_counts_1000)
print("Times:", hpcc_times_1000)
print("PIs:", hpcc_pi_calcs_1000)

# Data from tests on HPCC with 1000000 darts (1-64 processes)

hpcc_files_1000000 = ["Q4-4_output_1-1000000.txt",
              "Q4-4_output_2-1000000.txt",
              "Q4-4_output_4-1000000.txt",
              "Q4-4_output_8-1000000.txt",
              "Q4-4_output_16-1000000.txt",
              "Q4-4_output_32-1000000.txt",
              "Q4-4_output_64-1000000.txt"]
hpcc_times_1000000 = []
hpcc_process_counts_1000000 = []
hpcc_pi_calcs_1000000 = []

for f in hpcc_files_1000000:
    with open(path + f, 'r') as file:
        times = []
        for line in file:
            parts = line.split()
            if parts[0] == "I:":
                hpcc_process_counts_1000000.append(int(parts[1]))
            elif parts[0] == "P:":
                times.append(float(parts[2]))
            elif parts[0] == "F:":
                hpcc_pi_calcs_1000000.append(float(parts[1]))
        hpcc_times_1000000.append(max(times))

print("Data for HPCC, 1000000 Darts")
print("Process:", hpcc_process_counts_1000000)
print("Times:", hpcc_times_1000000)
print("PIs:", hpcc_pi_calcs_1000000)

# Data from tests on HPCC with 1000000000 darts (1-64 processes)

hpcc_files_1000000000 = ["Q4-4_output_1-1000000000.txt",
              "Q4-4_output_2-1000000000.txt",
              "Q4-4_output_4-1000000000.txt",
              "Q4-4_output_8-1000000000.txt",
              "Q4-4_output_16-1000000000.txt",
              "Q4-4_output_32-1000000000.txt",
              "Q4-4_output_64-1000000000.txt"]
hpcc_times_1000000000 = []
hpcc_process_counts_1000000000 = []
hpcc_pi_calcs_1000000000 = []

for f in hpcc_files_1000000000:
    with open(path + f, 'r') as file:
        times = []
        for line in file:
            parts = line.split()
            if parts[0] == "I:":
                hpcc_process_counts_1000000000.append(int(parts[1]))
            elif parts[0] == "P:":
                times.append(float(parts[2]))
            elif parts[0] == "F:":
                hpcc_pi_calcs_1000000000.append(float(parts[1]))
        hpcc_times_1000000000.append(max(times))

print("Data for HPCC, 1000000000 Darts")
print("Process:", hpcc_process_counts_1000000000)
print("Times:", hpcc_times_1000000000)
print("PIs:", hpcc_pi_calcs_1000000000)

# Plot error vs dart count for each processor count
darts = [1000, 1000000, 1000000000]
for i in range(len(hpcc_process_counts_1000)):
    errors = [abs(hpcc_pi_calcs_1000[i] - math.pi),
             abs(hpcc_pi_calcs_1000000[i] - math.pi),
             abs(hpcc_pi_calcs_1000000000[i] - math.pi)]
    plt.figure(figsize=(10, 6))
    plt.plot(darts, errors, marker='o', linestyle='-')
    plt.title(f"Error/Darts for {hpcc_process_counts_1000[i]} Processors")
    plt.xlabel('Darts')
    plt.ylabel('Error')
    plt.grid(True)
    plt.savefig(path + f"Q4-4_plot_errors_{hpcc_process_counts_1000[i]}.png")

# Plot runtime vs processor count for each dart count
plt.figure(figsize=(10, 6))
plt.plot(hpcc_process_counts_1000, hpcc_times_1000, marker='o', linestyle='-')
plt.title(f"Runtime/Processors for 1000 Darts")
plt.xlabel('Processors')
plt.ylabel('Runtime (seconds)')
plt.grid(True)
plt.savefig(path + "Q4-4_plot_runtime_1000.png")

plt.figure(figsize=(10, 6))
plt.plot(hpcc_process_counts_1000000, hpcc_times_1000000, marker='o', linestyle='-')
plt.title(f"Runtime/Processors for 1000000 Darts")
plt.xlabel('Processors')
plt.ylabel('Runtime (seconds)')
plt.grid(True)
plt.savefig(path + "Q4-4_plot_runtime_1000000.png")

plt.figure(figsize=(10, 6))
plt.plot(hpcc_process_counts_1000000000, hpcc_times_1000000000, marker='o', linestyle='-')
plt.title(f"Runtime/Processors for 1000000000 Darts")
plt.xlabel('Processors')
plt.ylabel('Runtime (seconds)')
plt.grid(True)
plt.savefig(path + "Q4-4_plot_runtime_1000000000.png")


