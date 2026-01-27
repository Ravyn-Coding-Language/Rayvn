from compiler.rayvn_ast import *
from compiler.lexer import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def finish_call(self, callee):
        self.expect(TokenType.LPAREN)

        args = []
        if self.peek().type != TokenType.RPAREN:
            args.append(self.expression())
            while self.peek().type == TokenType.COMMA:
                self.advance()
                args.append(self.expression())

        self.expect(TokenType.RPAREN)
        return CallExpr(callee.name, args)

    def peek_next(self):
        if self.pos + 1 >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos + 1]

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def parse(self):
        stmts = []
        while self.peek().type != TokenType.EOF:
            stmts.append(self.statement())
        return Program(stmts)
    
    def if_chain(self):
        branches = []

        # if
        self.expect(TokenType.IF)
        condition = self.expression()
        body = self.block()
        branches.append((condition, body))

        # elseif*
        while self.peek().type == TokenType.ELSEIF:
            self.advance()
            condition = self.expression()
            body = self.block()
            branches.append((condition, body))

        # else?
        else_body = None
        if self.peek().type == TokenType.ELSE:
            self.advance()
            else_body = self.block()

        return IfChain(branches, else_body)

    def while_statement(self):
        self.advance()  # consume 'while'
        condition = self.expression()
        body = self.block()
        return WhileStmt(condition, body)

    def for_in_loop(self):
        self.advance()  # consume 'for'

        var_tok = self.advance()
        if var_tok.type != TokenType.IDENT:
            raise Exception("Expected identifier after 'for'")

        if self.advance().type != TokenType.IN:
            raise Exception("Expected 'in' after loop variable")

        iterable = self.expression()
        body = self.block()

        return ForInLoop(var_tok.value, iterable, body)

    def expect(self, type_):
        tok = self.advance()
        if tok.type != type_:
            raise Exception(f"Expected {type_}, got {tok.type}")
    
    def block(self):
        self.expect(TokenType.LBRACE)
        statements = []

        while self.peek().type != TokenType.RBRACE:
            statements.append(self.statement())

        self.expect(TokenType.RBRACE)
        return statements

    def statement(self):
        tok = self.peek()

        if tok.type == TokenType.ELSEIF:
            raise Exception("Unexpected 'else' without matching 'if'")

        if tok.type == TokenType.LET:
            self.advance()

            name_tok = self.advance()
            if name_tok.type != TokenType.IDENT:
                raise Exception("Expected identifier after 'let'")

            eq = self.advance()
            if eq.type != TokenType.EQUAL:
                raise Exception("Expected '=' after identifier")

            value = self.expression()
            return LetStmt(name_tok.value, value)

        if tok.type == TokenType.LOG:
            self.advance()
            return PrintStmt(self.expression())

        if tok.type == TokenType.IF:
            return self.if_chain()

        if tok.type == TokenType.WHILE:
            return self.while_statement()

        if tok.type == TokenType.FOR:
            return self.for_in_loop()

        if tok.type == TokenType.IDENT and tok.value == "range":
            self.advance()
            self.expect(TokenType.LPAREN)
            start = self.expression()
            self.expect(TokenType.COMMA)
            end = self.expression()
            self.expect(TokenType.RPAREN)
            return RangeExpr(start, end)

        if tok.type == TokenType.IDENT and self.peek_next().type == TokenType.LBRACKET:
            array = self.primary()  # parses a[expr]
            if self.peek().type == TokenType.EQUAL:
                self.advance()  # consume '='
                value = self.expression()
                return IndexAssign(array.array, array.index, value)
            return ExprStmt(array)

        if tok.type == TokenType.IDENT and self.peek_next().type == TokenType.EQUAL:
            target = self.advance().value  # variable name
            self.advance()  # consume '='
            value = self.expression()
            return AssignStmt(target, value)

        if tok.type == TokenType.FN:
            return self.function_def()
        
        if tok.type == TokenType.RETURN:
            self.advance()
            value = None

            if self.peek().type != TokenType.RBRACE:
                value = self.expression()

            return ReturnStmt(value)

        if tok.type == TokenType.BREAK:
            self.advance()
            return BreakStmt()

        if tok.type == TokenType.CONTINUE:
            self.advance()
            return ContinueStmt()

        expr = self.expression()
        return ExprStmt(expr)

    def primary(self):
        tok = self.peek()

        # --- Base expression ---
        if tok.type == TokenType.LBRACKET:
            self.advance()
            elements = []

            if self.peek().type != TokenType.RBRACKET:
                elements.append(self.expression())
                while self.peek().type == TokenType.COMMA:
                    self.advance()
                    elements.append(self.expression())

            self.expect(TokenType.RBRACKET)
            expr = ArrayLiteral(elements)

        elif tok.type == TokenType.IDENT and tok.value == "range":
            self.advance()
            self.expect(TokenType.LPAREN)

            start = self.expression()
            self.expect(TokenType.COMMA)
            end = self.expression()

            step = None
            if self.peek().type == TokenType.COMMA:
                self.advance()
                step = self.expression()

            self.expect(TokenType.RPAREN)
            expr = RangeExpr(start, end, step)

        elif tok.type == TokenType.TRUE:
            self.advance()
            expr = Boolean(True)

        elif tok.type == TokenType.FALSE:
            self.advance()
            expr = Boolean(False)

        elif tok.type == TokenType.IDENT:
            self.advance()
            expr = Var(tok.value)

        elif tok.type == TokenType.NUMBER:
            self.advance()
            expr = Number(tok.value)

        elif tok.type == TokenType.STRING:
            self.advance()
            expr = String(tok.value)

        elif tok.type == TokenType.LPAREN:
            self.advance()
            expr = self.expression()
            self.expect(TokenType.RPAREN)

        else:
            raise Exception(f"Invalid expression starting with {tok.type}")

        # --- Postfix operations: indexing + calls ---
        while True:
            # Indexing: a[expr]
            if self.peek().type == TokenType.LBRACKET:
                self.advance()
                index = self.expression()
                self.expect(TokenType.RBRACKET)
                expr = IndexExpr(expr, index)
                continue

            # Function call: f(...)
            if self.peek().type == TokenType.LPAREN:
                expr = self.finish_call(expr)
                continue

            break

        return expr

    def function_def(self):
        self.advance()  # fn
        name = self.advance().value  # function name

        self.expect(TokenType.LPAREN)

        params = []
        if self.peek().type != TokenType.RPAREN:
            params.append(self.advance().value)
            while self.peek().type == TokenType.COMMA:
                self.advance()
                params.append(self.advance().value)

        self.expect(TokenType.RPAREN)
        body = self.block()

        return FunctionDef(name, params, body)

    def call_expression(self):
        name = self.advance().value
        self.expect(TokenType.LPAREN)

        args = []
        if self.peek().type != TokenType.RPAREN:
            args.append(self.expression())
            while self.peek().type == TokenType.COMMA:
                self.advance()
                args.append(self.expression())

        self.expect(TokenType.RPAREN)
        return CallExpr(name, args)

    def or_expr(self):
        left = self.and_expr()

        while self.peek().type in (TokenType.OROR, TokenType.OR):
            op = self.advance().type
            right = self.and_expr()
            left = Binary(left, op, right)

        return left

    def and_expr(self):
        left = self.comparison()

        while self.peek().type in (TokenType.ANDAND, TokenType.AND):
            op = self.advance().type
            right = self.comparison()
            left = Binary(left, op, right)

        return left

    def expression(self):
        return self.or_expr()
    
    def comparison(self):
        left = self.term()

        while self.peek().type in (
            TokenType.GT,
            TokenType.LT,
            TokenType.GTE,
            TokenType.LTE,
            TokenType.EQEQ,
            TokenType.NOTEQ,
        ):
            op = self.advance().type
            right = self.term()
            left = Binary(left, op, right)

        return left
    
    def term(self):
        left = self.factor()

        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance().type
            right = self.factor()
            left = Binary(left, op, right)

        return left
    
    def unary(self):
        if self.peek().type == TokenType.NOT:
            self.advance()
            return Not(self.unary())

        if self.peek().type == TokenType.MINUS:
            op = self.advance().type
            expr = self.unary()
            return Unary(op, expr)

        return self.primary()

    def factor(self):
        left = self.unary()
        while self.peek().type in (TokenType.STAR, TokenType.SLASH):
            op = self.advance().type
            right = self.unary()
            left = Binary(left, op, right)
        return left
