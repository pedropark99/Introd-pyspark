import re
import os


from print_big_dataframe import print_dataframe
from print_big_list import print_big_list
from print_big_text import print_big_text


def read_file(path):
    with open(path, 'r') as file:
        file_contents = file.read()
    return file_contents

def write_file(path, text):
    with open(path, 'w') as file:
        file.write(text)
    return True

#os.system("quarto render . --to pdf")


files = os.listdir('.')
tex_path = list(filter(lambda x: x.endswith('.tex'), files))[0]
tex_path = '/home/pedro/Documentos/Projetos/Livros/Introd-pyspark/Introduction-to-`pyspark`.tex'
tex_file = read_file(tex_path)
tex_file = tex_file.split('\n')


def find_substring(lines, substring):
    positions = list()
    for i in range(len(lines)):
        if substring in lines[i]:
            positions.append(i)

    return positions


def get_chunk_content(chunk_text):
    regex = r'\\begin{verbatim}\n|\n\\end{verbatim}'
    content = re.sub(regex, '', chunk_text)
    return content


def detect_chunk_type(content):
    df_regex = r'^[+]--'
    list_regex = r'^(\[|\{|StructType)'
    df_description_regex = r'^DataFrame\['

    if re.match(df_regex, content):
        return 'DataFrame'
    elif re.match(df_description_regex, content):
        return 'DataFrame description'
    elif re.match(list_regex, content):
        return 'list'
    else:
        return 'str'


chunks_begin = find_substring(tex_file, '\\begin{verbatim}')
chunks_end = find_substring(tex_file, '\\end{verbatim}')



if len(chunks_begin) != len(chunks_end):
    print(len(chunks_begin))
    print(len(chunks_end))

    print(chunks_begin)
    print(chunks_end)

    raise Exception('Quantidade de inícios de chunks está diferente do número de finais de chunks!')


chunks = list()
for i in range(len(chunks_begin)):
    begin = chunks_begin[i]
    end = chunks_end[i] + 1
    chunk_text = '\n'.join(tex_file[begin:end])
    chunk_content = get_chunk_content(chunk_text)
    chunk_type = detect_chunk_type(chunk_content)
    chunks.append({
        'chunk_begin': begin, 'chunk_end': end,
        'chunk_content': chunk_content,
        'chunk_type': chunk_type
    })





def truncate_chunks(chunk, n_chars = 80):
    chunk_type = chunk['chunk_type']
    if chunk_type == 'DataFrame':
        chunk['chunk_content'] = print_dataframe(chunk['chunk_content'], n_chars)
        return chunk
    elif chunk_type == 'DataFrame description':
        chunk['chunk_content'] = print_big_list(chunk['chunk_content'], n_chars)
        return chunk
    elif chunk_type == 'list':
        chunk['chunk_content'] = print_big_list(chunk['chunk_content'], n_chars)
        return chunk
    else:
        chunk['chunk_content'] = print_big_text(chunk['chunk_content'], n_chars)
        return chunk


chunks = [truncate_chunks(chunk) for chunk in chunks]

for chunk in chunks:
    chunk_begin = chunk['chunk_begin']
    chunk_end = chunk['chunk_end']
    chunk_content = chunk['chunk_content'].split('\n')

    n_lines_content = len(chunk_content)
    n_lines_content_with_begin_end = n_lines_content + 2
    n_lines_chunk = chunk_end - chunk_begin
    if n_lines_content_with_begin_end > n_lines_chunk:
        n_lines_to_merge = n_lines_content_with_begin_end - n_lines_chunk + 1
        lines_to_merge = chunk_content[(n_lines_content - n_lines_to_merge):n_lines_content]
        merged_lines = '\n'.join(lines_to_merge)
        chunk_content = chunk_content[:(n_lines_content - n_lines_to_merge)]
        chunk_content.append(merged_lines)


    tex_file[chunk_begin + 1:chunk_end - 1] = chunk_content


tex_file = '\n'.join(tex_file)
new_path = 'Introd-pyspark-fixed.tex'
write_file(new_path, tex_file)

os.system(f"xelatex \"{new_path}\"")
os.system(f"bibtex \"{new_path}\"")
os.system(f"xelatex \"{new_path}\"")

#### TESTS ================================
# transf_chunk = list()
# for chunk in chunks:
#     chunk_content = chunk['chunk_content']
#     if 'dateTransfer' in chunk_content:
#         transf_chunk.append(chunk)

# chunk = transf_chunk[0]
# chunk = truncate_chunks(chunk)
# chunk_begin = chunk['chunk_begin']
# chunk_end = chunk['chunk_end']
# chunk_content = chunk['chunk_content'].split('\n')

# n_lines_content = len(chunk_content)
# n_lines_content_with_begin_end = n_lines_content + 2
# n_lines_chunk = chunk_end - chunk_begin
# if n_lines_content_with_begin_end > n_lines_chunk:
#     n_lines_to_merge = n_lines_content_with_begin_end - n_lines_chunk + 1
#     lines_to_merge = chunk_content[(n_lines_content - n_lines_to_merge):n_lines_content]
#     merged_lines = '\n'.join(lines_to_merge)
#     chunk_content = chunk_content[:(n_lines_content - n_lines_to_merge)]
#     chunk_content.append(merged_lines)


# print(n_lines_content)
# print("================")
# print(tex_file[chunk_begin:chunk_end])


