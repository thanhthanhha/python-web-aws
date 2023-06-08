
class Tree(object):
    def __init__(self, post):
        self.value=post
        self.children=[]
    def add(self, post):
        self.children.append(post)
    