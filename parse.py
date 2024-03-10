import ast

def emit(text):
    print(text, end='')

def process(element):
    if isinstance(element, ast.ImportFrom):
        module = element.module
        if module:
            module += '.'
        else:
            module = ''
        path = (module + element.names[0].name).split(".")
        if element.level > 0:
            path = ['.' * element.level] + path
        name = element.names[0].asname or path[-1]
        path = "/".join(path) + ".mini"
        emit(f'import: {name}("{path}")')
    if isinstance(element, ast.Add):
        emit(" + ")
    if isinstance(element, ast.Import):
        path = element.names[0].name.split(".")
        name = element.names[0].asname or path[-1]
        path = "/".join(path) + ".mini"
        emit(f'import: {name}("{path}")')
    if isinstance(element, ast.Name):
        emit(element.id)
    if isinstance(element, ast.Constant):
        emit(repr(element.value))
    if isinstance(element, ast.Return):
        emit("ret ")
        process(element.value)
    if isinstance(element, ast.BinOp):
        emit("(")
        process(element.left)
        process(element.op)
        process(element.right)
        emit(")")
    if isinstance(element, ast.Expr):
        process(element.value)
    if isinstance(element, ast.Call):
        emit("(")
        process(element.func)
        emit("(")
        process_body(element.args, False)
        emit("))")
    if isinstance(element, ast.FunctionDef):
        name = element.name
        args = ", ".join([x.arg for x in element.args.args])
        emit(f'fun {name}({args}) do\n')
        process_body(element.body)
        emit(f'end\n')

def process_body(body, newlines=True):
    for element in body:
        process(element)
        if newlines:
            emit("\n")

if __name__ == '__main__':
    x = ast.parse("""
import bob.x
from z import y
from .z import y
from ..z import y
import z
def bob(i):
    print('hi')
    print(1 + 2)
    return 5
    """)
    process_body(x.body)
