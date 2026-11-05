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


