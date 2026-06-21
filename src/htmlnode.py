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
        html_att = ""
        for k, v in self.props.items():
            html_att += f' {k}="{v}"'
        return html_att

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
