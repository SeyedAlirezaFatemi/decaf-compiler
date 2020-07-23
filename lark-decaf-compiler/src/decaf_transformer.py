from lark import Transformer


class DecafTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.stack_pointer = 0X7fffffff
