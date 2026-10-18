from ast_printer import AstPrinter
from token import Token, TokenType
from expr import Literal, Binary, Grouping, Unary
# Create three test cases for the AST, add them to the a list then iterate each test through the printer

# This test uses grouping, binary, literal and operator(-,<)
#  (10 - 12) < 25
def test1():
    printer = AstPrinter()

    # Left Expression
    minus = Token(TokenType.MINUS, "-", None, 1)
    grouping = Binary(Literal(10), minus, Literal(12))
    left_expression = Grouping(grouping)

    # operator
    operator = Token(TokenType.LESS, "<", None, 1)

    # Right Exprssion
    right_expression = Literal(25)

    test = Binary(left_expression, operator, right_expression)

    result = printer.print(test)
    return(result)

# This tests literal(Number, False), unary, binary, operator(!,==)
# !15 == false
def test2():
    printer = AstPrinter()

    # Left Expression
    bang = Token(TokenType.BANG, "!", None, 1)
    unary_expression = Literal(15)
    left_expression = Unary(bang, unary_expression)

    # Operator
    operator = Token(TokenType.EQUAL_EQUAL, "==", None, 1)

    # Right Expression
    right_expression = Literal(False)
    
    test = Binary(left_expression, operator, right_expression)

    result = printer.print(test)
    return(result)

# Test unary, literal, grouping, operator(+,*,>=)
# (12 * 12) >= (12 + 12)
def test3():
    printer = AstPrinter()

    # Left Expression
    minus = Token(TokenType.STAR, "*", None, 1)
    grouping = Binary(Literal(12), minus, Literal(12))
    left_expression = Grouping(grouping)

    # Operator
    operator = Token(TokenType.GREATER_EQUAL, ">=", None, 1)

    # Right Expression
    minus = Token(TokenType.PLUS, "+", None, 1)
    grouping = Binary(Literal(12), minus, Literal(12))
    right_expression = Grouping(grouping)

    test = Binary(left_expression, operator, right_expression)

    result = printer.print(test)
    return(result)

# Testing, bianry, literal(true), operator(!=, ==), Grouping.
# ()"Testing" != "Test") == True
def test4():
    printer = AstPrinter()

    left_group_expression = Literal('Testing')
    bang_equal = Token(TokenType.BANG_EQUAL, "!=", None, 1)
    right_group_expression = Literal("Test")
    group  = Binary(left_group_expression, bang_equal, right_group_expression)

    left_expression = Grouping(group)
    operator = Token(TokenType.EQUAL_EQUAL, "==", None, 1)

    right_expression = Literal(True)

    test = Binary(left_expression, operator, right_expression)
    result = printer.print(test)
    return(result)

# Testing Unary, Binary, Grouping, Literal(None), and operators(-, /, >, <=).
# ((-45.67 / 2) > 0) <= nil
# --- start AI code ---
def test5():
    printer = AstPrinter()

    negative = Unary(
        Token(TokenType.MINUS, "-", None, 1),
        Literal(45.67),
    )

    division = Binary(
        negative,
        Token(TokenType.SLASH, "/", None, 1),
        Literal(2),
    )

    comparison = Binary(
        Grouping(division),
        Token(TokenType.GREATER, ">", None, 1),
        Literal(0),
    )

    expression = Binary(
        Grouping(comparison),
        Token(TokenType.LESS_EQUAL, "<=", None, 1),
        Literal(None),
    )

    return printer.print(expression)
# --- end AI code ---

if __name__ == "__main__":
    tests = [test1(), test2(), test3(), test4(), test5()]
    for i, test in enumerate(tests, start=1):
        print(f"Test{i}: {test}")
