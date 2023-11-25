import re

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
    lines = text.split('\n')
    if is_trunc_needed(lines, n_chars) == False:
        return text
    
    truncated_text = list()
    for line in lines:
        n = len(line)
        if n > n_chars:
            truncated_text.append(
                truncate_line(line, n_chars)
            )
        else:
            truncated_text.append(line)

    truncated_text = '\n'.join(truncated_text)
    return truncated_text


# x = print_big_list(test_list)
# print(x)