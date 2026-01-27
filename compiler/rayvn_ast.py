"""
Rayvn Abstract Syntax Tree (AST)

This file defines all AST node types used by the Rayvn parser.
Each class represents one syntactic construct in the language.

The parser produces instances of these classes.
The compiler / interpreter consumes them.
"""


# =========================
# Program Structure
# =========================

class Program:
    """
    Root node of the AST.

    Represents an entire Rayvn program.
    Contains a list of top-level statements.
    """
    def __init__(self, statements):
        self.statements = statements


# =========================
# Statements
# =========================

class LetStmt:
    """
    Variable declaration.

    Example:
        let x = 5
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value


class AssignStmt:
    """
    Variable reassignment.

    Example:
        x = x + 1
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value


class PrintStmt:
    """
    Print/log statement.

    Example:
        log x
    """
    def __init__(self, expr):
        self.expr = expr


class ExprStmt:
    """
    Expression used as a statement.

    Example:
        add(1, 2)
    """
    def __init__(self, expr):
        self.expr = expr


class ReturnStmt:
    """
    Return statement inside a function.

    Example:
        return x + 1
    """
    def __init__(self, value):
        self.value = value


class BreakStmt:
    """
    Break statement for loops.

    Example:
        break
    """
    pass


class ContinueStmt:
    """
    Continue statement for loops.

    Example:
        continue
    """
    pass


# =========================
# Control Flow
# =========================

class IfChain:
    """
    If / ElseIf / Else chain.

    branches: list of (condition, body) tuples
    else_body: optional list of statements
    """
    def __init__(self, branches, else_body=None):
        self.branches = branches
        self.else_body = else_body


class WhileStmt:
    """
    While loop.

    Example:
        while x < 10 { ... }
    """
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForInLoop:
    """
    For-in loop over an iterable.

    Example:
        for i in range(0, 10) { ... }
    """
    def __init__(self, var, iterable, body):
        self.var = var
        self.iterable = iterable
        self.body = body


# =========================
# Functions
# =========================

class FunctionDef:
    """
    Function definition.

    Example:
        fn add(a, b) { return a + b }
    """
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class CallExpr:
    """
    Function call expression.

    Example:
        add(1, 2)
    """
    def __init__(self, name, args):
        self.name = name
        self.args = args


# =========================
# Expressions
# =========================

class Number:
    """
    Numeric literal.

    Example:
        42
    """
    def __init__(self, value):
        self.value = value


class Boolean:
    """
    Boolean literal.

    Example:
        true / false
    """
    def __init__(self, value):
        self.value = value


class String:
    """
    String literal.

    Example:
        "hello"
    """
    def __init__(self, value):
        self.value = value


class Var:
    """
    Variable reference.

    Example:
        x
    """
    def __init__(self, name):
        self.name = name


class Unary:
    """
    Unary operation.

    Example:
        -x
    """
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class Not:
    """
    Logical NOT expression.

    Example:
        not x
    """
    def __init__(self, expr):
        self.expr = expr


class Binary:
    """
    Binary operation.

    Example:
        x + y
        a > b
    """
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Logical:
    """
    Logical AND / OR expression.

    Example:
        x and y
    """
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


# =========================
# Ranges
# =========================

class RangeExpr:
    """
    Range expression.

    Example:
        range(0, 10)
        range(10, 0, -1)
    """
    def __init__(self, start, end, step=None):
        self.start = start
        self.end = end
        self.step = step


# =========================
# Arrays and Indexing
# =========================

class ArrayLiteral:
    """
    Array literal.

    Example:
        [1, 2, 3]
    """
    def __init__(self, elements):
        self.elements = elements


class IndexExpr:
    """
    Array/string indexing expression.

    Example:
        a[0]
    """
    def __init__(self, array, index):
        self.array = array
        self.index = index


class IndexAssign:
    """
    Array index assignment.

    Example:
        a[1] = 42
    """
    def __init__(self, array, index, value):
        self.array = array
        self.index = index
        self.value = value