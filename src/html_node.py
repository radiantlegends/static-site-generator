class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or self.props == "":
            return ""
        html = ""
        for k, v in self.props.items():
            html += f' {k}="{v}"'
        return html

    def __repr__(self):
        return f'HTMLNode({self.tag}, "{self.value}", {self.children}, {self.props})'



class LeafNode(HTMLNode):
    SELF_CLOSING_TAGS = {'img', 'br', 'hr', 'input', 'meta', 'link'}
    
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if not self.tag:
            if not self.value:
                raise ValueError("Text nodes must have a value.")
            return self.value
        if self.tag in self.SELF_CLOSING_TAGS:
            return f"<{self.tag}{self.props_to_html()} />"
        if not self.value:
            raise ValueError(f"Leaf nodes must have a value.\n{self}")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f'LeafNode({self.tag}, "{self.value}", {self.props})'



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag not provided.")
        if not self.children:
            raise ValueError("Missing children.")
        html = ""
        for child in self.children:
            html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html}</{self.tag}>"