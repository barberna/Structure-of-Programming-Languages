from token import TokenType
from expr import Literal, Unary, Binary, Grouping
from parse_error import ParseError

"""
expression → equality ;
equality   → comparison ( ( "!=" | "==" ) comparison )* ;
comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term       → factor ( ( "-" | "+" ) factor )* ;
factor     → unary ( ( "/" | "*" ) unary )* ;
unary      → ( "!" | "-" ) unary | primary ;
primary    → NUMBER | STRING | "true" | "false" | "nil"
           | "(" expression ")" ;
"""

class ExpressionParser:
    def __init__(self, stream, lox):
        self.lox = lox
        self.stream = stream

    # --- start AI code ---
    # NUMBER | STRING | "true" | "false" | "nil"
    #      | "(" expression ")" ;
    def primary(self):
        if self.stream.peek().type in (TokenType.NUMBER, TokenType.STRING):
            token = self.stream.advance()
            return Literal(token.literal)

        if self.stream.peek().type == TokenType.FALSE:
            self.stream.advance()
            return Literal(False)
        # --- end AI code ---

        if self.stream.peek().type == TokenType.TRUE:
            self.stream.advance()
            return Literal(True)

        if self.stream.peek().type == TokenType.NIL:
            self.stream.advance()
            return Literal(None)

        if self.stream.peek().type == TokenType.LEFT_PAREN:
            self.stream.advance()

            expression = self.expression()
            
            if self.stream.peek().type != TokenType.RIGHT_PAREN:
                token = self.stream.peek()
                self.lox.error(token.line, "Expected Closing Paren")
                raise ParseError()
                
            self.stream.advance()
            return Grouping(expression)
        
        # --- start AI code ---
        token = self.stream.peek()
        self.lox.error(token.line, "Expected expression.")
        raise ParseError()
        # --- end AI code ---
        

    # ( "!" | "-" ) unary | primary ;
    def unary(self):
        if self.stream.peek().type in (TokenType.BANG, TokenType.MINUS):
            operator = self.stream.advance()
            right = self.unary()
            return Unary(operator, right)
        
        return self.primary()


    # factor → unary ( ( "/" | "*" ) unary )* ;
    def factor(self):
        expression = self.unary()

        while self.stream.peek().type in (TokenType.SLASH, TokenType.STAR):
            operator = self.stream.advance()
            right = self.unary()
            expression = Binary(expression, operator, right)

        return expression
            

    # factor ( ( "-" | "+" ) factor )* ;
    def term(self):
        expression = self.factor()

        while self.stream.peek().type in (TokenType.MINUS, TokenType.PLUS):
            operator = self.stream.advance()
            right = self.factor()
            expression = Binary(expression, operator, right)

        return expression


    # term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    def comparison(self):
        expression = self.term()
        
        while self.stream.peek().type in (TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL):
            operator = self.stream.advance()
            right = self.term()
            expression = Binary(expression, operator, right)

        return expression


    # comparison ( ( "!=" | "==" ) comparison )* ;
    def equality(self):
        expression = self.comparison()
        
        while self.stream.peek().type in (TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.stream.advance()
            right = self.comparison()
            expression = Binary(expression, operator, right)

        return expression

    def expression(self):
        return self.equality()

    def parse(self):
        return self.expression()

    


    