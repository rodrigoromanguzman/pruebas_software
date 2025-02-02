"""
Module to count word frequencies in a text file.
Reads lines from a file, processes words, and outputs the word counts to a file.
"""

import sys
import time

WORD_COUNT_RESULTS = "WordCountResults.txt"

# Dictionary to store word counts
WORD_COUNT = {}

def read_words_file(file_name):
    """
    Read words from the specified file and process each line.
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
    Process each line, splitting into words and counting frequency.
    """
    words = split_into_words(line)
    for word in words:
        if is_valid(word):
            update_word_count(word)
        else:
            print(f"Invalid data: '{word}' - Skipping...")


def split_into_words(line):
    """
    Split a line into words.

    """
    words = []
    current_word = ""
    for char in line:
        if char != ' ':
            current_word += char
        else:
            if current_word:
                words.append(current_word)
                current_word = ""
    if current_word:
        words.append(current_word)
    return words


def is_valid(word):
    """
    Check if the word is valid (non-empty and alphabetic).
    """
    return all(char.isalpha() for char in word)


def update_word_count(word):
    """
    Update the counter for each word.
    """
    word = word.lower()  # Ensure case-insensitivity
    if word in WORD_COUNT:
        WORD_COUNT[word] += 1
    else:
        WORD_COUNT[word] = 1


def write_to_file(content):
    """
    Write results to the output file.
    """
    with open(WORD_COUNT_RESULTS, "a", encoding="utf-8") as file:
        file.write(content + "\n")


def display_word_counts():
    """
    Display and save word counts.
    """
    for word, count in WORD_COUNT.items():
        result = f"Word: '{word}' | Frequency: {count}"
        print(result)
        write_to_file(result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py fileWithData.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    start_time = time.time()

    open(WORD_COUNT_RESULTS, 'w', encoding='utf-8').close()  # Clear previous results


    read_words_file(input_file)

    if WORD_COUNT:
        display_word_counts()
        elapsed_time = time.time() - start_time
        time_info = f"Execution Time: {elapsed_time:.4f} seconds"
        print(time_info)
        write_to_file(time_info)
    else:
        print("No valid words found in the file.")
