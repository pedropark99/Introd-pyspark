from contextlib import redirect_stdout
import io

df = '''+------------+-------------------+------------+-------------+----------------+----------+-----------+---------------------+---------------------+----------------------+
|dateTransfer|   datetimeTransfer|clientNumber|transferValue|transferCurrency|transferID|transferLog|destinationBankNumber|destinationBankBranch|destinationBankAccount|
+------------+-------------------+------------+-------------+----------------+----------+-----------+---------------------+---------------------+----------------------+
|  2022-12-31|2022-12-31 07:37:02|        4608|       5603.0|        dollar $|  20223561|       null|                  666|                 4425|               41323-1|
|  2022-12-31|2022-12-31 07:35:05|        1121|      4365.22|        dollar $|  20223560|       null|                  666|                 2400|               74120-4|
|  2022-12-31|2022-12-31 02:44:46|        1121|       7158.0|          zing ƒ|  20223558|       null|                  290|                 1100|               35424-4|
|  2022-12-31|2022-12-31 01:02:06|        4862|       6714.0|        dollar $|  20223557|       null|                  666|                 1002|               71839-1|
|  2022-12-31|2022-12-31 00:48:47|        3294|     10882.52|        dollar $|  20223556|       null|                  666|                 2231|               50190-5|
+------------+-------------------+------------+-------------+----------------+----------+-----------+---------------------+---------------------+----------------------+'''


# https://stackoverflow.com/questions/1218933/can-i-redirect-the-stdout-into-some-sort-of-string-buffer
# with io.StringIO() as buf, redirect_stdout(buf):    
#     output = buf.getvalue()
def get_substring_indexes(text, substring):
    indexes = list()
    for i in range(len(text)):
        char = text[i]
        if char == substring:
            indexes.append(i)
    return indexes



def get_columns_names(text):
    column_names = text.split('|')
    column_names = [name.strip() for name in column_names]
    column_names = list(filter(lambda name: name != '', column_names))
    return column_names

def get_columns_in_range(text, max_index):
    truncated_text = text[0:max_index]
    column_names = truncated_text.split('|')
    column_names = [name.strip() for name in column_names]
    column_names = list(filter(lambda name: name != '', column_names))
    return column_names


def create_remainder_message(columns, max_index, n_chars):
    all_columns = get_columns_names(columns)
    columns_in_range = get_columns_in_range(columns, max_index)
    remaning_columns = list()
    for column in all_columns:
        if column not in columns_in_range:
            remaning_columns.append(column)

    n = len(remaning_columns)
    if n > 0:
        columns = ', '.join(remaning_columns)
        message = f"... with {n} more columns: {columns}"
    else:
        return None

    if len(message) > n_chars:
        # Insert a break line
        commas = get_substring_indexes(message, ',')
        last_comma = max(filter(lambda x: x <= n_chars, commas))
        message = [
            message[:last_comma],
            message[(last_comma + 1):]
        ]
        message = '\n   '.join(message)

    return message


def add_column_delimiter(lines):
    for i in range(len(lines)):
        line = lines[i]
        n = len(line)
        if line[n - 1] == '-':
            line = line + '+'
        else:
            line = line + '|'

        lines[i] = line

    return lines







def print_dataframe_two_blocks(text, n_chars = 80):
    lines = text.split('\n')
    first_line = lines[0]
    
    if len(first_line) <= n_chars:
        return text
    
    trunc_area = first_line[0:n_chars]
    column_seps = get_substring_indexes(trunc_area, '+')
    max_char = max(column_seps)
    first_block = list()
    second_block = list()
    for i in range(len(lines)):
        line = lines[i]
        n = len(line)
        first_block.append(line[0:max_char])
        second_block.append(line[(max_char+1):n])

    first_block = add_column_delimiter(first_block)

    dataframe = first_block + [''] + second_block
    dataframe = '\n'.join(dataframe)

    return dataframe






def print_dataframe(text, n_chars = 80):
    lines = text.split('\n')
    first_line = lines[0]

    if len(first_line) <= n_chars:
        return text

    column_seps = get_substring_indexes(first_line, '+')
    max_index = max(filter(lambda x: x <= n_chars, column_seps))
    remainder_message = create_remainder_message(lines[1], max_index, n_chars)

    truncated_block = list()
    for i in range(len(lines)):
        line = lines[i]
        if 'only showing top' in line:
            truncated_block.append(line)
            continue

        truncated_line = line[0:max_index]

        if truncated_line[max_index - 1] == '-':
            truncated_line = truncated_line + '+'
        else:
            truncated_line = truncated_line + '|'

        truncated_block.append(truncated_line)


    truncated_block.append(remainder_message)
    truncated_block = '\n'.join(truncated_block)

    return truncated_block



# t = print_dataframe_two_blocks(df)

# print(t)