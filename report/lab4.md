# CIS 343 Statements Lab 4

Language Name: PLox

## Statement Grammar

```text
program   -> statement* EOF ;
statement -> exprStmt | printStmt ;
exprStmt  -> expression ";" ;
printStmt -> "print" expression ";" ;
```

The `*` means zero or more statements. Each statement ends with a semicolon. The `expression` rule reuses the expression grammar from the previous lab, including literals, grouping, unary operators, arithmetic, comparisons, and equality. A program can contain multiple statements, and an empty program is allowed.

## Design choices relative to Lox

PLox supports Lox-style expression statements and print statements. An expression statement evaluates its expression and discards the result. A print statement evaluates its expression and prints the result. For example, `4 + 2;` produces no result output, while `print 4 + 2;` prints `6.0`.

The scanner still processes the source once and returns one token list. The parser does not split that list into separate lists for individual statements. `TokenStream` holds the tokens and one shared current index. `ProgramParser` creates the stream and passes the same object to `ExpressionParser` and `PrintParser`.

`ProgramParser` directs parsing based on the next token. If it sees `PRINT`, it calls `PrintParser`. Otherwise, it calls the expression parser and then requires a semicolon. `PrintParser` consumes the print keyword, calls the shared expression parser, requires a semicolon, and returns a print statement node. The expression parser stops before the semicolon, leaving the statement handler to consume it.

This separates statement handling into cooperating parser classes instead of placing all parsing methods in one class. The shared cursor keeps them at the same position without rescanning tokens. A shared `ParseError` class is imported from `parse_error.py` to avoid circular imports between parsers.

### Statement AST and execution

`PrintStmt` and `ExpressionStmt` inherit from `Stmt`, which stores an expression. The existing `Literal`, `Unary`, `Binary`, and `Grouping` expression classes are reused. `ProgramParser.parse()` returns a list of successfully parsed statement nodes in source order.

`PLox.run()` scans the source, checks for lexical errors, parses the program, and passes each returned statement to `Evaluator.execute()`. The evaluator uses Python match/case to distinguish the two statement classes. `ExpressionStmt` evaluates without printing a result; `PrintStmt` evaluates and formats the value for printing. The expression evaluator is reused from the midterm work.

Numbers print as floating-point values, such as `3.0`. Booleans print as `true` and `false`, and the nil value prints as `nil`. Strings print without quotation marks. The language retains the boolean-number coercion introduced for the midterm; it is not a new requirement of this lab.

The scanner, tokens, expression AST classes, and AST printer remain under `src/`. The normal statement execution path does not print the AST. It does echo the source before parsing, so source text in the output must be distinguished from statement results.

## Panic-Mode Error Recovery

`ProgramParser.parse()` handles `ParseError` inside its statement loop. A malformed statement is not appended to the statement list. After the diagnostic is reported, the parser skips tokens until it reaches a safe boundary:

- At a semicolon, it consumes the semicolon and resumes parsing the next statement.
- At `PRINT`, it leaves the token unconsumed so `PrintParser` can start the next statement.
- At EOF, it stops recovery and finishes parsing instead of advancing forever.

`PrintParser` consumes its `PRINT` token before parsing the expression. This ensures that an invalid print statement makes progress before control returns to recovery.

For the first required test, the missing semicolon after `"one"` is detected at `true`. Recovery skips `true` and consumes its semicolon, then resumes at `print`. The incomplete expression `2 +` produces a second diagnostic at EOF. Reporting both errors in one run demonstrates continued parsing after an error.

Successfully parsed statements still execute after syntax-error recovery. The post-parse error flag does not block execution of the returned statement list. For example, `print ; print 42;` reports the malformed first statement and still prints `42.0`. Lexical errors are handled differently: the check after scanning stops the run before parsing. A runtime `EvaluationError` stops execution of the remaining statements in that input and reports the error; interactive mode remains available for another input.

## Dependency/setup instructions

Python 3.10 or newer is required for match/case. No third-party packages are required. The results below were verified with Python 3.12.14. A virtual environment is optional, and no PYTHONPATH setting is needed.

Open PowerShell in the repository root, which contains `src`, `test`, and `report`:

```powershell
python --version
python src/plox.py test/lab4/error_test.plx
python src/plox.py test/lab4/test.plx
```

If the terminal is already inside `src`, use:

```powershell
python plox.py ../test/lab4/error_test.plx
python plox.py ../test/lab4/test.plx
```

Start interactive mode from the repository root with:

```powershell
python src/plox.py
```

Enter semicolon-terminated statements. Multiple statements may be entered on one line. Source files can span multiple lines. Exit the interactive session with Ctrl+C or end-of-input.

## Testing

The two required input files are saved under `test/lab4/`. Expected results were compared with actual program output. Standard output and standard error are shown separately because their interleaving can vary in a terminal. Text captures are included directly, so no screenshots or files in `lab4-assets/` are needed.

### Test 1: Syntax errors and panic-mode recovery

File: [error_test.plx](../test/lab4/error_test.plx)

Purpose: Verify that a missing statement terminator is reported, parsing continues, and a later incomplete expression also produces an error without a hang or Python traceback.

Source input:

```text
"one"
true;
print 2 +
```

The saved file includes a newline after `print 2 +`.

Expected standard output: the source echo only; no evaluated statement results.

Expected standard error:

```text
[Line: 2] Error: Expected ';' after expression.
[Line: 4] Error: Expected expression.
```

Actual standard output:

```text
"one"
true;
print 2 +
```

Actual standard error:

```text
[Line: 2] Error: Expected ';' after expression.
[Line: 4] Error: Expected expression.
```

The first diagnostic points to line 2 because `true` is the next token encountered where the parser expected the semicolon after `"one"`. The second diagnostic points to line 4 because the saved file's trailing newline advances the scanner's line counter before the EOF token is created. The missing operand belongs to the expression on line 3. Without that final newline, the EOF diagnostic would instead report line 3.

Result: **Pass** - both expected syntax errors were reported in the same run. Recovery reached the second malformed statement, and no statement result was printed.

### Test 2: Expression and print statements

File: [test.plx](../test/lab4/test.plx)

Purpose: Verify that expression statements discard their results, print statements display values, and multiple statements execute in source order. This case also checks string, boolean, numeric, and nil output.

Source input:

```text
4 + 2;
print "one";
print true;
print 1 + 2;
print nil;
```

Expected statement output after the source echo:

```text
one
true
3.0
nil
```

Expected standard error: none.

Actual standard output, including the source echo:

```text
4 + 2;
print "one";
print true;
print 1 + 2;
print nil;
one
true
3.0
nil
```

Actual standard error: none.

Result: **Pass** - the expression statement did not print `6.0`, and all four print statements produced the expected values in order.

### Additional interactive recovery checks

These checks were entered in one interactive session, in the order below. Each row is one input line and can be reproduced by starting `python src/plox.py`.

| Input | Purpose | Expected result after source echo | Actual result after source echo | Result |
|---|---|---|---|---|
| `print ; print 42;` | Recover at a semicolon and execute a later valid statement | `[Line: 1] Error: Expected expression before ';'.` and `42.0` | Same diagnostic and `42.0` | Pass |
| `print 1` | Stop recovery safely at EOF when a semicolon is missing | `[Line: 1] Error: Expected ';' after expression.` and no statement result | Same diagnostic; no statement result | Pass |
| `print 7;` | Accept valid input after the preceding error | `7.0`, no error | `7.0`, no error | Pass |

All three inputs completed without hanging, and the prompt remained usable. Error messages are written to standard error; printed values are written to standard output.

## Known limitations

- Both required tests and the three additional interactive checks passed. This does not establish correctness for every possible input.
- Recovery uses semicolons, the print keyword, and EOF as boundaries. It can discard additional tokens that might otherwise form a valid expression statement, as happens to `true;` in the first required test.
- Variable declarations, assignment, blocks, conditionals, loops, and functions are not implemented in this statement grammar.
- Diagnostics include line numbers but not column positions. Missing tokens at EOF may be reported on the line after a trailing newline.
- Interactive input is handled one line at a time. Multiline programs should be placed in a source file.
- The source is echoed before execution. This echo is diagnostic output, not the result of an expression statement.
- File mode does not currently return a nonzero exit code for language errors. Check the diagnostics rather than relying only on the process exit status.
- The existing recursive expression parser and evaluator remain subject to Python's recursion limit for very deeply nested input.

## AI assistance

AI assistance was used for implementation guidance, test review, and report preparation. Actual outputs in this report were checked against the current program. AI-generated code must be marked in the implementation using `# --- start AI code ---` and `# --- end AI code ---`, as required by the lab. This acknowledgment does not replace the source-code markers.

