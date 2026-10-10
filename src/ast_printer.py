from expr import Literal, Binary, Grouping, Unary
from token import Token, TokenType

class AstPrinter:
    def print(self, expression):
        match expression:
            case Literal():
                if expression.literal is None:
                    return "nil" 
                if expression.literal is True:
                    return "true"
                if expression.literal is False:
                    return "false"
                return(str(expression.literal))
            case Unary():
                # Start AI code
                operator = expression.operator.lexeme
                right = self.print(expression.right)
                return f"({operator} {right})"
                # End AI Code
            case Binary():
                expression_left = self.print(expression.left)
                expression_right = self.print(expression.right)
                operator = expression.operator.lexeme
                return f"({operator} {expression_left} {expression_right})"
            case Grouping():
                group = self.print(expression.expression)
                return f"(group {group})"


if __name__ == "__main__":
    printer = AstPrinter()
    minus = Token(TokenType.MINUS, "-", None, 1)
    expression = Binary(Literal(10), minus, Literal(12))
    grouping = Grouping(expression)

    operator = Token(TokenType.GREATER, ">", None, 1)

    test_expression = Literal(25)

    test = Binary(grouping, operator, test_expression)

    result = printer.print(test)
    print(result)
