from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode, LeafNode
from blocks import *
from convert import *
import re
import os
import shutil


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


def generate_page(from_path, template_path, dest_path):
    with open(from_path) as markdown, open(template_path) as template:
        markdown_content = markdown.read()
        template_content = template.read()
        HTML_content = markdown_to_html_node(markdown_content).to_html()
        Title = extract_title(markdown_content)
        template_content = template_content.replace("{{ Title }}", Title)
        template_content = template_content.replace("{{ Content }}", HTML_content)
        if not (os.path.exists(os.path.dirname(dest_path))):
            os.makedirs(os.path.dirname(dest_path))
        newfile = open(dest_path, "w")
        newfile.write(template_content)
    return


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        generate_page(
            dir_path_content, template_path, dest_dir_path.replace("md", "html")
        )
        return

    for path in os.listdir(dir_path_content):
        generate_pages_recursive(
            os.path.join(dir_path_content, path),
            template_path,
            os.path.join(dest_dir_path, path),
        )


def main():
    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")


main()
