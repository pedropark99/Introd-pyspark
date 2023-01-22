import os
import re
from bs4 import BeautifulSoup

chapters_folder = "./docs/Chapters/"
chapters_files = os.listdir(chapters_folder)
chapters_files = [chapters_folder + f for f in chapters_files]

is_html = lambda x: x.endswith(".html")
chapters_files = list(filter(is_html, chapters_files))

def read_file(path:str) -> list[str]:
    with open(path, encoding="utf8") as f:
        file = f.readlines()
    return file


html_file = read_file(chapters_files[6])
html_file = ''.join(html_file)
html_file = BeautifulSoup(html_file, features="html.parser")


def remove_stages(html_file):
    for node in html_file.find_all("code"):
        text = node.text
        pattern = re.compile("\\[Stage ")
        if pattern.match(text):
            node.decompose()
    
    return html_file

# nodes_with_stage = list()
# for node in code_nodes:
#     text = node.text
#     if have_stage(text):
#         nodes_with_stage.append(node)

html_file = remove_stages(html_file)

with open(chapters_files[6], "w", encoding="utf8") as file:
    file.write(str(html_file))