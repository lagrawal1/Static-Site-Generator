from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode, LeafNode

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
            
def main():
    test = TextNode("testing za text", TextType.BOLD, "idk.com")
    print(test)

main()