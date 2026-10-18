from token import TokenType
from expr import Literal, Unary, Binary, Grouping

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

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens, lox):
        self.lox = lox
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


    # --- start AI code ---
    # NUMBER | STRING | "true" | "false" | "nil"
    #      | "(" expression ")" ;
    def primary(self):
        if self.peek().type in (TokenType.NUMBER, TokenType.STRING):
            token = self.advance()
            return Literal(token.literal)

        if self.peek().type == TokenType.FALSE:
            self.advance()
            return Literal(False)
        # --- end AI code ---

        if self.peek().type == TokenType.TRUE:
            self.advance()
            return Literal(True)

        if self.peek().type == TokenType.NIL:
            self.advance()
            return Literal(None)

        if self.peek().type == TokenType.LEFT_PAREN:
            self.advance()

            expression = self.expression()
            
            if self.peek().type != TokenType.RIGHT_PAREN:
                token = self.peek()
                self.lox.error(token.line, "Expected Closing Paren")
                raise ParseError()
                
            self.advance()
            return Grouping(expression)
        
        # --- start AI code ---
        token = self.peek()
        self.lox.error(token.line, "Expected expression.")
        raise ParseError()
        # --- end AI code ---
        

    # ( "!" | "-" ) unary | primary ;
    def unary(self):
        if self.peek().type in (TokenType.BANG, TokenType.MINUS):
            operator = self.advance()
            right = self.unary()
            return Unary(operator, right)
        
        return self.primary()


    # factor → unary ( ( "/" | "*" ) unary )* ;
    def factor(self):
        expression = self.unary()

        while self.peek().type in (TokenType.SLASH, TokenType.STAR):
            operator = self.advance()
            right = self.unary()
            expression = Binary(expression, operator, right)

        return expression
            

    # factor ( ( "-" | "+" ) factor )* ;
    def term(self):
        expression = self.factor()

        while self.peek().type in (TokenType.MINUS, TokenType.PLUS):
            operator = self.advance()
            right = self.factor()
            expression = Binary(expression, operator, right)

        return expression


    # term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    def comparison(self):
        expression = self.term()
        
        while self.peek().type in (TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL):
            operator = self.advance()
            right = self.term()
            expression = Binary(expression, operator, right)

        return expression


    # comparison ( ( "!=" | "==" ) comparison )* ;
    def equality(self):
        expression = self.comparison()
        
        while self.peek().type in (TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.advance()
            right = self.comparison()
            expression = Binary(expression, operator, right)

        return expression

    def expression(self):
        return self.equality()

    def parse(self):
        try:
            expression = self.expression()

            # --- start AI code ---
            if not self.is_at_end():
                token = self.peek()
                self.lox.error(
                    token.line,
                    f"Unexpected token '{token.lexeme}' after expression."
                )
                raise ParseError()

            return expression
            # --- End AI code ---

        except ParseError:
            return None

    


    