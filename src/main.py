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


def main():
    copy_files("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


main()
