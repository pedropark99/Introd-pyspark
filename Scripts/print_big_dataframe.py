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
def get_substring_index(text, substring):
    indexes = list()
    for i in range(len(text)):
        char = text[i]
        if char == substring:
            indexes.append(i)
    return indexes

def print_dataframe(text, n_chars = 80):
    text = text.split('\n')
    first_line = text[0]
    trunc_area = first_line[0:n_chars]
    column_seps = get_substring_index(trunc_area, '+')
    max_char = max(column_seps)
    first_block = list()
    second_block = list()
    for i in range(len(text)):
        line = text[i]
        n = len(line)
        first_block.append(line[0:max_char])
        second_block.append(line[(max_char+1):n])

    first_block = '\n'.join(first_block)
    second_block = '\n'.join(second_block)

    print(first_block)
    print('\n')
    print(second_block)

    return None



t = print_dataframe(df)
print(t)