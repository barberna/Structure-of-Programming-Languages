from token import Token, TokenType

class Scanner:
    def __init__(self, source, lox):
        self.source = source
        self.lox = lox
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "fun": TokenType.FUN,
        "for": TokenType.FOR,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }

    # Check if current char position is past source length
    def is_at_end(self):
        return self.current >= len(self.source)

    # Add Token to tokens list
    def add_token(self, type: TokenType, literal: object = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    # Advance 1 char position
    def advance(self):
        char = self.source[self.current]
        self.current += 1

        if char == '\n':
            self.line += 1

        return char

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def match(self, c: str):
        if self.is_at_end():
            return False

        if self.source[self.current] != c:
            return False

        self.current += 1
        return True

    def string(self):
        # Start AI code
        while not self.is_at_end() and self.peek() != '"':
            self.advance()

        # --- start AI code ---
        if self.is_at_end():
            self.lox.error(self.line, "Unterminated string")
            return
        # --- end AI code ---

        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)
        # End AI code

    def number(self):

        while not self.is_at_end() and '0' <= self.peek() <= '9':
            self.advance()

        # --- start AI code ---
        # Include a decimal point only when a digit follows it.
        if (self.peek() == '.'
                and self.current + 1 < len(self.source)
                and '0' <= self.source[self.current + 1] <= '9'):
            self.advance()
            while not self.is_at_end() and '0' <= self.peek() <= '9':
                self.advance()
        # --- end AI code ---

        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    def identifier(self):
        while ( 'a' <= self.peek() <= 'z'
               or 'A' <= self.peek() <= 'Z'
               or '0' <= self.peek() <= '9'
               or self.peek() == '_' ):
            self.advance()

        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)
        

    # Scan token list and add token 
    def scan_token(self, c):
        match c:
            # Single Char token cases
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ',': self.add_token(TokenType.COMMA)
            case '.': self.add_token(TokenType.DOT)
            case '-': self.add_token(TokenType.MINUS)
            case '+': self.add_token(TokenType.PLUS)
            case ';': self.add_token(TokenType.SEMICOLON)
            case '*': self.add_token(TokenType.STAR)

            # One or two char tokens
            case '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            case '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)

            # Literals
            case '"': self.string()
            case _ if '0' <= c <= '9': self.number()
            case _ if ('a' <= c <= 'z') or ('A' <= c <= 'Z'): self.identifier()

            # Ignore whitespace.
            case ' ' | '\r' | '\t' | '\n':
                pass

            # Commenting
            case '/':
                if self.match('/'):
                    # --- start AI code ---
                    while not self.is_at_end() and self.peek() != '\n':
                        self.advance()
                    # --- end AI code ---
                else:
                    self.add_token(TokenType.SLASH)
            # Lox creates Scanner -> Scanner -> reports errors back to lox
            # This is why Scanner needs to take in lox. We call Scanner(source, self) in lox
            case _: self.lox.error(self.line, "Unexpected Character")

            
    # While not at at end, 
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token(self.advance())

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    