# --- start AI code ---
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
expected = [
'45.67', 'hello', 'true', 'false', 'nil', '(+ 1.0 2.0)', '(- 5.0 3.0)',
'(* 2.0 3.0)', '(/ 8.0 2.0)', '(- 5.0)', '(! true)', '(! (! false))',
'(== 2.0 2.0)', '(!= 2.0 3.0)', '(> 3.0 2.0)', '(>= 3.0 3.0)',
'(< 2.0 3.0)', '(<= 2.0 2.0)', '(+ 1.0 (* 2.0 3.0))',
'(* (group (+ 1.0 2.0)) 3.0)', '(group (group (+ 1.0 2.0)))',
'(- (- 8.0 3.0) 1.0)', '(/ (/ 16.0 4.0) 2.0)', '(* (- 2.0) 3.0)',
'(< (+ 1.0 2.0) 4.0)', '(== (< 1.0 2.0) true)', '(< (< 1.0 2.0) 3.0)',
'(!= (== true false) nil)']
errors = ['Expected expression.', 'Expected expression.', 'Expected expression.',
'Expected Closing Paren', "Unexpected token ')' after expression.", 'Expected expression.',
'Expected expression.', 'Expected expression.', "Unexpected token '2' after expression.",
"Unexpected token ';' after expression.", 'Expected expression.', 'Unexpected Character',
'Unterminated string', 'Expected expression.']
purposes = [
'Decimal number literal', 'String literal', 'True literal', 'False literal', 'Nil literal',
'Binary addition', 'Binary subtraction', 'Binary multiplication', 'Binary division',
'Unary negation', 'Unary logical not', 'Stacked unary operators', 'Equality', 'Inequality',
'Greater than', 'Greater than or equal', 'Less than', 'Less than or equal',
'Multiplication binds before addition', 'Parentheses override precedence', 'Nested grouping',
'Subtraction associates left', 'Division associates left', 'Unary binds before multiplication',
'Arithmetic binds before comparison', 'Comparison binds before equality',
'Comparison associates left', 'Equality associates left',
'Missing right operand after +', 'Missing left operand: * cannot begin an expression',
'Missing operand after unary !', 'Opening parenthesis has no closing parenthesis',
'Closing parenthesis has no matching opening parenthesis', 'Empty group has no expression',
'Unexpected * where an operand is required', 'Identifiers are outside the expression grammar',
'Second literal is an unexpected trailing token', 'Semicolons are not part of the expression grammar',
'Empty input has no expression', 'Unexpected @ character prevents parsing',
'String is missing its closing quote', 'Invalid operand on line 2 tests diagnostic location',
'Multiline expression with leading and trailing comments']

def run(args=(), source=None):
    return subprocess.run([sys.executable, '-B', str(root/'src/plox.py'), *args],
                          input=source, capture_output=True, text=True, timeout=15)

results = []
for i, path in enumerate(sorted((root/'test/lab3').glob('*.plx'))):
    source = path.read_text(encoding='utf-8')
    result = run([str(path)])
    echo = source + ('' if source.endswith('\n') else '\n')
    ast = expected[i] if i < 28 else ('(+ 1.0 (* 2.0 3.0))' if i == 42 else None)
    error = f'[Line: {2 if i == 41 else 1}] Error: {errors[i-28]}\n' if 28 <= i <= 41 else ''
    wanted = echo + (ast + '\n' if ast is not None else '')
    passed = result.stdout == wanted and result.stderr == error and result.returncode == 0
    results.append((path, source, ast, error, result, passed))
    print(('PASS ' if passed else 'FAIL ') + path.name)

interactive_source = '1 +\n2 * 3\n@\n!false\n(1 + 2\n(1 + 2) * 3\n'
interactive = run(source=interactive_source)
interactive_stdout = ('>>>>> PLox Interactive Shell <<<<<\n>1 +\n>2 * 3\n(* 2.0 3.0)\n'
                      '>@\n>!false\n(! false)\n>(1 + 2\n>(1 + 2) * 3\n'
                      '(* (group (+ 1.0 2.0)) 3.0)\n>\n')
interactive_stderr = ('[Line: 1] Error: Expected expression.\n'
                      '[Line: 1] Error: Unexpected Character\n'
                      '[Line: 1] Error: Expected Closing Paren\n')
interactive_pass = (interactive.stdout == interactive_stdout and
                    interactive.stderr == interactive_stderr and interactive.returncode == 0)
print('Interactive recovery:', 'PASS' if interactive_pass else 'FAIL')
assert len(results) == 43 and all(r[-1] for r in results) and interactive_pass

print('All 43 file tests and interactive recovery passed.')
# --- end AI code ---

