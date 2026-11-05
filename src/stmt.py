class Stmt:
    def __init__(self, expression):
        self.expression = expression


class PrintStmt(Stmt):
    def __init__(self, expression):
        super().__init__(expression)


class ExpressionStmt(Stmt):
    def __init__(self, expression):
        super().__init__(expression)

