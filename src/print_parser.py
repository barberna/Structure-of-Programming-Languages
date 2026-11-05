from token import TokenType
from parse_error import ParseError
from stmt import PrintStmt
"""
- From program we will be directed if token == print
- We will then run the expression token list through the expression parser
- we will then link the expression output to the print statment and print the expression to the user
"""
class PrintParser:
    def __init__(self, stream, expression_parser, lox):
        self.stream = stream
        self.expression_parser = expression_parser
        self.lox = lox

    def parse(self):
        self.stream.advance()
        
        if self.stream.peek().type == TokenType.SEMICOLON:
            self.lox.error(self.stream.peek().line, "Expected expression before ';'.")
            raise ParseError()

        expression = self.expression_parser.parse()

        # --- start AI code ---
        if self.stream.peek().type != TokenType.SEMICOLON:
            self.lox.error(self.stream.peek().line, "Expected ';' after expression.")
            raise ParseError()
        # --- end AI code ---

        self.stream.advance()
        return PrintStmt(expression)
