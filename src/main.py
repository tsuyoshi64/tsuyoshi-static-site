from textnode import TextNode, TextType


def main():
    textnode = TextNode(
        "This is my github", TextType.LINK, "https://github.com/tsuyoshi64"
    )
    print(textnode)


if __name__ == "__main__":
    main()
