// --- start AI code ---
// Test every TokenType. EOF is generated automatically at the end.
// Scanner input does not need to form an executable program.
// Expected: no lexical errors; comments and whitespace produce no tokens.

// Single-character tokens: LEFT_PAREN RIGHT_PAREN LEFT_BRACE RIGHT_BRACE
// COMMA DOT MINUS PLUS SEMICOLON SLASH STAR. Literal values: None.
( ) { } , . - + ; / *

// Operators: BANG BANG_EQUAL EQUAL EQUAL_EQUAL GREATER GREATER_EQUAL
// LESS LESS_EQUAL. Literal values: None.
! != = == > >= < <=

// Keywords: one token per word. Literal values: None.
and class else false fun for if nil or print return super this true var while

// Identifiers: each produces IDENTIFIER with literal None.
// Keyword prefixes and capitalization changes remain identifiers.
x variable name_2 forLoop trueValue Var

// NUMBER tokens: literal values 0.0, 5.0, 42.0, 12345.0.
0 5 42 12345

// Negative number: MINUS (None), NUMBER (9.0).
-9

// STRING tokens: literals hello, hello world, and the empty string.
"hello" "hello world" ""

// STRING with literal // still a string; slashes inside strings are preserved.
"// still a string"

// Adjacent tokens: VAR IDENTIFIER EQUAL NUMBER SEMICOLON.
var x=5;

// PRINT STRING SEMICOLON; trailing comment produces no tokens.
print "done"; // ignored: @ ! == 123 "not a token"

// Blank lines and whitespace produce no tokens.
// End of file: EOF with empty lexeme and literal None.
// --- end AI code ---
