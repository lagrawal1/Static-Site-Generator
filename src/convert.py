from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode, LeafNode
from blocks import *
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.extend([node])
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise Exception("All markdown delimiters must be closed.")

        text_list = node.text.split(delimiter)
        node_list = []
        for i in range(len(text_list)):
            if i % 2 == 0:
                node_list.append(TextNode(text_list[i], TextType.TEXT))
            elif i % 2 == 1:
                node_list.append(TextNode(text_list[i], text_type))

        new_nodes.extend(node_list)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:

        if len(extract_markdown_images(node.text)) == 0:
            new_nodes.extend([node])
            continue

        text_list, node_list = [], []
        text_list = re.split(r"(!\[.*?\]\(.*?\))", node.text)
        text_list = list(filter(None, text_list))
        for i in range(len(text_list)):
            if len(re.findall(r"!\[.*?\]\(.*?\)", text_list[i])) == 0:
                node_list.append(TextNode(text_list[i], TextType.TEXT))
            else:
                image = extract_markdown_images(text_list[i])
                node_list.append(
                    TextNode(
                        image[0][0],
                        TextType.IMAGE,
                        image[0][1],
                    )
                )

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
        text_list = re.split(r"(\[.*?\]\(.*?\))", node.text)
        text_list = list(filter(None, text_list))

        for i in range(len(text_list)):
            if len(extract_markdown_links(text_list[i])) == 0:
                node_list.append(TextNode(text_list[i], TextType.TEXT))
            else:
                link = extract_markdown_links(text_list[i])
                node_list.append(
                    TextNode(
                        link[0][0],
                        TextType.LINK,
                        link[0][1],
                    )
                )

        new_nodes.extend(node_list)
    return new_nodes


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "a", value="", props={"src": text_node.url, "alt": text_node.text}
            )


def extract_markdown_images(text):
    image_tuples = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return image_tuples


def extract_markdown_links(text):
    link_tuples = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return link_tuples


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_link(split_nodes_image([text_node]))
    TextType_dict = {TextType.BOLD: "**", TextType.ITALIC: "_", TextType.CODE: "`"}
    for type in TextType_dict:
        nodes = split_nodes_delimiter(nodes, TextType_dict[type], type)
    return nodes


def extract_title(markdown):
    block_list = markdown_to_blocks(markdown)
    for block in block_list:
        if len(re.findall(r"^# ", block)) == 0:
            continue
        else:
            return re.sub(r"# ", "", block).strip()
    raise Exception("Markdown text must contain heading 1.")


def markdown_to_html_node(markdown):

    BlockList = markdown_to_blocks(markdown)
    HTML_Div = []

    def text_to_children(text):
        TextNode_List = text_to_textnodes(text)
        HTMLNode_List = list(map(text_node_to_html_node, TextNode_List))
        return HTMLNode_List

    def regex_md_line(regex):
        def curry_line(line):
            return re.sub(regex, "", line)

        return curry_line

    def regex_md_block(block, regex):
        line_list = block.split("\n")
        line_list = list(map(regex_md_line(regex), line_list))
        block = "\n".join(line_list)
        return block

    def block_to_paragraph(block):
        block = re.sub("\n", " ", block)
        HTMLNode_List = text_to_children(block)
        return ParentNode("p", HTMLNode_List, None)

    def block_to_heading(block):
        h_num = len(re.findall(r"^#{1,6} ", block)[0]) - 1
        block = re.sub(r"#{1,6} ", "", block)
        HTMLNode_List = text_to_children(block)
        return ParentNode("h" + str(h_num), HTMLNode_List, None)

    def block_to_quote(block):
        block = regex_md_block(block, r"^> ")

        HTMLNode_List = text_to_children(block)
        return ParentNode("blockquote", HTMLNode_List, None)

    def block_to_unordlist(block):
        block = regex_md_block(block, r"^- ")

        lines_list = block.split("\n")
        lines_html = list(map(text_to_children, lines_list))
        HTMLNode_List = []
        for node_list in lines_html:
            HTMLNode_List.append(ParentNode("li", node_list))

        return ParentNode("ul", HTMLNode_List, None)

    def block_to_ordlist(block):
        block = regex_md_block(block, r"^\d. ")

        lines_list = block.split("\n")
        lines_html = list(map(text_to_children, lines_list))
        HTMLNode_List = []
        for node_list in lines_html:
            HTMLNode_List.append(ParentNode("li", node_list))

        return ParentNode("ol", HTMLNode_List, None)

    for block in BlockList:
        Type = block_to_block_type(block)

        match Type:
            case BlockType.PARAGRAPH:
                HTML_Node = block_to_paragraph(block)
            case BlockType.HEADING:
                HTML_Node = block_to_heading(block)
            case BlockType.QUOTE:
                HTML_Node = block_to_quote(block)
            case BlockType.UNORDERED_LIST:
                HTML_Node = block_to_unordlist(block)
            case BlockType.ORDERED_LIST:
                HTML_Node = block_to_ordlist(block)
            case BlockType.CODE:
                block = block.strip("``` ").lstrip("\n")
                Block_HTML = LeafNode("code", block, None)
                HTML_Node = ParentNode("pre", [Block_HTML], None)

        HTML_Div.append(HTML_Node)

    return ParentNode("div", HTML_Div, None)
