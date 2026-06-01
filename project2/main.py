'''
Written by: Stephen Heller, Northwestern University

5/18/2025

Test of "hot hand fallacy" via monte carlo simulation
'''

import ctypes
import os
import matplotlib.pyplot as plt
import time
import statistics

script_dir = os.path.dirname(os.path.abspath(__file__))
library_path = os.path.join(script_dir, "compute.so") # mac/linux--recompile and use .dll for windows
backend = ctypes.CDLL(library_path)

# configure function
backend.run_sim.argtypes = [
    ctypes.c_size_t, 
    ctypes.c_size_t,
    ctypes.c_uint64,
    ctypes.c_double,
    ctypes.POINTER(ctypes.c_double)

]
backend.run_sim.restype = None #in-place array operation

def main():

    num_trials = int(input("How many trials would you like to run?\n"))
    seq_len = int(input("How long should each sequence be (up to 64)\n"))
    if seq_len > 64:
        raise ValueError("64 bit implementation can only do sequences up to length 64\n")
    success_rate = float(input("What should the success rate be? Enter a number from 0 to 100\n"))

    streak_len = int(input("What should the streak length be?\n"))
    
    print(f"Running simulation of {num_trials} trials...")

    start = time.perf_counter()

    # Allocate a double array to take results
    c_double_array = ctypes.c_double * num_trials
    output_buffer = c_double_array()

    # Call C backend
    backend.run_sim(num_trials, seq_len, streak_len, success_rate, output_buffer)

    # Convert array to list
    raw_results = list(output_buffer)

    # Filter out games with 0 streaks
    valid_results = [r for r in raw_results if r != -1.0]

    print(f"Simulation done")

    # Data analysis
    avg_probability = sum(valid_results) / len(valid_results)
    print(f"\n\n\n Summary ")
    print(f"Probability of success after a streak: {avg_probability:.4f}")

    #median and quartiles

    median_val = statistics.media1000n(valid_results)
    q1, _, q3 = statistics.quantiles(valid_results, n=4)
    print(f"Q1 (25th Percentile): {q1:.4f}")
    print(f"Median:               {median_val:.4f}")
    print(f"Q3 (75th Percentile): {q3:.4f}")
    
    #variance/stddev
    variance = sum((x - avg_probability) ** 2 for x in valid_results) / len(valid_results)
    std_dev = variance ** 0.5
    print(f"Standard Deviation: {std_dev:.4f}")

    end = time.perf_counter()
    print(f"Time for sim: {end - start:.2f} seconds")

    # histogram
    plt.figure(figsize=(10, 6))
    
    plt.hist(valid_results, bins=30, alpha=0.7, color='blue')
    
    # Add a line showing the baseline shooter capability
    plt.axvline(success_rate / 100, color='red', linestyle='dashed', linewidth=2, label=f'Base Shooter Accuracy ({success_rate}%)')
    plt.axvline(avg_probability, color='green', linestyle='dotted', linewidth=2, label=f'Observed Mean ({avg_probability:.4f})')
    
    plt.title(f"Distribution of Success Rates After a {streak_len}-Hit Streak\n({len(valid_results):,} Independent 50-Shot Games)")
    plt.xlabel("Probability of Success on Next Shot")
    plt.ylabel("Number of Games")
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    print("\nDisplaying histogram plot...")
    plt.show()

    

if __name__ == "__main__":
    main()


