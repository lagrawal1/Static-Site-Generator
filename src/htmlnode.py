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
            print(html_props)
        return html_props
    
    def __repr__(self):
        return f'Tag: {self.tag} \nValue: {self.value} \nChildren: {self.children}\nProps: {self.props}\n'



