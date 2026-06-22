import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old in old_nodes:
        if old.text_type != TextType.NORMAL:
            new_nodes.append(old)
            continue

        parts: list[str] = old.text.split(delimiter)

        # Delimiters must come in pairs; an even number of parts means an unclosed delimiter
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax: unclosed delimiter: '{delimiter}' found!"
            )

        split_nodes: list[TextNode] = []
        for i, part in enumerate(parts):
            if part == "":
                continue

            # even indexes are outside the delimiters -> NORMAL
            # odd indexes are inside the delimiters -> target type
            if i % 2 == 0:
                split_nodes.append(TextNode(part, TextType.NORMAL))
            else:
                split_nodes.append(TextNode(part, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # !         -> Matches the exclamation mark for images
    # \[(.*?)\] -> Captures everything inside the square brackets (alt text) non-greedily
    # \((.*?)\) -> Captures everything inside the parentheses (URL) non-greedily
    pattern: str = r"!\[(.*?)\]\((.*?)\)"
    matches: list[tuple[str, str]] = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # (?<!\!) ensures the link does not have an exclamation mark in front of it
    pattern: str = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    matches: list[tuple[str, str]] = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old in old_nodes:
        if old.text_type != TextType.NORMAL:
            new_nodes.append(old)
            continue

        original_text: str = old.text
        images: list[tuple[str, str]] = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(old)
            continue

        for alt_text, url in images:
            # Split once per loop to safely isolate the current image
            sections: list[str] = original_text.split(f"![{alt_text}]({url})", 1)
            # Only splitted once so there should be only two parts
            if len(sections) != 2:
                continue
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            original_text: str = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old in old_nodes:
        if old.text_type != TextType.NORMAL:
            new_nodes.append(old)
            continue

        original_text: str = old.text
        links: list[tuple[str, str]] = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(old)
            continue

        for alt_text, url in links:
            sections: list[str] = original_text.split(f"[{alt_text}]({url})", 1)
            if len(sections) != 2:
                continue
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            original_text: str = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))

    return new_nodes


def text_to_text_nodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.NORMAL)]
    nodes: list[TextNode] = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes: list[TextNode] = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes: list[TextNode] = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes: list[TextNode] = split_nodes_image(nodes)
    nodes: list[TextNode] = split_nodes_link(nodes)
    return nodes
