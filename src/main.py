from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode, LeafNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.extend(node)
            continue

        if node.text.count(delimiter)%2 != 0:
            raise Exception("All markdown delimiters must be closed.")
        
        text_list = node.text.split(delimiter)
        node_list = []
        for i in range(len(text_list)):
            if i%2 == 0:
                node_list.append(TextNode(text_list[i], TextType.TEXT))
            elif i%2 == 1:
                node_list.append(TextNode(text_list[i], text_type))
        
        new_nodes.extend(node_list)
    return new_nodes           

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.extend(node)
            continue

        text_list, node_list = [], []
        for image in images:
            text_list = re.split(r"!\[.*?\]\(.*?\)", node.text)
        
        for i in range(len(text_list) + len(images) - 1):
            if i%2 == 0:
                node_list.append(TextNode(text_list[int(i/2)], TextType.TEXT))
            elif i%2 == 1:
                node_list.append(TextNode(images[int((i-1)/2)][0], TextType.IMAGE, images[int((i-1)/2)][1]))
                
        new_nodes.extend(node_list)
    return new_nodes

            
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.extend([node])
            continue

        text_list, node_list = [], []
        for image in links:
            text_list = re.split(r"\[.*?\]\(.*?\)", node.text)
        
        for i in range(len(text_list) + len(links) - 1):
            if i%2 == 0:
                node_list.append(TextNode(text_list[int(i/2)], TextType.TEXT))
            elif i%2 == 1:
                node_list.append(TextNode(links[int((i-1)/2)][0], TextType.LINK, links[int((i-1)/2)][1]))
                
        new_nodes.extend(node_list)
    return new_nodes




def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i" , text_node.text)
        case TextType.CODE:
            return LeafNode("code" , text_node.text)
        case TextType.LINK:
            return LeafNode("a" , text_node.text, props = {"href" : text_node.url})
        case TextType.IMAGE:
            return LeafNode("a" , value = "", props = {"src" : text_node.url , "alt" : text_node.text})

def extract_markdown_images(text):
    image_tuples = re.findall(r"!\[(.*?)\]\((.*?)\)" , text)
    return image_tuples

def extract_markdown_links(text):
    link_tuples = re.findall(r"\[(.*?)\]\((.*?)\)" , text)
    return link_tuples
              
def main():
    test = TextNode("testing za text", TextType.BOLD, "idk.com")
    print(test)

main()