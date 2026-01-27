from compiler.lexer import Lexer
from compiler.parser import Parser
# from interpreter import Interpreter
import sys
from compiler.ByteCode.compiler import Compiler
from compiler.ByteCode.vm import VM

def run(source: str):
    tokens = Lexer(source).tokenize()
    # ast = Parser(tokens).parse()
    # Interpreter().eval(ast)

    ast = Parser(tokens).parse()

    compiler = Compiler()
    compiler.compile(ast)

    vm = VM(compiler.code, compiler.functions)
    vm.run()

def run_file(path: str):
    with open(path, "r") as f:
        source = f.read()
    run(source)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        run("""
        let x = 10
        log x
        """)