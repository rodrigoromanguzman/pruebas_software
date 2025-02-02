"""

This script reads decimal numbers from a specified file, converts each number 
to its binary and hexadecimal representations (handling both positive and 
negative numbers using two's complement for negatives), and writes the 
results to an output file named 'ConversionResults.txt'.

"""

import sys
import time

CONVERSION_RESULTS = "ConversionResults.txt"


def read_nums_file(file_name):
    """Read numbers from a file and return as a list of strings."""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)


def process_numbers(number_list):
    """Validate and process each number from the list."""
    results = []
    for line in number_list:
        try:
            number = int(line)
            results.append(convert_number(number))
        except ValueError:
            print(f"Invalid data: '{line}' - Skipping...")
    return results


def decimal_to_binary(decimal_num):
    """Convert a decimal number to its minimal binary representation."""
    if decimal_num == 0:
        return "0"

    if decimal_num < 0:
        bits = 32
        two_complement = (1 << bits) + decimal_num
        binary_str = bin(two_complement)[2:]
        minimal_binary = binary_str.lstrip('0') if '0' in binary_str else binary_str
        return minimal_binary

    return bin(decimal_num)[2:]


def decimal_to_hexadecimal(decimal_num):
    """Convert a decimal number to its hexadecimal representation."""
    if decimal_num == 0:
        return "0"

    if decimal_num < 0:
        bits = 32
        two_complement = (1 << bits) + decimal_num
        return hex(two_complement)[2:].upper().zfill(8)

    return hex(decimal_num)[2:].upper()


def convert_number(number):
    """Convert a number to binary and hexadecimal formats."""
    binary = decimal_to_binary(number)
    hexadecimal = decimal_to_hexadecimal(number)
    return f"Decimal: {number} | Binary: {binary} | Hexadecimal: {hexadecimal}"


def write_to_file(contents):
    """Write all conversion results to the output file."""
    try:
        with open(CONVERSION_RESULTS, "w",encoding="utf-8") as file:
            file.write("\n".join(contents) + "\n")
    except IOError as error:
        print(f"Error writing to file: {error}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    start_time = time.time()

    numbers = read_nums_file(input_file)
    conversion_results = process_numbers(numbers)

    elapsed_time = time.time() - start_time
    time_info = f"Execution Time: {elapsed_time:.4f} seconds"

    conversion_results.append(time_info)
    write_to_file(conversion_results)

    # Display results
    for result in conversion_results:
        print(result)
