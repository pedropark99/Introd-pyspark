import re
import subprocess
import os

test_list = "StructType([StructField('id', LongType(), True), StructField('value', DoubleType(), True), StructField('date', DateType(), True)])"


def get_substring_indexes(text, substring):
    indexes = list()
    for i in range(len(text)):
        char = text[i]
        if char == substring:
            indexes.append(i)
    return indexes


def is_trunc_needed(lines, n_chars):
    for line in lines:
        n = len(line)
        if n > n_chars:
            return True
        
    return False


def truncate_line(line, n_chars):
    truncated_text = list()
    current_line = line
    stage_regex = r'\[Stage [0-9]:>'

    while True:
        if len(current_line) <= n_chars:
            truncated_text.append(current_line)
            break

        if re.match(stage_regex, current_line):
            truncated_text.append(current_line)
            break

        breakpoints = get_substring_indexes(current_line, ',')
        max_index = max(filter(lambda index: index <= n_chars, breakpoints))

        trunc_text = current_line[:max_index]
        truncated_text.append(trunc_text)
        current_line = current_line[max_index:]

    truncated_text = '\n'.join(truncated_text)
    return truncated_text
    



def print_big_list(text, n_chars = 80):
    from pprint import pformat
    text = re.sub("\n", ' ', text)
    formatted_output = pformat(text, indent = 2, width = n_chars)
    formatted_output = re.sub("^[(]", "", formatted_output)
    formatted_output = re.sub("[)]$", "", formatted_output)
    formatted_output = formatted_output.split('\n')
    for i in range(len(formatted_output)):
        current_line = formatted_output[i]
        for chr in current_line:
            if chr == '"' or chr == "'":
                char_to_replace = chr
                break

        formatted_output[i] = re.sub(char_to_replace, '', current_line)

    formatted_output = "\n".join(formatted_output)
    return formatted_output


def split_list_into_lines(input_list, max_items_per_line):
    input_list = [x.strip() for x in input_list.split(',')]
    result = [input_list[i:i + max_items_per_line] for i in range(0, len(input_list), max_items_per_line)]
    adjusted_lines = list()
    for line_elements in result:
        adjusted_lines.append(', '.join(line_elements))

    return ',\n'.join(adjusted_lines)


