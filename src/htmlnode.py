class HtmlNode: 
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("TBD")
    
    def props_to_html(self):
        properties = ""
        if self.props != None:
            for k, v in self.props.items():
                properties += f' {k}="{v}"'
        return properties

    def __repr__(self):
        return f"TextNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HtmlNode):
    def __init__(self, tag=None, value="", props=None):
        super().__init__(tag=tag,value=value,props=props)

    def to_html(self):
        if self.tag is None: 
            return self.value
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
    

class ParentNode(HtmlNode):
    def __init__(self, tag="", children=[], props=None):
        super().__init__(tag=tag,children=children,props=props)

    def to_html(self):
        if self.tag is None: 
            raise ValueError("Missing tag")
        if len(self.children) == 0: 
            raise ValueError("No children")
        
        props = self.props_to_html()
        html = f"<{self.tag}{props}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html
    