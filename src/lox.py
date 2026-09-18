import sys
from pathlib import Path

"""
When we call run coil.py, we enter REPL Mode where we echo the input
And then send "Scanner Not Implemented" and allow the user to keep inputing inill
CTR+C
"""
"""
We then run coil.py fallowd by another files name then we execute
the code and ehco it, then return "Scanner Not Implemented"
"""

class Lox:
    def __init__(self):
        self.had_error = False

    def error(self, line, column, message):
        print(f"[Line: {line}, column {column}] Error: {message}", file=sys.stderr)
        self.had_error = True

    def run(self, source):
        # Source: AI
        print(source, end="" if source.endswith("\n") else "\n", flush=True)
        # End Source
        self.error(1, 1, "Scanner Not Implemented")

    def run_file(self, filename):
        try:
            source = Path(filename).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            print(f"Could not read '{filename}': {error}", file=sys.stderr)
            return

        self.run(source)
        return

    def run_prompt(self):
        # Keep accepting inout until CTR+C
        print(">>>>> PLox Interactive Shell <<<<<")
        try:
            while True:
                source = input(">")
                self.run(source)
                self.has_error = False
        except (KeyboardInterrupt, EOFError):
            print()
        return

def main(argv=None):
    # if length of args is one then we un REPL
    # if the length of args > 1 then we want to run the file

    # This says: starting after the first arg,
    # if we want to run REPL mode this will be an empty string
    args = sys.argv[1:] if argv is None else argv

    if len(args) > 1:
        print('Usage: python src/lox.py [script.lox]')
        return 64

    interpretor = Lox()
    if args:
        return interpretor.run_file(args[0])
    return interpretor.run_prompt()

if __name__ == "__main__":
    sys.exit(main())
    