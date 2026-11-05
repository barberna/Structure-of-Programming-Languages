from token import TokenType
from print_parser import PrintParser
from expression_parser import ExpressionParser
from stmt import ExpressionStmt
from parse_error import ParseError

"""
program → statement* EOF ;

statement → exprStmt
    | printStmt ;

exprStmt → expression ";" ;
printStmt → "print" expression ";" ;
"""

"""
TokenStream gives all parsers acces to current parsing indexing

ProgramParser then takes current stream and indexing and facilicates what parser to use
    - current is only print and expression parsing
"""

# Allows for all parsers to fallow the same token list and keep track of current index
class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current]

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def advance(self):
        token = self.peek()
        if not self.is_at_end():
            self.current += 1
        return token

# Directs parsing to correct parser node
class ProgramParser:
    def __init__(self, tokens, lox):
        self.lox = lox
        self.stream = TokenStream(tokens)
        self.expression_parser = ExpressionParser(self.stream, lox)
        self.print_parser = PrintParser(self.stream, self.expression_parser, lox)

    def parse(self):
        statements = []

        # While not end of file loop through the token list and add statments
        while not self.stream.is_at_end():
            try:
                statement = self.parse_statement()
                statements.append(statement)
            # if a Parese error so not pause execution, simply keep advacing to safe point and continue parsing
            except ParseError:
                while not self.stream.is_at_end():
                    if self.stream.peek().type == TokenType.PRINT:
                        break  # Leave 'print' for the next statement.

                    if self.stream.peek().type == TokenType.SEMICOLON:
                        self.stream.advance()  # Consume the boundary.
                        break

                    self.stream.advance()  # Skip an unwanted token

        return statements

    def parse_statement(self):
        if self.stream.peek().type == TokenType.PRINT:
            return self.print_parser.parse()

        expression = self.expression_parser.parse()

        # --- start AI code ---
        if self.stream.peek().type != TokenType.SEMICOLON:
            self.lox.error(self.stream.peek().line, "Expected ';' after expression.")
            raise ParseError()
        # --- end AI code ---

        self.stream.advance()
        return ExpressionStmt(expression)

    