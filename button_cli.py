import math

class ButtonCLI(object):
    color: str
    selected: bool
    lit: bool
    height: int
    width: int
    id: int

    def __init__(self, text, color, bright_color, selected, lit, height, width, id):
        self.text = text
        self.color = color
        self.bright_color = bright_color
        self.selected = selected
        self.lit = lit
        self.height = height
        self.width = width
        self.id = id
    
    def get_slices(self):
        slices = []
        # edges
        if self.selected:
            edges1 = '▄'
            edges2 = '█' # '\u001b[37m█\u001b[0m'
            edges3 = '▀'
        else:
            edges1 = ' '
            edges2 = ' '
            edges3 = ' '

        # inside part
        if self.lit:
            color_btn = self.bright_color
        else:
            color_btn = self.color

        for i in range(self.height):
            if i == 0:
                slices.append(edges1*self.width)
            elif i == self.height - 1:
                slices.append(edges3*self.width)
            elif i == math.floor(self.height/2):
                slices.append(edges2 + color_btn + self.text.center(self.width - 2) + '\u001b[0m' + edges2)
            else:
                slices.append(edges2 + color_btn + ' '*(self.width - 2) + '\u001b[0m' + edges2)

        
        return slices