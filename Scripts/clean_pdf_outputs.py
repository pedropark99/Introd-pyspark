import sys
import os
import re
from itertools import chain

from print_big_dataframe import print_dataframe
from print_big_list import print_big_list, split_list_into_lines
from print_big_text import print_big_text

TEX_FILE_PATH = "Introduction-to-`pyspark`.tex"
# Number of characters to use as the limit for truncate
# lines of text
TRUNCATE_LIMIT = 80
BEGIN_VERBATIM_REGEX = r'\\begin\{verbatim\}'
END_VERBATIM_REGEX = r'\\end\{verbatim\}'
STAGE_REGEX = r'^\[Stage'

def read_text_file(file_path):
    with open(file_path, mode = 'r', encoding = "utf8") as file_connection:
        content = file_connection.read()
    return content

def write_text_file(file_path, content):
    with open(file_path, 'w', encoding = 'utf-8') as file_connection:
        file_connection.write(content)

TEX_FILE = read_text_file(TEX_FILE_PATH)
TEX_LINES = TEX_FILE.split('\n')


def find_positions(lines, regex_pattern):
    positions = list()
    pattern = re.compile(regex_pattern)

    for i, string in enumerate(lines):
        if pattern.search(string):
            positions.append(i)

    return positions


BEGIN_POSITIONS = find_positions(TEX_LINES, BEGIN_VERBATIM_REGEX)
END_POSITIONS = find_positions(TEX_LINES, END_VERBATIM_REGEX)


def build_chunk_ranges(begin_positions, end_positions):
    chunk_ranges = list()
    for b, e in zip(begin_positions, end_positions):
        chunk_ranges.append(list(range(b + 1, e + 1)))
    return chunk_ranges


CHUNK_RANGES = build_chunk_ranges(BEGIN_POSITIONS, END_POSITIONS)
def collect_chunk_content(chunk_range):
    s = chunk_range[0]
    e = chunk_range[-1]
    return '\n'.join(TEX_LINES[s:e])


def is_dataframe_output(text):
    return text.startswith('+--')

def is_list_output(text):
    regex = re.compile(r'(^\[)|(^StructType\()')
    return regex.match(text)

def is_stage_output(text):
    regex = re.compile(STAGE_REGEX)
    return regex.match(text)


def need_adjustment(chunk_output, n_chars = TRUNCATE_LIMIT):
    lines = chunk_output.split('\n')
    for line in lines:
        if len(line) >= n_chars:
            return True
        
    return False

def adjust_chunk_output(chunk_output):
    if is_dataframe_output(chunk_output) and need_adjustment(chunk_output):
        print("[INFO]: Found a DataFrame output that needs adjustment! Adjusting...")
        chunk_output = print_dataframe(chunk_output, n_chars = TRUNCATE_LIMIT)
    if is_list_output(chunk_output) and need_adjustment(chunk_output):
        print("[INFO]: Found a list output that needs adjustment! Adjusting...")
        chunk_output = split_list_into_lines(chunk_output, max_items_per_line = 3)
    if need_adjustment(chunk_output):
        print("[INFO]: Found text output that needs adjustment! Adjusting...")
        chunk_output = print_big_text(chunk_output, n_chars = TRUNCATE_LIMIT)

    return chunk_output



adjusted_lines = list()
last_index = 0
for chunk_range in CHUNK_RANGES:
    start_index = chunk_range[0]
    end_index = chunk_range[-1]
    print(f"[INFO]: Found chunk output at indexes {start_index}, {end_index}")
    chunk_output = collect_chunk_content(chunk_range)

    if is_stage_output(chunk_output):
        # Remove stage outputs
        print("[INFO]: Found a stage output at: ", start_index)
        adjusted_lines.append('\n'.join([
            '\n'.join(TEX_LINES[last_index:(start_index - 1)])
        ]))
        last_index = end_index + 1
        continue

    # The chunk is not a stage output
    adjusted_output = adjust_chunk_output(chunk_output)
    adjusted_lines.append('\n'.join([
        '\n'.join(TEX_LINES[last_index:start_index]),
        adjusted_output,
        TEX_LINES[end_index]
    ]))
    last_index = end_index + 1


# Append the last lines of the document
adjusted_lines.append('\n'.join([
    '\n'.join(TEX_LINES[last_index:])
]))

adjusted_lines = '\n'.join(adjusted_lines)
write_text_file(TEX_FILE_PATH, adjusted_lines)
print(f"[INFO]: Rewrited tex file {TEX_FILE_PATH}")

