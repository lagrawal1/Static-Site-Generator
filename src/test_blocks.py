import unittest

from blocks import *


class Test_MD_to_BlockType(unittest.TestCase):
    def test_heading(self):
        MDText = "### Hello world"
        MDType = block_to_block_type(MDText)
        self.assertEqual(MDType, BlockType.HEADING)

    def test_code(self):
        MDText = "``` code ```"
        MDType = block_to_block_type(MDText)
        self.assertEqual(MDType, BlockType.CODE)

    def test_quote(self):
        MDText = "> quotes"
        MDType = block_to_block_type(MDText)
        self.assertEqual(MDType, BlockType.QUOTE)

    def test_text(self):
        MDText = "Sup"
        MDType = block_to_block_type(MDText)
        self.assertEqual(MDType, BlockType.PARAGRAPH)

    def test_ord_list(self):
        MDText = "1. Hi\n2.Hello\n3.G'morning"
        MDType = block_to_block_type(MDText)
        self.assertEqual(MDType, BlockType.ORDERED_LIST)

    def test_unord_list(self):
        MDText = "- Hi\n- Hello\n- G'morning"
        MDType = block_to_block_type(MDText)
        self.assertEqual(MDType, BlockType.UNORDERED_LIST)
