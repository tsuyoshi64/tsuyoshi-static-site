class HTMLNode:
    def __init__(
        self,
        tag: None | str = None,
        value: None | str = None,
        children: None | list = None,
        props: None | dict = None,
    ):
        self.tag: None | str = tag
        self.value: None | str = value
        self.children: None | list = children
        self.props: None | dict = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props or self.props is None:
            return ""
        html_att: str = ""
        for k, v in self.props.items():
            html_att += f' {k}="{v}"'
        return html_att

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        props_str: str = self.props_to_html() if self.props else ""
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
