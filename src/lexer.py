import error


from enum import Enum

class TokenType(Enum):
    """
    Represents types of tokens in a programming language for parsing or lexical
    analysis.

    This class defines an enumeration of token types that might be identified in
    a source code during the lexical analysis or parsing phase. It groups tokens
    under categories like single-character tokens, literals, comments, two-character
    tokens, keywords, whitespace, and other types. The members of this enumeration
    correspond to specific types of tokens that might appear in a language.
    """
    # Single-char tokens.
    LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE = 1, 2, 3, 4
    COMMA, DOT, MINUS, PLUS = 5, 6, 7, 8
    SEMICOLON, SLASH, STAR, LESS = 9, 10, 11, 12
    NOT, GREATER, ASSIGN, TYPEOF = 13, 14, 15, 16

    # Literals.
    NAME, NUMBER, STRING = 17, 18, 19

    # Comments.
    SCOMMENT, MCOMMENT = 20, 21

    # Two chars tokens.
    RARROW, OR, AND, EQ = 22, 23, 24, 25
    NEQ, LTE, GTE, NEWLINE = 26, 27, 28, 29

    # Keywords.
    FUNC, IF, ELSE = 30, 31, 32
    WHILE, RETURN, BREAK, CONTINUE = 33, 34, 35, 36
    SEQ, PAR, C_CHANNEL, S_CHANNEL, FOR = 37, 38, 39, 40, 41

    # Whitespace.
    WHITESPACE = 42

    # Types.
    NUMBER_TYPE, BOOL_TYPE, STRING_TYPE, VOID_TYPE = 43, 44, 45, 46

    # Other.
    OTHER = -1

class Token:
    """
    Represents a token in the lexical analysis phase of a compiler or interpreter.

    This class encapsulates information about a token, including its type, its
    lexeme (the actual text of the token), an optional literal value, and the
    line where the token appears within the source code. It provides a structured
    way to represent tokens extracted during the lexical analysis process.
    """
    _type: TokenType
    lexeme: str
    literal: object
    line: int

    def __init__(self, _type: TokenType, lexeme: str, literal: object, line: int):
        self._type = _type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self._type.name} {self.lexeme} {self.literal}"


class Scanner:
    """
    Performs lexical analysis (scanning) of a source code string and generates a
    list of tokens.

    The Scanner class is responsible for breaking down a source code input string
    into individual tokens. These tokens are then utilized in subsequent stages of
    a compiler or interpreter, such as parsing or code generation. The class handles
    various types of tokens, including identifiers, keywords, numbers, strings,
    operators, and punctuation. Additionally, it accounts for whitespace and comments
    while managing line numbers for accurate error reporting.

    The Scanner implements methods to process each character of the source code,
    identifying token types and constructing tokens with relevant metadata. It supports
    multi-character tokens like strings, numbers, and complex operators, as well as
    error reporting for invalid or unmatched characters.
    """
    keywords = {
        "func": TokenType.FUNC,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "return": TokenType.RETURN,
        "break": TokenType.BREAK,
        "continue": TokenType.CONTINUE,
        "seq": TokenType.SEQ,
        "par": TokenType.PAR,
        "c_channel": TokenType.C_CHANNEL,
        "s_channel": TokenType.S_CHANNEL,
        "for": TokenType.FOR,
        "number": TokenType.NUMBER_TYPE,
        "bool": TokenType.BOOL_TYPE,
        "string": TokenType.STRING_TYPE,
        "void": TokenType.VOID_TYPE,
    }

    source: str
    tokens: list[Token]
    start: int = 0
    current: int = 0
    line: int = 1

    def __init__(self, source: str):
        self.source = source
        self.tokens = []

    def _is_at_end(self) -> bool:
        """
        Checks if the cursor has reached the end of the source string.

        The method compares the current position of the cursor to the
        length of the source string to determine whether the end of
        the input has been reached.

        :return: True if the current position is greater than or equal
                 to the length of the source string, False otherwise.
        :rtype: bool
        """
        return self.current >= len(self.source)

    def _advance(self) -> str:
        """
        Advances the current position in the source string by one and returns the character
        at the previous position.

        This method updates the internal state of `self.current` by incrementing it after
        retrieving the character at the current position in the `self.source`. It is typically
        used for iterating through a sequence of characters in a string.

        :return: The character at the position of `self.current` before it was incremented.
        """
        char: str = self.source[self.current]
        self.current += 1
        return char

    def _add_token(self, _type: TokenType, literal: object = None):
        """
        Adds a new token to the list of tokens based on the provided type, text, and optional literal value.
        This function utilizes the current position within the source code to extract the necessary substring
        for the token's value.

        The appended token includes type, text, literal, and the current line for accuracy in tracking.

        :param _type: Type of the token being added
        :param literal: Optional literal value associated with the token
        :return: None
        """
        text: str = self.source[self.start:self.current]
        self.tokens.append(Token(_type, text, literal, self.line))

    def _match(self, expected: str) -> bool:
        """
        Compares the current character in the input source with the expected character
        and advances the cursor position if they match. Returns a boolean indicating
        whether the characters match.

        This function is used to consume and verify characters one at a time during
        parsing or scanning processes. It ensures that the parser progresses only when
        the characters match the specified `expected` character.

        :param expected: The character being checked against the current character
            in the input source.
        :return: True if the current character matches the `expected` character,
            otherwise False.
        """
        if self._is_at_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        return True

    def _peek(self) -> str | None:
        """
        _peek method retrieves the current character from the source
        string without advancing the current position of the cursor. If there
        are no more characters to process (end of source is reached), it will
        return None.

        :return: The current character from the source if it exists,
            otherwise None
        :rtype: Optional[str]
        """
        if self._is_at_end(): return None
        return self.source[self.current]

    def _peek_next(self) -> str | None:
        """
        Peek at the next character in the source string without advancing the current index.

        This function evaluates whether there is a character available at the next position in
        the source string without modifying the current index. If the current index is at the
        last character or if there are no characters left in the source, the function will return
        None.

        :return: The next character in the source string if available; otherwise, None.
        :rtype: Optional[str]
        """
        if self.current + 1 >= len(self.source): return None
        return self.source[self.current + 1]

    def _string(self):
        """
        Processes a string literal, adding it as a token upon successful parsing. This
        method handles cases where a string spans multiple lines and ensures strings
        are properly terminated. If an unterminated string is encountered, an error is
        reported, and the method exits without adding a token.

        :return: None
        """
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == '\n': self.line += 1
            self._advance()

        if self._is_at_end():
            error.report(self.line, "Unterminated string.")
            return

        self._advance()
        value: str = self.source[self.start + 1:self.current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self):
        """
        Processes a number in the source string and adds it as a token if it matches
        the number pattern. The function scans for digits, including handling decimals
        for floating-point numbers.

        :return: None
        """
        while self._peek().isdigit():
            self._advance()

        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit(): self._advance()

        self._add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def _name(self):
        """
        Processes a sequence of alphanumeric characters or underscores, extracts a potential
        identifier or keyword, and adds the corresponding token to the list of tokens.

        The method identifies a valid name by iterating over the source text until it encounters
        a character that is neither alphanumeric nor an underscore. It then determines whether
        the extracted identifier matches any language keyword or if it should be classified as
        a generic name. Finally, a token of the appropriate type is created and added to the
        list of tokens.

        :return: None
        """
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()

        text: str = self.source[self.start:self.current]
        _type: TokenType = self.keywords.get(text, TokenType.NAME)
        self._add_token(_type)

    def _scan_token(self):
        """
        Scans a single token from the source code and categorizes it into a recognized
        token type. This method matches the current character against various patterns
        and handles special cases for composite or unsupported characters.

        :return: None
        """
        c: str = self._advance()

        match c:
            case '(': self._add_token(TokenType.LEFT_PAREN)
            case ')': self._add_token(TokenType.RIGHT_PAREN)
            case '{': self._add_token(TokenType.LEFT_BRACE)
            case '}': self._add_token(TokenType.RIGHT_BRACE)
            case ',': self._add_token(TokenType.COMMA)
            case '.': self._add_token(TokenType.DOT)
            case '+': self._add_token(TokenType.PLUS)
            case ';': self._add_token(TokenType.SEMICOLON)
            case '/': self._add_token(TokenType.SLASH)
            case '*': self._add_token(TokenType.STAR)
            case ':': self._add_token(TokenType.TYPEOF)
            case '-':
                if self._match('>'):
                    self._add_token(TokenType.RARROW)
                else:
                    self._add_token(TokenType.MINUS)
            case "!":
                if self._match("="):
                    self._add_token(TokenType.NEQ)
                else:
                    self._add_token(TokenType.NOT)
            case "|":
                if self._match("|"):
                    self._add_token(TokenType.OR)
                else:
                    error.report(self.line, "Unexpected character.")
                    self._add_token(TokenType.OTHER)
            case "&":
                if self._match("&"):
                    self._add_token(TokenType.AND)
                else:
                    error.report(self.line, "Unexpected character.")
                    self._add_token(TokenType.OTHER)
            case "=":
                if self._match("="):
                    self._add_token(TokenType.EQ)
                else:
                    self._add_token(TokenType.ASSIGN)
            case "<":
                if self._match("="):
                    self._add_token(TokenType.LTE)
                else:
                    self._add_token(TokenType.LESS)
            case ">":
                if self._match("="):
                    self._add_token(TokenType.GTE)
                else:
                    self._add_token(TokenType.GREATER)
            case "#":
                while not self._match("\n"):
                    self._advance()
            case "/":
                if self._match("*"):
                    while not self._match("/"):
                        if self._is_at_end():
                            error.report(self.line, "Unterminated comment.")
                            break
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case " " | "\t" | "\r": pass
            case "\n": self.line += 1
            case '"':
                self._string()
            case _:
                if c.isdigit():
                    self._number()
                    return

                if c.isalpha() or c == "_":
                    self._name()
                    return

                error.report(self.line, f"Unexpected character {c}. ")
                self._add_token(TokenType.OTHER)

    def scan_tokens(self) -> list[Token]:
        """
        Scans through the input source code and tokenizes it into a list of tokens.

        This method iterates through the input source, identifying tokens one by one
        until the end of the source is reached. Each identified token is added to the
        list of tokens (`self.tokens`) that will ultimately be returned. The scanning
        process involves resetting the `start` and `current` pointers for each token
        and invoking the private method `_scan_token` to classify and handle the token.

        :return: A list of tokens generated from the input source code.
        :rtype: List[Token]
        """
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        return self.tokens