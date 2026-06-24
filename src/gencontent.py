import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines: list[str] = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No header found.")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as markdown_file:
        markdown_content: str = markdown_file.read()

    with open(template_path, "r") as template_file:
        template_content: str = template_file.read()

    title: str = extract_title(markdown_content)
    html_content: str = markdown_to_html_node(markdown_content).to_html()

    final_html: str = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    if os.path.exists(dest_path):
        print(f"Warning: Overwriting existing file at {dest_path}")

    with open(dest_path, "w") as dest_file:
        dest_file.write(final_html)
