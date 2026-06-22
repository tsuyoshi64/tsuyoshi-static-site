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
