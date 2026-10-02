import sys
from pathlib import Path
from scanner import Scanner


class PLox:
    def __init__(self):
        self.had_error = False

    def error(self, line, message):
        print(f"[Line: {line}] Error: {message}", file=sys.stderr)
        self.had_error = True

    def run(self, source):
        # Source: AI
        print(source, end="" if source.endswith("\n") else "\n", flush=True)

        scanner = Scanner(source, self)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

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
                self.had_error = False
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

    interpretor = PLox()
    if args:
        return interpretor.run_file(args[0])
    return interpretor.run_prompt()

if __name__ == "__main__":
    sys.exit(main())
    