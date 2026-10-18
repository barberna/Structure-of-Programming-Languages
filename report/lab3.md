# CIS 343 Parser Lab 3

Language Name: PLox

## Expression Grammar

```text
expression -> equality ;
equality   -> comparison ( ( "!=" | "==" ) comparison )* ;
comparison -> term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term       -> factor ( ( "-" | "+" ) factor )* ;
factor     -> unary ( ( "/" | "*" ) unary )* ;
unary      -> ( "!" | "-" ) unary | primary ;
primary    -> NUMBER | STRING | "true" | "false" | "nil"
           | "(" expression ")" ;
```

The `|` symbol means an alternative, and `*` outside quotation marks means zero or more repetitions. The parser accepts one complete expression followed by EOF per source file or interactive input. A semicolon is not required or accepted.

### Precedence and associativity

The following levels are listed from lowest to highest precedence:

| Level | Operators or forms | Associativity |
|---|---|---|
| Equality | `==`, `!=` | Left |
| Comparison | `>`, `>=`, `<`, `<=` | Left |
| Term | `+`, `-` | Left |
| Factor | `*`, `/` | Left |
| Unary | `!`, unary `-` | Right |
| Primary | Literals and parenthesized expressions | Parentheses explicitly group an expression |

For example, `1 + 2 * 3` groups as `1 + (2 * 3)`, while `8 - 3 - 1` groups as `(8 - 3) - 1`. Recursive unary parsing makes `!!false` group as `!(!false)`.

## Design choices relative to Lox

PLox retains Lox-style number, string, boolean, and nil literals, arithmetic operators, comparison operators, equality operators, unary operators, and grouping. Logical `and` and `or` are not implemented for this lab. No additional expression operators were added.

The parser uses recursive descent. Each grammar rule has a corresponding method in `Parser`. Binary rules use a loop that builds a new `Binary` node with the previous expression as its left child. This preserves left associativity. The unary rule calls itself for its operand, and the primary rule handles literals and grouping.

The scanner, `Token` and `TokenType`, AST classes, and AST printer are reused from the previous labs. The four AST classes remain `Literal`, `Unary`, `Binary`, and `Grouping`. Grammar levels such as `term` and `factor` do not require separate AST classes. The printer uses Python match/case instead of the textbook's Visitor pattern and produces parenthesized prefix notation. Numeric values are floats, so an input such as `2` prints as `2.0`. Python `True`, `False`, and `None` print as `true`, `false`, and `nil`.

### Grammar changes since Lab 2

Lab 2 used `expression -> literal | unary | binary | grouping` with `binary -> expression operator expression`. That grammar described expression forms but did not determine precedence or associativity. It also could not be translated directly into recursive descent because the binary rule could recurse without consuming a token.

Lab 3 splits binary parsing into equality, comparison, term, and factor levels. The `primary` rule combines literals and grouping. The unary operand is now another unary expression rather than an unrestricted expression. These changes keep the same literal and operator vocabulary while defining an unambiguous order of operations.

## Scanner, parser, and printer integration

`PLox.run()` resets the error flag, echoes the source, and asks the scanner for tokens. If scanning reports an error, it stops before parsing. Otherwise, `Parser.parse()` produces the AST. If parsing succeeds, `AstPrinter` displays the tree. Both file mode and interactive mode use this same method.

The parser reports errors through `PLox.error()`, which prints a line number to standard error and sets `had_error`. A `ParseError` stops the parse and is caught in `parse()`. A missing operand or unexpected primary token reports `Expected expression.`; a missing closing parenthesis reports `Expected Closing Paren`. After parsing the expression, the parser checks EOF and rejects unexpected trailing tokens. Invalid inputs in the tests below print no AST and produce no unhandled Python exception. Interactive mode resets for the next input.

## Dependency/setup instructions

Python 3.10 or newer is required because the AST printer uses match/case. No third-party packages are required. These results were captured with Python 3.12.14. A virtual environment is optional.

Open PowerShell in the repository root, which contains `src`, `test`, and `report`:

```powershell
python --version
python src/plox.py
```

Run one source-file test:

```powershell
python src/plox.py test/lab3/19_precedence.plx
```

Run the automated verification script, which checks source echoes, AST output, exact errors, absence of extra output, and interactive recovery:

```powershell
python test/lab3/run_tests.py
```

The script uses only Python's standard library and exits with an assertion failure if a result differs from expectations. Its final success message is `All 43 file tests and interactive recovery passed.`. The script is AI-generated and marked accordingly.

Alternatively, display all 43 saved input files in filename order:

```powershell
# --- start AI code ---
Get-ChildItem test/lab3/*.plx | Sort-Object Name | ForEach-Object {
    Write-Output ("Test: " + $_.Name)
    python src/plox.py $_.FullName
}
# --- end AI code ---
```

The loop displays results for comparison with the expected outputs below; it does not automatically assert pass/fail. No PYTHONPATH configuration is necessary for these commands. The source file must contain one expression, although that expression can span multiple lines. Each interactive input is one line. Exit interactive mode with Ctrl+C or end-of-input.

## Testing

The 43 test inputs are saved under `test/lab3/`. They cover all five literal types, every supported operator, all four AST forms, precedence, associativity, nested grouping, syntax errors, lexical errors, line numbers, comments, and source-file mode. A separate interactive sequence tests recovery after errors.

All 43 file tests and the interactive recovery sequence matched their expected outputs during verification. The actual output blocks below were captured from the program. Standard output includes the source echo; standard error is shown separately so its ordering does not depend on terminal buffering. Each expected error includes its required line number. An empty file is represented explicitly in its source section.

### Test 1: Decimal number literal

File: [`01_literals_number.plx`](../test/lab3/01_literals_number.plx)

Purpose: Decimal number literal.

Source input:

```text
45.67
```

Expected AST output (after the source echo):

```text
45.67
```

Expected standard error: none.

Actual standard output:

```text
45.67
45.67
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 2: String literal

File: [`02_literals_string.plx`](../test/lab3/02_literals_string.plx)

Purpose: String literal.

Source input:

```text
"hello"
```

Expected AST output (after the source echo):

```text
hello
```

Expected standard error: none.

Actual standard output:

```text
"hello"
hello
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 3: True literal

File: [`03_literals_true.plx`](../test/lab3/03_literals_true.plx)

Purpose: True literal.

Source input:

```text
true
```

Expected AST output (after the source echo):

```text
true
```

Expected standard error: none.

Actual standard output:

```text
true
true
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 4: False literal

File: [`04_literals_false.plx`](../test/lab3/04_literals_false.plx)

Purpose: False literal.

Source input:

```text
false
```

Expected AST output (after the source echo):

```text
false
```

Expected standard error: none.

Actual standard output:

```text
false
false
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 5: Nil literal

File: [`05_literals_nil.plx`](../test/lab3/05_literals_nil.plx)

Purpose: Nil literal.

Source input:

```text
nil
```

Expected AST output (after the source echo):

```text
nil
```

Expected standard error: none.

Actual standard output:

```text
nil
nil
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 6: Binary addition

File: [`06_addition.plx`](../test/lab3/06_addition.plx)

Purpose: Binary addition.

Source input:

```text
1 + 2
```

Expected AST output (after the source echo):

```text
(+ 1.0 2.0)
```

Expected standard error: none.

Actual standard output:

```text
1 + 2
(+ 1.0 2.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 7: Binary subtraction

File: [`07_subtraction.plx`](../test/lab3/07_subtraction.plx)

Purpose: Binary subtraction.

Source input:

```text
5 - 3
```

Expected AST output (after the source echo):

```text
(- 5.0 3.0)
```

Expected standard error: none.

Actual standard output:

```text
5 - 3
(- 5.0 3.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 8: Binary multiplication

File: [`08_multiplication.plx`](../test/lab3/08_multiplication.plx)

Purpose: Binary multiplication.

Source input:

```text
2 * 3
```

Expected AST output (after the source echo):

```text
(* 2.0 3.0)
```

Expected standard error: none.

Actual standard output:

```text
2 * 3
(* 2.0 3.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 9: Binary division

File: [`09_division.plx`](../test/lab3/09_division.plx)

Purpose: Binary division.

Source input:

```text
8 / 2
```

Expected AST output (after the source echo):

```text
(/ 8.0 2.0)
```

Expected standard error: none.

Actual standard output:

```text
8 / 2
(/ 8.0 2.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 10: Unary negation

File: [`10_negation.plx`](../test/lab3/10_negation.plx)

Purpose: Unary negation.

Source input:

```text
-5
```

Expected AST output (after the source echo):

```text
(- 5.0)
```

Expected standard error: none.

Actual standard output:

```text
-5
(- 5.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 11: Unary logical not

File: [`11_not.plx`](../test/lab3/11_not.plx)

Purpose: Unary logical not.

Source input:

```text
!true
```

Expected AST output (after the source echo):

```text
(! true)
```

Expected standard error: none.

Actual standard output:

```text
!true
(! true)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 12: Stacked unary operators

File: [`12_stacked_unary.plx`](../test/lab3/12_stacked_unary.plx)

Purpose: Stacked unary operators.

Source input:

```text
!!false
```

Expected AST output (after the source echo):

```text
(! (! false))
```

Expected standard error: none.

Actual standard output:

```text
!!false
(! (! false))
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 13: Equality

File: [`13_equal.plx`](../test/lab3/13_equal.plx)

Purpose: Equality.

Source input:

```text
2 == 2
```

Expected AST output (after the source echo):

```text
(== 2.0 2.0)
```

Expected standard error: none.

Actual standard output:

```text
2 == 2
(== 2.0 2.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 14: Inequality

File: [`14_not_equal.plx`](../test/lab3/14_not_equal.plx)

Purpose: Inequality.

Source input:

```text
2 != 3
```

Expected AST output (after the source echo):

```text
(!= 2.0 3.0)
```

Expected standard error: none.

Actual standard output:

```text
2 != 3
(!= 2.0 3.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 15: Greater than

File: [`15_greater.plx`](../test/lab3/15_greater.plx)

Purpose: Greater than.

Source input:

```text
3 > 2
```

Expected AST output (after the source echo):

```text
(> 3.0 2.0)
```

Expected standard error: none.

Actual standard output:

```text
3 > 2
(> 3.0 2.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 16: Greater than or equal

File: [`16_greater_equal.plx`](../test/lab3/16_greater_equal.plx)

Purpose: Greater than or equal.

Source input:

```text
3 >= 3
```

Expected AST output (after the source echo):

```text
(>= 3.0 3.0)
```

Expected standard error: none.

Actual standard output:

```text
3 >= 3
(>= 3.0 3.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 17: Less than

File: [`17_less.plx`](../test/lab3/17_less.plx)

Purpose: Less than.

Source input:

```text
2 < 3
```

Expected AST output (after the source echo):

```text
(< 2.0 3.0)
```

Expected standard error: none.

Actual standard output:

```text
2 < 3
(< 2.0 3.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 18: Less than or equal

File: [`18_less_equal.plx`](../test/lab3/18_less_equal.plx)

Purpose: Less than or equal.

Source input:

```text
2 <= 2
```

Expected AST output (after the source echo):

```text
(<= 2.0 2.0)
```

Expected standard error: none.

Actual standard output:

```text
2 <= 2
(<= 2.0 2.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 19: Multiplication binds before addition

File: [`19_precedence.plx`](../test/lab3/19_precedence.plx)

Purpose: Multiplication binds before addition.

Source input:

```text
1 + 2 * 3
```

Expected AST output (after the source echo):

```text
(+ 1.0 (* 2.0 3.0))
```

Expected standard error: none.

Actual standard output:

```text
1 + 2 * 3
(+ 1.0 (* 2.0 3.0))
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 20: Parentheses override precedence

File: [`20_grouping.plx`](../test/lab3/20_grouping.plx)

Purpose: Parentheses override precedence.

Source input:

```text
(1 + 2) * 3
```

Expected AST output (after the source echo):

```text
(* (group (+ 1.0 2.0)) 3.0)
```

Expected standard error: none.

Actual standard output:

```text
(1 + 2) * 3
(* (group (+ 1.0 2.0)) 3.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 21: Nested grouping

File: [`21_nested_grouping.plx`](../test/lab3/21_nested_grouping.plx)

Purpose: Nested grouping.

Source input:

```text
((1 + 2))
```

Expected AST output (after the source echo):

```text
(group (group (+ 1.0 2.0)))
```

Expected standard error: none.

Actual standard output:

```text
((1 + 2))
(group (group (+ 1.0 2.0)))
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 22: Subtraction associates left

File: [`22_subtraction_associativity.plx`](../test/lab3/22_subtraction_associativity.plx)

Purpose: Subtraction associates left.

Source input:

```text
8 - 3 - 1
```

Expected AST output (after the source echo):

```text
(- (- 8.0 3.0) 1.0)
```

Expected standard error: none.

Actual standard output:

```text
8 - 3 - 1
(- (- 8.0 3.0) 1.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 23: Division associates left

File: [`23_division_associativity.plx`](../test/lab3/23_division_associativity.plx)

Purpose: Division associates left.

Source input:

```text
16 / 4 / 2
```

Expected AST output (after the source echo):

```text
(/ (/ 16.0 4.0) 2.0)
```

Expected standard error: none.

Actual standard output:

```text
16 / 4 / 2
(/ (/ 16.0 4.0) 2.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 24: Unary binds before multiplication

File: [`24_unary_precedence.plx`](../test/lab3/24_unary_precedence.plx)

Purpose: Unary binds before multiplication.

Source input:

```text
-2 * 3
```

Expected AST output (after the source echo):

```text
(* (- 2.0) 3.0)
```

Expected standard error: none.

Actual standard output:

```text
-2 * 3
(* (- 2.0) 3.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 25: Arithmetic binds before comparison

File: [`25_comparison_precedence.plx`](../test/lab3/25_comparison_precedence.plx)

Purpose: Arithmetic binds before comparison.

Source input:

```text
1 + 2 < 4
```

Expected AST output (after the source echo):

```text
(< (+ 1.0 2.0) 4.0)
```

Expected standard error: none.

Actual standard output:

```text
1 + 2 < 4
(< (+ 1.0 2.0) 4.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 26: Comparison binds before equality

File: [`26_equality_precedence.plx`](../test/lab3/26_equality_precedence.plx)

Purpose: Comparison binds before equality.

Source input:

```text
1 < 2 == true
```

Expected AST output (after the source echo):

```text
(== (< 1.0 2.0) true)
```

Expected standard error: none.

Actual standard output:

```text
1 < 2 == true
(== (< 1.0 2.0) true)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 27: Comparison associates left

File: [`27_comparison_associativity.plx`](../test/lab3/27_comparison_associativity.plx)

Purpose: Comparison associates left.

Source input:

```text
1 < 2 < 3
```

Expected AST output (after the source echo):

```text
(< (< 1.0 2.0) 3.0)
```

Expected standard error: none.

Actual standard output:

```text
1 < 2 < 3
(< (< 1.0 2.0) 3.0)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 28: Equality associates left

File: [`28_equality_associativity.plx`](../test/lab3/28_equality_associativity.plx)

Purpose: Equality associates left.

Source input:

```text
true == false != nil
```

Expected AST output (after the source echo):

```text
(!= (== true false) nil)
```

Expected standard error: none.

Actual standard output:

```text
true == false != nil
(!= (== true false) nil)
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Test 29: Missing right operand after +

File: [`29_missing_right.plx`](../test/lab3/29_missing_right.plx)

Purpose: Missing right operand after +.

Source input:

```text
1 +
```

Expected standard error:

```text
[Line: 1] Error: Expected expression.
```

Expected AST output: none.

Actual standard output:

```text
1 +
```

Actual standard error:

```text
[Line: 1] Error: Expected expression.
```

Result: **Pass** - actual output matches the expected result.

### Test 30: Missing left operand: * cannot begin an expression

File: [`30_missing_left.plx`](../test/lab3/30_missing_left.plx)

Purpose: Missing left operand: * cannot begin an expression.

Source input:

```text
* 2
```

Expected standard error:

```text
[Line: 1] Error: Expected expression.
```

Expected AST output: none.

Actual standard output:

```text
* 2
```

Actual standard error:

```text
[Line: 1] Error: Expected expression.
```

Result: **Pass** - actual output matches the expected result.

### Test 31: Missing operand after unary !

File: [`31_missing_unary_operand.plx`](../test/lab3/31_missing_unary_operand.plx)

Purpose: Missing operand after unary !.

Source input:

```text
!
```

Expected standard error:

```text
[Line: 1] Error: Expected expression.
```

Expected AST output: none.

Actual standard output:

```text
!
```

Actual standard error:

```text
[Line: 1] Error: Expected expression.
```

Result: **Pass** - actual output matches the expected result.

### Test 32: Opening parenthesis has no closing parenthesis

File: [`32_missing_close.plx`](../test/lab3/32_missing_close.plx)

Purpose: Opening parenthesis has no closing parenthesis.

Source input:

```text
(1 + 2
```

Expected standard error:

```text
[Line: 1] Error: Expected Closing Paren
```

Expected AST output: none.

Actual standard output:

```text
(1 + 2
```

Actual standard error:

```text
[Line: 1] Error: Expected Closing Paren
```

Result: **Pass** - actual output matches the expected result.

### Test 33: Closing parenthesis has no matching opening parenthesis

File: [`33_extra_close.plx`](../test/lab3/33_extra_close.plx)

Purpose: Closing parenthesis has no matching opening parenthesis.

Source input:

```text
1 + 2)
```

Expected standard error:

```text
[Line: 1] Error: Unexpected token ')' after expression.
```

Expected AST output: none.

Actual standard output:

```text
1 + 2)
```

Actual standard error:

```text
[Line: 1] Error: Unexpected token ')' after expression.
```

Result: **Pass** - actual output matches the expected result.

### Test 34: Empty group has no expression

File: [`34_empty_group.plx`](../test/lab3/34_empty_group.plx)

Purpose: Empty group has no expression.

Source input:

```text
()
```

Expected standard error:

```text
[Line: 1] Error: Expected expression.
```

Expected AST output: none.

Actual standard output:

```text
()
```

Actual standard error:

```text
[Line: 1] Error: Expected expression.
```

Result: **Pass** - actual output matches the expected result.

### Test 35: Unexpected * where an operand is required

File: [`35_unexpected_operator.plx`](../test/lab3/35_unexpected_operator.plx)

Purpose: Unexpected * where an operand is required.

Source input:

```text
1 + * 2
```

Expected standard error:

```text
[Line: 1] Error: Expected expression.
```

Expected AST output: none.

Actual standard output:

```text
1 + * 2
```

Actual standard error:

```text
[Line: 1] Error: Expected expression.
```

Result: **Pass** - actual output matches the expected result.

### Test 36: Identifiers are outside the expression grammar

File: [`36_identifier.plx`](../test/lab3/36_identifier.plx)

Purpose: Identifiers are outside the expression grammar.

Source input:

```text
name
```

Expected standard error:

```text
[Line: 1] Error: Expected expression.
```

Expected AST output: none.

Actual standard output:

```text
name
```

Actual standard error:

```text
[Line: 1] Error: Expected expression.
```

Result: **Pass** - actual output matches the expected result.

### Test 37: Second literal is an unexpected trailing token

File: [`37_trailing_literal.plx`](../test/lab3/37_trailing_literal.plx)

Purpose: Second literal is an unexpected trailing token.

Source input:

```text
1 2
```

Expected standard error:

```text
[Line: 1] Error: Unexpected token '2' after expression.
```

Expected AST output: none.

Actual standard output:

```text
1 2
```

Actual standard error:

```text
[Line: 1] Error: Unexpected token '2' after expression.
```

Result: **Pass** - actual output matches the expected result.

### Test 38: Semicolons are not part of the expression grammar

File: [`38_semicolon.plx`](../test/lab3/38_semicolon.plx)

Purpose: Semicolons are not part of the expression grammar.

Source input:

```text
1;
```

Expected standard error:

```text
[Line: 1] Error: Unexpected token ';' after expression.
```

Expected AST output: none.

Actual standard output:

```text
1;
```

Actual standard error:

```text
[Line: 1] Error: Unexpected token ';' after expression.
```

Result: **Pass** - actual output matches the expected result.

### Test 39: Empty input has no expression

File: [`39_empty_input.plx`](../test/lab3/39_empty_input.plx)

Purpose: Empty input has no expression.

Source input:

Empty file (zero characters).

Expected standard error:

```text
[Line: 1] Error: Expected expression.
```

Expected AST output: none.

Actual standard output: one blank line from echoing the empty source; no AST.

Actual standard error:

```text
[Line: 1] Error: Expected expression.
```

Result: **Pass** - actual output matches the expected result.

### Test 40: Unexpected @ character prevents parsing

File: [`40_lexical_error.plx`](../test/lab3/40_lexical_error.plx)

Purpose: Unexpected @ character prevents parsing.

Source input:

```text
1 @
```

Expected standard error:

```text
[Line: 1] Error: Unexpected Character
```

Expected AST output: none.

Actual standard output:

```text
1 @
```

Actual standard error:

```text
[Line: 1] Error: Unexpected Character
```

Result: **Pass** - actual output matches the expected result.

### Test 41: String is missing its closing quote

File: [`41_unterminated_string.plx`](../test/lab3/41_unterminated_string.plx)

Purpose: String is missing its closing quote.

Source input:

```text
"hello
```

Expected standard error:

```text
[Line: 1] Error: Unterminated string
```

Expected AST output: none.

Actual standard output:

```text
"hello
```

Actual standard error:

```text
[Line: 1] Error: Unterminated string
```

Result: **Pass** - actual output matches the expected result.

### Test 42: Invalid operand on line 2 tests diagnostic location

File: [`42_line_number.plx`](../test/lab3/42_line_number.plx)

Purpose: Invalid operand on line 2 tests diagnostic location.

Source input:

```text
1 +
* 2
```

Expected standard error:

```text
[Line: 2] Error: Expected expression.
```

Expected AST output: none.

Actual standard output:

```text
1 +
* 2
```

Actual standard error:

```text
[Line: 2] Error: Expected expression.
```

Result: **Pass** - actual output matches the expected result.

### Test 43: Multiline expression with leading and trailing comments

File: [`43_comments.plx`](../test/lab3/43_comments.plx)

Purpose: Multiline expression with leading and trailing comments.

Source input:

```text
// A comment before the expression
1 +
2 * 3 // A comment after the expression
```

Expected AST output (after the source echo):

```text
(+ 1.0 (* 2.0 3.0))
```

Expected standard error: none.

Actual standard output:

```text
// A comment before the expression
1 +
2 * 3 // A comment after the expression
(+ 1.0 (* 2.0 3.0))
```

Actual standard error: none.

Result: **Pass** - actual output matches the expected result.

### Interactive mode and recovery

Start `python src/plox.py` and enter these six lines in the same session:

```text
1 +
2 * 3
@
!false
(1 + 2
(1 + 2) * 3
```

| Step | Purpose | Expected result | Actual result | Match |
|---|---|---|---|---|
| 1 | Missing operand after `+` | `[Line: 1] Error: Expected expression.`; no AST | Same diagnostic; no AST | Pass |
| 2 | Valid input after syntax error | `(* 2.0 3.0)` | `(* 2.0 3.0)` | Pass |
| 3 | Unexpected character | `[Line: 1] Error: Unexpected Character`; no AST | Same diagnostic; no AST | Pass |
| 4 | Valid input after lexical error | `(! false)` | `(! false)` | Pass |
| 5 | Missing closing parenthesis | `[Line: 1] Error: Expected Closing Paren`; no AST | Same diagnostic; no AST | Pass |
| 6 | Valid grouped input after error | `(* (group (+ 1.0 2.0)) 3.0)` | `(* (group (+ 1.0 2.0)) 3.0)` | Pass |

Actual captured standard output, including the banner, prompts, and source echo:

```text
>>>>> PLox Interactive Shell <<<<<
>1 +
>2 * 3
(* 2.0 3.0)
>@
>!false
(! false)
>(1 + 2
>(1 + 2) * 3
(* (group (+ 1.0 2.0)) 3.0)
>
```

Actual captured standard error:

```text
[Line: 1] Error: Expected expression.
[Line: 1] Error: Unexpected Character
[Line: 1] Error: Expected Closing Paren
```

The same running process accepted all six inputs and exited normally at end-of-input. Each new input restarts scanning at line 1. The capture feeds the listed lines through standard input; the same sequence can be entered manually with the command above.

## Concrete syntax tree and printed AST

Test 19 uses the source `1 + 2 * 3`. The diagram below is a concrete syntax tree for the expression grammar. Every nonterminal level is included. The term rule uses one repetition for `+ factor`; the second factor uses one repetition for `* unary`. All other binary repetitions occur zero times. NUMBER leaves retain their source lexemes.

```text
expression
`-- equality
    `-- comparison
        `-- term
            |-- factor
            |   `-- unary
            |       `-- primary
            |           `-- NUMBER: 1
            |-- "+"
            `-- factor
                |-- unary
                |   `-- primary
                |       `-- NUMBER: 2
                |-- "*"
                `-- unary
                    `-- primary
                        `-- NUMBER: 3
```

The parser separately requires EOF after this complete expression; EOF is not a production in the expression grammar itself.

Actual program AST output:

```text
(+ 1.0 (* 2.0 3.0))
```

The AST removes grammar-only levels such as equality, comparison, term, factor, and primary. Its root is a `Binary` node for `+`, with `Literal(1.0)` on the left and a `Binary` node for `*` on the right. The multiplication node contains `Literal(2.0)` and `Literal(3.0)`. Multiplication is nested inside the addition's right operand because factor has higher precedence than term. The printer visits this structure recursively and produces the prefix output above. There is no `Grouping` node because the source contains no parentheses.

## Known limitations and failing tests

- None of the 43 documented source-file tests or the interactive recovery checks failed.
- This lab constructs and prints an AST; it does not evaluate expressions or check operand types. For example, chained comparisons can be parsed without determining whether their operand types would be valid at runtime.
- Variables, assignment, function calls, statements, logical `and`/`or`, comma operators, and ternary operators are not supported by this expression grammar.
- Diagnostics include line numbers but not column numbers. Missing-operand messages do not identify a specific operator or token; trailing-token diagnostics do include the unexpected lexeme.
- The recursive parser and printer do not impose an explicit depth limit or catch Python `RecursionError`; extremely deep expressions can exceed Python's recursion limit. The documented tests use ordinary expression sizes and do not establish arbitrary-depth safety.
- String values print without quotation marks, so the string `"true"` and boolean `true` have the same displayed text. Strings do not support escape sequences.
- Only `//` comments are supported. Numbers are floating-point values without scientific notation; large values may lose precision.
- Interactive input is limited to one line per expression. File mode supports multiline expressions.
- File mode currently does not return a nonzero process status for lexical or syntax errors. Error output and absence of an AST must be checked instead of relying only on the exit status.

## Extra credit

No extra credit is requested. Missing left operands are rejected by the normal primary-expression error handling; no specialized extra-credit diagnostic or additional operator is claimed.

## AI assistance

AI assistance was used during parser development, test-input preparation, and report preparation. The report's concrete test results were captured by running the current implementation. AI-provided Python code must be enclosed with `# --- start AI code ---` and `# --- end AI code ---` in the source files, following the lab policy with Python comment syntax. The AI-provided PowerShell loop above is marked as well. A report acknowledgment does not replace source-code attribution.

## Submission

The submitted commit must include all implementation files under `src/`, all 43 test inputs and `run_tests.py` under `test/lab3/`, and this report under `report/`. The syntax tree is embedded as text, so no separate image is needed to view it.

Before submitting, review the source attribution markers, commit the final files, push the commit to GitHub, and verify that the instructor can access it. Submit the exact commit link on Blackboard using this repository's URL format:

```text
https://github.com/barberna/Structure-of-Programming-Languages/commit/<commit-hash>
```

Replace `<commit-hash>` with the final committed revision from `git rev-parse HEAD`. The report does not assert that the final commit has been pushed or submitted.

