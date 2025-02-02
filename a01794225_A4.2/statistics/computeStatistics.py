"""
This script computes descriptive statistics (mean, median, mode, variance,
standard deviation) from a text file containing numeric data.
"""

import sys
import time
import math

STATISTIC_RESULTS = "StatisticsResults.txt"

# Global list to store numbers
NUMBERS = []

def read_nums_file(file_name):
    """
    Reads numeric data from a given file and processes each line.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                process_line(line.strip())
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

def process_line(line):
    """
    Processes each line, validating if it's a proper number.
    """
    try:
        number = float(line)
        NUMBERS.append(number)
    except ValueError:
        print(f"Invalid data: '{line}' - Skipping...")

def compute_mean():
    """
    Computes the mean of the numeric data.
    """
    return sum(NUMBERS) / len(NUMBERS)

def compute_median():
    """
    Computes the median of the numeric data.
    """
    sorted_nums = sorted(NUMBERS)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 != 0:
        return sorted_nums[mid]
    return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2

def compute_mode():
    """
    Computes the mode(s) of the numeric data.
    """
    frequency = {}
    for num in NUMBERS:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())
    if max_freq == 1:
        return "No mode"
    modes = [key for key, value in frequency.items() if value == max_freq]
    return modes if len(modes) > 1 else modes[0]

def compute_variance():
    """
    Computes the variance of the numeric data.
    """
    mean = compute_mean()
    return sum((x - mean) ** 2 for x in NUMBERS) / len(NUMBERS)

def compute_standard_deviation():
    """
    Computes the standard deviation of the numeric data.
    """
    return math.sqrt(compute_variance())

def write_to_file(content):
    """
    Appends the computed statistics to the output file.
    """
    with open(STATISTIC_RESULTS, "a", encoding="utf-8") as f:
        f.write(content + "\n")

def descriptive_stats():
    """
    Prints and saves descriptive statistics.
    """
    mean = compute_mean()
    median = compute_median()
    mode = compute_mode()
    variance = compute_variance()
    std_dev = compute_standard_deviation()

    results = (
        f"Mean: {format(mean, '.0f')}\n"
        f"Median: {format(median, '.0f')}\n"
        f"Mode: {mode}\n"
        f"Variance: {format(variance, '.0f')}\n"
        f"Standard Deviation: {format(std_dev, '.0f')}"
    )

    print(results)
    write_to_file(results)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compute_statistics.py fileWithData.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    start_time = time.time()

    read_nums_file(input_file)

    if NUMBERS:
        descriptive_stats()
        elapsed_time = time.time() - start_time
        time_info = f"Execution Time: {elapsed_time:.4f} seconds"
        print(time_info)
        write_to_file(time_info)
    else:
        print("No valid numeric data found in the file.")
        