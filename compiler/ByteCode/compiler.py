from compiler.ByteCode.opcodes import OpCode
from compiler.rayvn_ast import *
from compiler.lexer import TokenType


class Compiler:
    """
    Compiler
    --------
    Walks the AST and emits bytecode instructions for the VM.

    Responsibilities:
    - Traverse AST nodes
    - Emit OpCode instructions
    - Track function entry points
    - Track loop state for break / continue
    """

    def __init__(self):
        self.code = []         # Final bytecode: list of (OpCode, arg)
        self.functions = {}    # Function table: name -> { entry, params }
        self.loop_stack = []   # Stack of active loops (for break/continue)

    # ---------------------------------------------------------
    # Low-level bytecode helpers
    # ---------------------------------------------------------

    def emit(self, op, arg=None):
        """
        Append an instruction to the bytecode.

        Returns the index of the emitted instruction so it can
        be patched later (used for jumps).
        """
        self.code.append((op, arg))
        return len(self.code) - 1

    def patch(self, index, value):
        """
        Update the argument of a previously emitted instruction.

        Used for control flow (if, loops, break, continue).
        """
        op, _ = self.code[index]
        self.code[index] = (op, value)

    # ---------------------------------------------------------
    # Main compilation dispatcher
    # ---------------------------------------------------------

    def compile(self, node):
        """
        Recursively compile an AST node into bytecode.
        """

        # =========================
        # Program root
        # =========================

        if isinstance(node, Program):
            for stmt in node.statements:
                self.compile(stmt)
            self.emit(OpCode.HALT)

        # =========================
        # Literals
        # =========================

        elif isinstance(node, Number):
            self.emit(OpCode.PUSH_CONST, node.value)

        elif isinstance(node, Boolean):
            self.emit(OpCode.PUSH_CONST, node.value)

        elif isinstance(node, String):
            self.emit(OpCode.PUSH_CONST, node.value)

        # =========================
        # Variables
        # =========================

        elif isinstance(node, Var):
            self.emit(OpCode.LOAD_VAR, node.name)

        elif isinstance(node, LetStmt):
            self.compile(node.value)
            self.emit(OpCode.STORE_VAR, node.name)

        elif isinstance(node, AssignStmt):
            self.compile(node.value)
            self.emit(OpCode.STORE_VAR, node.name)

        # =========================
        # Output
        # =========================

        elif isinstance(node, PrintStmt):
            self.compile(node.expr)
            self.emit(OpCode.PRINT)

        # =========================
        # Unary expressions
        # =========================

        elif isinstance(node, Unary):
            self.compile(node.expr)
            if node.op == TokenType.MINUS:
                self.emit(OpCode.NEG)

        elif isinstance(node, Not):
            self.compile(node.expr)
            self.emit(OpCode.NOT)

        # =========================
        # Binary expressions
        # =========================

        elif isinstance(node, Binary):
            self.compile(node.left)
            self.compile(node.right)
            self.emit(self.map_binary(node.op))

        # =========================
        # Expression statements
        # =========================

        elif isinstance(node, ExprStmt):
            self.compile(node.expr)
            self.emit(OpCode.POP)

        # =========================
        # Conditionals
        # =========================

        elif isinstance(node, IfChain):
            end_jumps = []

            for condition, body in node.branches:
                self.compile(condition)
                jump_false = self.emit(OpCode.JUMP_IF_FALSE, None)

                for stmt in body:
                    self.compile(stmt)

                end_jumps.append(self.emit(OpCode.JUMP, None))
                self.patch(jump_false, len(self.code))

            if node.else_body:
                for stmt in node.else_body:
                    self.compile(stmt)

            for j in end_jumps:
                self.patch(j, len(self.code))

        # =========================
        # While loops
        # =========================

        elif isinstance(node, WhileStmt):
            loop_start = len(self.code)

            self.compile(node.condition)
            exit_jump = self.emit(OpCode.JUMP_IF_FALSE, None)

            self.loop_stack.append({
                "start": loop_start,
                "breaks": [],
                "continues": []
            })

            for stmt in node.body:
                self.compile(stmt)

            self.emit(OpCode.JUMP, loop_start)

            loop = self.loop_stack.pop()
            loop_end = len(self.code)

            self.patch(exit_jump, loop_end)

            for br in loop["breaks"]:
                self.patch(br, loop_end)

            for ct in loop["continues"]:
                self.patch(ct, loop_start)

        # =========================
        # For-in loops
        # =========================

        elif isinstance(node, ForInLoop):
            self.compile(node.iterable)
            self.emit(OpCode.ITER_INIT)

            loop_start = len(self.code)
            self.emit(OpCode.ITER_NEXT)
            exit_jump = self.emit(OpCode.JUMP_IF_FALSE, None)

            self.emit(OpCode.STORE_VAR, node.var)

            self.loop_stack.append({
                "start": loop_start,
                "breaks": [],
                "continues": []
            })

            for stmt in node.body:
                self.compile(stmt)

            self.emit(OpCode.JUMP, loop_start)

            loop = self.loop_stack.pop()
            loop_end = len(self.code)

            self.patch(exit_jump, loop_end)

            for br in loop["breaks"]:
                self.patch(br, loop_end)

            for ct in loop["continues"]:
                self.patch(ct, loop_start)

            self.emit(OpCode.ITER_END)

        # =========================
        # Range expression
        # =========================

        elif isinstance(node, RangeExpr):
            self.compile(node.start)
            self.compile(node.end)

            if node.step:
                self.compile(node.step)
            else:
                self.emit(OpCode.PUSH_CONST, 1)

            self.emit(OpCode.BUILD_RANGE)

        # =========================
        # Functions
        # =========================

        elif isinstance(node, FunctionDef):
            skip_jump = self.emit(OpCode.JUMP, None)

            entry = len(self.code)
            self.functions[node.name] = {
                "entry": entry,
                "params": node.params
            }

            for stmt in node.body:
                self.compile(stmt)

            self.emit(OpCode.PUSH_CONST, None)
            self.emit(OpCode.RETURN)

            self.patch(skip_jump, len(self.code))

        elif isinstance(node, CallExpr):
            for arg in node.args:
                self.compile(arg)
            self.emit(OpCode.CALL, self.functions[node.name])

        elif isinstance(node, ReturnStmt):
            if node.value:
                self.compile(node.value)
            else:
                self.emit(OpCode.PUSH_CONST, None)
            self.emit(OpCode.RETURN)

        # =========================
        # Loop control
        # =========================

        elif isinstance(node, BreakStmt):
            if not self.loop_stack:
                raise Exception("break outside loop")

            jump = self.emit(OpCode.JUMP, None)
            self.loop_stack[-1]["breaks"].append(jump)

        elif isinstance(node, ContinueStmt):
            if not self.loop_stack:
                raise Exception("continue outside loop")

            jump = self.emit(OpCode.JUMP, None)
            self.loop_stack[-1]["continues"].append(jump)

        # =========================
        # Arrays & indexing
        # =========================

        elif isinstance(node, ArrayLiteral):
            for elem in node.elements:
                self.compile(elem)
            self.emit(OpCode.BUILD_ARRAY, len(node.elements))

        elif isinstance(node, IndexExpr):
            self.compile(node.array)
            self.compile(node.index)
            self.emit(OpCode.INDEX_GET)

        elif isinstance(node, IndexAssign):
            self.compile(node.array)
            self.compile(node.index)
            self.compile(node.value)
            self.emit(OpCode.INDEX_SET)

        # =========================
        # Fallback
        # =========================

        else:
            raise Exception(f"Compiler missing node: {type(node)}")

    # ---------------------------------------------------------
    # Operator mapping
    # ---------------------------------------------------------

    def map_binary(self, op):
        """
        Convert parser TokenType operators into VM opcodes.
        """
        return {
            TokenType.PLUS: OpCode.ADD,
            TokenType.MINUS: OpCode.SUB,
            TokenType.STAR: OpCode.MUL,
            TokenType.SLASH: OpCode.DIV,

            TokenType.GT: OpCode.GT,
            TokenType.GTE: OpCode.GTE,
            TokenType.LT: OpCode.LT,
            TokenType.LTE: OpCode.LTE,
            TokenType.EQEQ: OpCode.EQ,
            TokenType.NOTEQ: OpCode.NEQ,

            TokenType.AND: OpCode.AND,
            TokenType.ANDAND: OpCode.AND,
            TokenType.OR: OpCode.OR,
            TokenType.OROR: OpCode.OR,
        }[op]