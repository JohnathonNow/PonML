import ast

scope = []

def enter_scope():
    global scope
    scope += [set()]

def exit_scope():
    global scope
    scope.pop()

def check_reassignment(elements):
    if len(elements) > 1:
        return False
    if isinstance(elements[0], ast.Name):
        name = elements[0].id
        ret = False
        for ctx in scope:
            if name in ctx:
                ret = True
        scope[-1].add(name)
        return ret
    return True

def debug(element):
    print(element, dir(element))

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
    elif isinstance(element, ast.Import):
        path = element.names[0].name.split(".")
        name = element.names[0].asname or path[-1]
        path = "/".join(path) + ".mini"
        emit(f'import: {name}("{path}")')
    elif isinstance(element, ast.Add):
        emit(" + ")
    elif isinstance(element, ast.Name):
        emit(element.id)
    elif isinstance(element, ast.Constant):
        emit(repr(element.value))
    elif isinstance(element, ast.Return):
        emit("ret ")
        process(element.value)
    elif isinstance(element, ast.BinOp):
        emit("(")
        process(element.left)
        process(element.op)
        process(element.right)
        emit(")")
    elif isinstance(element, ast.Expr):
        process(element.value)
    elif isinstance(element, ast.Assign):
        if not check_reassignment(element.targets):
            emit("var ")
        for i, n in enumerate(element.targets):
            if i > 0:
                emit(", ")
            process(n)
        emit(" = ")
        process(element.value)
    elif isinstance(element, ast.Call):
        emit("(")
        process(element.func)
        emit("(")
        process_body(element.args, False)
        emit("))")
    elif isinstance(element, ast.FunctionDef):
        name = element.name
        args = ", ".join([x.arg for x in element.args.args])
        emit(f'fun {name}({args}) do\n')
        process_body(element.body)
        emit(f'end\n')

def process_body(body, newlines=True):
    enter_scope()
    for element in body:
        process(element)
        if newlines:
            emit("\n")
    exit_scope()

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
    return i + 2

def bob2():
    x = 5
    x = 6

bob(20)
    """)
    process_body(x.body)
