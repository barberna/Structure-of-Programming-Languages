from expr import Literal, Grouping, Unary, Binary
from token import TokenType
from stmt import ExpressionStmt, PrintStmt

# --- start AI code ---
class EvaluationError(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token
 # --- end AI code ---


class Evaluator:
    # --- start AI code ---
    def is_truthy(self, value):
        if value is None:
            return False
        if type(value) is bool:
            return value
        if type(value) is float:
            return value != 0.0
        return True
    # --- end AI code ---

        # --- start AI code ---
    def is_equal(self, left, right):
        if type(left) in (bool, float) and type(right) in (bool, float):
            return float(left) == float(right)
        if type(left) is not type(right):
            return False
        return left == right
    # --- end AI code ---

        # --- start AI code ---
    def to_number(self, value, operator):
        if value is True:
            return 1.0
        if value is False:
            return 0.0
        if type(value) is float:
            return value

        raise EvaluationError(operator, "Operand must be a number or boolean.")
    # --- end AI code ---

    def evaluate(self, expression):
        # --- start AI code ---
        match expression:
            case Literal():
                return expression.literal
            case Grouping():
                return self.evaluate(expression.expression)
        # --- end AI code ---
            case Unary():
                right = self.evaluate(expression.right)
                if expression.operator.type == TokenType.MINUS:
                    '''if type(right) is not float:
                        raise EvaluationError(
                            expression.operator,
                            "Operand must be a number"
                        )'''
                    return -self.to_number(right, expression.operator)
                
                if expression.operator.type == TokenType.BANG:
                    return not self.is_truthy(right)

                
            case Binary():
                left = self.evaluate(expression.left)
                right = self.evaluate(expression.right)

                if expression.operator.type == TokenType.MINUS:
                    """if type(left) is not float or type(right) is not float:
                        raise EvaluationError(
                            expression.operator,
                            "Operands must be numbers"
                        )"""
                    left_number = self.to_number(left, expression.operator)
                    right_number = self.to_number(right, expression.operator)

                    return left_number - right_number
                
                if expression.operator.type == TokenType.PLUS:
                    """if type(left) is not float or type(right) is not float:
                        raise EvaluationError(
                            expression.operator,
                            "Operands must be numbers"
                        )"""
                    left_number = self.to_number(left, expression.operator)
                    right_number = self.to_number(right, expression.operator)

                    return left_number + right_number
                
                if expression.operator.type == TokenType.STAR:
                    """if type(left) is not float or type(right) is not float:
                        raise EvaluationError(
                            expression.operator,
                            "Operands must be numbers"
                        )"""

                    left_number = self.to_number(left, expression.operator)
                    right_number = self.to_number(right, expression.operator)

                    return left_number * right_number
                
                if expression.operator.type == TokenType.SLASH:
                    """if type(left) is not float or type(right) is not float:
                        raise EvaluationError(
                            expression.operator,
                            "Operands must be numbers"
                        )"""
                    

                    left_number = self.to_number(left, expression.operator)
                    right_number = self.to_number(right, expression.operator)

                    if right_number == 0:
                        raise EvaluationError(
                            expression.operator,
                            "No Divison by Zero"
                        )
                    return left_number / right_number
                
                if expression.operator.type == TokenType.GREATER:
                    '''if type(left) is not float or type(right) is not float:
                        raise EvaluationError(
                            expression.operator,
                            "Operands must be numbers"
                        )'''
                    left_number = self.to_number(left, expression.operator)
                    right_number = self.to_number(right, expression.operator)

                    return left_number > right_number
                
                if expression.operator.type == TokenType.GREATER_EQUAL:
                    """if type(left) is not float or type(right) is not float:
                        raise EvaluationError(
                            expression.operator,
                            "Operands must be numbers"
                        )"""

                    left_number = self.to_number(left, expression.operator)
                    right_number = self.to_number(right, expression.operator)
                    return left_number >= right_number
                
                if expression.operator.type == TokenType.LESS:
                    '''if type(left) is not float or type(right) is not float:
                        raise EvaluationError(
                            expression.operator,
                            "Operands must be numbers"
                        )'''
                    
                    left_number = self.to_number(left, expression.operator)
                    right_number = self.to_number(right, expression.operator)
                    return left_number < right_number
                
                if expression.operator.type == TokenType.LESS_EQUAL:
                    """if type(left) is not float or type(right) is not float:
                        raise EvaluationError(
                            expression.operator,
                            "Operands must be numbers"
                        )"""

                    left_number = self.to_number(left, expression.operator)
                    right_number = self.to_number(right, expression.operator)

                    return left_number <= right_number
                
                if expression.operator.type == TokenType.EQUAL_EQUAL:
                    return self.is_equal(left, right)
                if expression.operator.type == TokenType.BANG_EQUAL:
                    return not self.is_equal(left, right)

    def execute(self, statement):
        match statement:
            case ExpressionStmt():
                self.evaluate(statement.expression)

            case PrintStmt():
                value = self.evaluate(statement.expression)
                match value:
                    case None:
                        print("nil")
                    case True:
                        print("true")
                    case False:
                        print("false")
                    case _:
                        print(value)
        

                

                