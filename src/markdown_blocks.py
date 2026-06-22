import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    if not block:
        return BlockType.PARAGRAPH
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines: list[str] = block.split("\n")

    is_quote: bool = True
    for line in lines:
        if not line.startswith(">"):
            is_quote: bool = False
            break
    if is_quote:
        return BlockType.QUOTE

    is_unordered: bool = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST

    is_ordered: bool = True
    expected_num: int = 1
    for line in lines:
        if not line.startswith(f"{expected_num}. "):
            is_ordered = False
            break
        expected_num += 1
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
