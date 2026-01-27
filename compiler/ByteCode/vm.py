from compiler.ByteCode.opcodes import OpCode

class VM:
    def __init__(self, code, functions):
        self.code = code
        self.stack = []
        self.functions = functions
        self.env = {}
        self.call_stack = []
        self.ip = 0
        # self.iter_stack = []

    def run(self):
        while True:
            op, arg = self.code[self.ip]
            self.ip += 1


            # Instructions
            if op == OpCode.PUSH_CONST:
                self.stack.append(arg)

            elif op == OpCode.LOAD_VAR:
                self.stack.append(self.env.get(arg, 0))

            elif op == OpCode.STORE_VAR:
                if not self.stack:
                    raise Exception(f"STORE_VAR {arg} with empty stack")
                self.env[arg] = self.stack.pop()

            # Iterators
            elif op == OpCode.ITER_INIT:
                iterable = self.stack.pop()

                if isinstance(iterable, (list, str, range)):
                    self.stack.append(iter(iterable))

                elif isinstance(iterable, int):
                    # iterate over digits
                    digits = str(abs(iterable))
                    self.stack.append(iter(digits))

                else:
                    raise Exception("Object is not iterable")

            elif op == OpCode.ITER_NEXT:
                it = self.stack.pop()

                try:
                    value = next(it)
                    self.stack.append(it)        # keep iterator
                    self.stack.append(value)     # current value
                    self.stack.append(True)      # continue loop
                except StopIteration:
                    self.stack.append(False)     # stop loop

            elif op == OpCode.ITER_END:
                pass

            # Arithmetic and Comparison
            elif op == OpCode.ADD:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)

            elif op == OpCode.SUB:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)

            elif op == OpCode.MUL:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)

            elif op == OpCode.DIV:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a / b)

            elif op == OpCode.NEG:
                self.stack.append(-self.stack.pop())

            elif op == OpCode.EQ:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a == b)

            elif op == OpCode.NEQ:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a != b)

            elif op == OpCode.GT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a > b)

            elif op == OpCode.GTE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a >= b)

            elif op == OpCode.LT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a < b)

            elif op == OpCode.LTE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a <= b)

            elif op == OpCode.NOT:
                self.stack.append(not self.stack.pop())

            # Boolean / Logic
            elif op == OpCode.JUMP:
                self.ip = arg

            elif op == OpCode.JUMP_IF_FALSE:
                if not self.stack.pop():
                    self.ip = arg

            elif op == OpCode.CALL:
                func = arg  # dict: { "entry", "params" }

                # Save return address and environment
                self.call_stack.append((self.ip, self.env))

                # Build new environment
                new_env = {}

                argc = len(func["params"])
                args = [self.stack.pop() for _ in range(argc)][::-1]

                for name, value in zip(func["params"], args):
                    new_env[name] = value

                self.env = new_env
                self.ip = func["entry"]

            elif op == OpCode.RETURN:
                ret = self.stack.pop() if self.stack else None

                if not self.call_stack:
                    # Top-level return = program end
                    return ret

                self.ip, self.env = self.call_stack.pop()
                self.stack.append(ret)

            elif op == OpCode.PRINT:
                print(self.stack.pop())

            elif op == OpCode.POP:
                self.stack.pop()

            elif op == OpCode.BUILD_RANGE:
                step = self.stack.pop()
                end = self.stack.pop()
                start = self.stack.pop()
                self.stack.append(range(start, end, step))

            # Arrays
            elif op == OpCode.BUILD_ARRAY:
                count = arg
                elements = [self.stack.pop() for _ in range(count)][::-1]
                self.stack.append(elements)

            elif op == OpCode.INDEX_GET:
                idx = self.stack.pop()
                value = self.stack.pop()

                if not isinstance(idx, int):
                    raise Exception("Index must be integer")

                if isinstance(value, list):
                    self.stack.append(value[idx])

                elif isinstance(value, str):
                    self.stack.append(value[idx])

                elif isinstance(value, int):
                    digits = str(abs(value))
                    self.stack.append(int(digits[idx]))

                else:
                    raise Exception("Indexing unsupported type")

            elif op == OpCode.INDEX_SET:
                val = self.stack.pop()
                idx = self.stack.pop()
                target = self.stack.pop()

                if not isinstance(idx, int):
                    raise Exception("Index must be integer")

                if isinstance(target, list):
                    target[idx] = val
                    self.stack.append(val)

                else:
                    raise Exception("Assignment only supported for arrays")

            elif op == OpCode.HALT:
                break