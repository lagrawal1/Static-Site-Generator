class HTMLNode():

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_props = ""
        if self.props == None:
            return html_props
        
        for prop in self.props:
            html_props += f' {prop} = "{self.props[prop]}"'
        return html_props
    
    def __repr__(self):
        return f'Tag: {self.tag} \nValue: {self.value} \nChildren: {self.children}\nProps: {self.props}\n'


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    HTML = ""
    def to_html(self):

        if self.tag == None:
            raise ValueError("All parent nodes must have a tag.")
        if type(self.children) == None:
            raise ValueError("All parent nodes must have children nodes.")
         
        for child in self.children:
            if child.children == None:
                self.HTML += (child.to_html())
            else:
                self.HTML += child.to_html()
        return f"<{self.tag}>{self.HTML}</{self.tag}>"

