from textnode import TextNode

from blocks import *
from convert import *
import re
import os
import shutil
import sys


def copy_files(source, destination):
    shutil.rmtree(destination)
    os.mkdir(destination)

    for path in os.listdir(source):
        if os.path.isfile(os.path.join(source, path)):
            shutil.copy(os.path.join(source, path), os.path.join(destination, path))
        else:
            os.mkdir(os.path.join(destination, path))
            copy_files(os.path.join(source, path), os.path.join(destination, path))
    return


def generate_page(from_path, template_path, dest_path, base_path):
    with open(from_path) as markdown, open(template_path) as template:
        markdown_content = markdown.read()
        template_content = template.read()
        HTML_content = markdown_to_html_node(markdown_content).to_html()
        Title = extract_title(markdown_content)
        template_content = template_content.replace("{{ Title }}", Title)
        template_content = template_content.replace("{{ Content }}", HTML_content)
        template_content = template_content.replace(f'href="/', f'href="{base_path}')
        template_content = template_content.replace(f'src="/', f'src="{base_path}')
        if not (os.path.exists(os.path.dirname(dest_path))):
            os.makedirs(os.path.dirname(dest_path))
        newfile = open(dest_path, "w")
        newfile.write(template_content)
    return


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    if os.path.isfile(dir_path_content):
        generate_page(
            dir_path_content,
            template_path,
            dest_dir_path.replace("md", "html"),
            base_path,
        )
        return

    for path in os.listdir(dir_path_content):
        generate_pages_recursive(
            os.path.join(dir_path_content, path),
            template_path,
            os.path.join(dest_dir_path, path),
            base_path,
        )


def main():
    if len(sys.argv) <= 1:
        base_path = "/"
    else:
        base_path = sys.argv[1]
    print(base_path)

    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "docs", base_path)


main()
