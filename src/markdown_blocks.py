import re
from enum import Enum

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_text_nodes
from textnode import TextNode, TextType, text_node_to_html_node


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


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes: list[TextNode] = text_to_text_nodes(text)
    children: list[LeafNode] = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    # <p> ... </p>
    text: str = " ".join(block.split("\n"))
    children: list[LeafNode] = text_to_children(text)
    # [LeafNode(...), LeafNode(...), LeafNode(...)]
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    # <h1>, <h6>
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    children: list[LeafNode] = text_to_children(block[level + 1 :])
    return ParentNode(f"h{level}", children)


def quote_to_html_node(block: str) -> ParentNode:
    # <blockquote>
    lines: list[str] = block.split("\n")
    lines: list[str] = [line.lstrip(">").strip() for line in lines]
    text: str = " ".join(lines)
    children: list[LeafNode] = text_to_children(text)
    return ParentNode("blockquote", children)


def code_to_html_node(block: str) -> ParentNode:
    # <pre><code>...</code></pre>
    # ```...```
    text_node: TextNode = TextNode(block[4:-3], TextType.NORMAL)
    child: LeafNode = text_node_to_html_node(text_node)
    code_node: ParentNode = ParentNode("code", [child])
    return ParentNode("pre", [code_node])


def ordered_to_html_node(block: str) -> ParentNode:
    lines: list[str] = block.split("\n")
    lines: list[str] = [line.split(". ", 1)[1] for line in lines]
    items: list[ParentNode] = []
    for line in lines:
        items.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ol", items)


def unordered_to_html_node(block: str) -> ParentNode:
    lines: list[str] = block.split("\n")
    lines: list[str] = [line.split("- ", 1)[1] for line in lines]
    items: list[ParentNode] = []
    for line in lines:
        items.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ul", items)


def block_to_html_node(block: str) -> ParentNode:
    block_type: BlockType = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_to_html_node(block)
    raise ValueError("invalid block type")


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    children: list = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)
