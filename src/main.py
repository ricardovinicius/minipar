import sys

from lexer import Scanner, Token

# FIXME: do something better than this
hadError = False

def run(source: str):
    """
    Processes a source string, scans it for tokens, and prints each token.

    This function utilizes the Scanner class to tokenize the provided source
    string. The tokens are then iteratively printed. It is assumed that the
    Scanner class and Token objects are properly defined and implemented
    elsewhere in the codebase.

    :param source: The source string to be tokenized.
    :type source: str
    :return: None
    """
    scanner: Scanner = Scanner(source)
    tokens: list[Token] = scanner.scan_tokens()

    for token in tokens:
        print(token)

def run_file(path: str):
    """
    Execute the content of a given file by reading and running its source code.

    This function reads the file specified by the path parameter, processes its
    content as source code, and executes it. It ensures to handle errors and exits
    the program with a specific status code if execution encounters an issue.

    :param path: The file path of the source code to be read and executed.
    :type path: str
    :return: None
    """
    with open(path) as file:
        source: str = file.read()
        run(source)

        if hadError:
            sys.exit(65)

if __name__ == "__main__":
    args = sys.argv

    if len(args) > 2:
        print("Usage: minipar <program>")
        sys.exit(1)
    elif len(args) == 2:
        run_file(args[1])
        # TODO add: run_file()
    else:
        pass
        # TODO: add run_prompt()
