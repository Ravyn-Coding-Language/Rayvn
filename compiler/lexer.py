from enum import Enum, auto

class TokenType(Enum):
    LET = auto()
    FN = auto()
    IF = auto()
    ELSEIF = auto()
    ELSE = auto()
    LOG = auto()

    IDENT = auto()
    NUMBER = auto()
    STRING = auto()

    EQUAL = auto()      
    EQEQ = auto()
    NOTEQ = auto()      
    GT = auto()         
    GTE = auto()      
    LT = auto()         
    LTE = auto()        

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()

    TRUE = auto()
    FALSE = auto()

    AND = auto()
    OR = auto()
    NOT = auto()

    ANDAND = auto()
    OROR = auto()

    RETURN = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()

    WHILE = auto()
    FOR = auto()
    IN = auto()

    BREAK = auto()
    CONTINUE = auto()

    COMMA = auto()
    EOF = auto()


KEYWORDS = {
    "let": TokenType.LET,
    "fn": TokenType.FN,
    "if": TokenType.IF,
    "elseif": TokenType.ELSEIF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "in": TokenType.IN,
    "log": TokenType.LOG,

    "true": TokenType.TRUE,
    "false": TokenType.FALSE,

    "return": TokenType.RETURN,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,

    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "!": TokenType.NOT,
}


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type.name}:{self.value}"


class Lexer:
    def __init__(self, src):
        self.src = src
        self.pos = 0

    def peek(self):
        if self.pos >= len(self.src):
            return "\0"
        return self.src[self.pos]

    def peek_next(self):
        if self.pos + 1 >= len(self.src):
            return "\0"
        return self.src[self.pos + 1]

    def peek_next_next(self):
        if self.pos + 2 >= len(self.src):
            return "\0"
        return self.src[self.pos + 2]

    def advance(self):
        ch = self.peek()
        self.pos += 1
        return ch

    def tokenize(self):
        tokens = []

        while self.peek() != "\0":
            c = self.peek()

            if c.isspace():
                self.advance()
                continue

            if c.isalpha():
                ident = ""
                while self.peek().isalnum():
                    ident += self.advance()
                tokens.append(Token(KEYWORDS.get(ident, TokenType.IDENT), ident))
                continue

            if c.isdigit():
                num = ""
                while self.peek().isdigit():
                    num += self.advance()
                tokens.append(Token(TokenType.NUMBER, int(num)))
                continue

            # --- COMMENTS ---

            # Multi-line comment ***
            if c == "*" and self.peek_next() == "*" and self.peek_next_next() == "*":
                # consume ***
                self.advance()
                self.advance()
                self.advance()

                while not (
                    self.peek() == "*" and
                    self.peek_next() == "*" and
                    self.peek_next_next() == "*"
                ):
                    if self.peek() == "\0":
                        raise Exception("Unterminated block comment")
                    self.advance()

                # consume closing ***
                self.advance()
                self.advance()
                self.advance()
                continue

            # Single-line comment **
            if c == "*" and self.peek_next() == "*":
                # consume **
                self.advance()
                self.advance()

                while self.peek() not in ("\n", "\0"):
                    self.advance()
                continue

            # Two-character operators
            if c == "=" and self.peek_next() == "=":
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.EQEQ))
                continue

            if c == "!" and self.peek_next() == "=":
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.NOTEQ))
                continue

            if c == ">" and self.peek_next() == "=":
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.GTE))
                continue

            if c == "<" and self.peek_next() == "=":
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.LTE))
                continue

            if c == "&" and self.peek_next() == "&":
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.ANDAND))
                continue

            if c == "|" and self.peek_next() == "|":
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.OROR))
                continue

            if c == '"':
                self.advance()  # consume opening "
                string_val = ""
                while self.peek() != '"':
                    if self.peek() == "\0":
                        raise Exception("Unterminated string literal")
                    string_val += self.advance()
                self.advance()  # consume closing "
                tokens.append(Token(TokenType.STRING, string_val))
                continue

            single = {
                "=": TokenType.EQUAL,
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.STAR,
                "/": TokenType.SLASH,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                "{": TokenType.LBRACE,
                "}": TokenType.RBRACE,
                "[": TokenType.LBRACKET,
                "]": TokenType.RBRACKET,
                ",": TokenType.COMMA,
                ">": TokenType.GT,
                "<": TokenType.LT,
                "!": TokenType.NOT,
            }

            if c in single:
                tokens.append(Token(single[c]))
                self.advance()
                continue

            if c == "=":
                tokens.append(Token(TokenType.EQUAL))
                self.advance()
                continue

            raise Exception(f"Unexpected character: {c}")

        tokens.append(Token(TokenType.EOF))
        return tokens