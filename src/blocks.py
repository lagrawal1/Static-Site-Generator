from enum import Enum
from htmlnode import *
from textnode import *
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")

    def strip_whitespace(string):
        return string.strip()

    def Nonempty_String(string):
        return string != ""

    block_list = filter(Nonempty_String, block_list)

    block_list = list(map(strip_whitespace, block_list))
    return block_list


def block_to_block_type(MDBlock):
    if not (re.search(r"^#{1,6} ", MDBlock) == None):
        return BlockType.HEADING

    if MDBlock.startswith("```") and MDBlock.endswith("```"):
        return BlockType.CODE

    MDLines_List = MDBlock.split("\n")

    def line_startswith(line, substring):
        if line.startswith(substring):
            return True
        return False

    UnordListBool = True
    for line in MDLines_List:
        if not (line_startswith(line, "-")):
            UnordListBool = False
            break

    if UnordListBool:
        return BlockType.UNORDERED_LIST

    OrdListBool = True
    for i in range(len(MDLines_List)):
        if not (line_startswith(MDLines_List[i], str(i + 1) + ".")):
            OrdListBool = False
            break

    if OrdListBool:
        return BlockType.ORDERED_LIST

    QuoteListBool = True
    for line in MDLines_List:
        if not (line_startswith(line, ">")):
            QuoteListBool = False
            break

    if QuoteListBool:
        return BlockType.QUOTE

    return BlockType.PARAGRAPH
