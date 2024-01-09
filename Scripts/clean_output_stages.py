import re
from pathlib import Path
from bs4 import BeautifulSoup


def get_html_chapter_files(folder):
    chapters_files = [x for x in Path(folder).iterdir()]
    return [str(x) for x in chapters_files if x.is_file() and x.name.endswith('html')]

chapters_folder = "./docs/Chapters/"
chapters_files = get_html_chapter_files(chapters_folder)


def read_file(path):
    with open(path, mode = 'r', encoding = "utf8") as file_connection:
        content = file_connection.readlines()
    return content

def read_html_file(path):
    text_file = read_file(path)
    text_file = ''.join(text_file)
    return BeautifulSoup(text_file, features="html.parser")


def remove_stages(html_file):
    for node in html_file.find_all("code"):
        text = node.text
        pattern = re.compile("^\\[Stage ")
        if pattern.match(text):
            node.decompose()
    
    return html_file


def rewrite_without_stages(path):
    html_file = read_html_file(path)
    html_file = remove_stages(html_file)
    with open(path, "w", encoding = "utf8") as file_connection:
        file_connection.write(str(html_file))
    return


for path in chapters_files:
    print(f"[INFO]: Rewriting {path}...")
    rewrite_without_stages(path)
