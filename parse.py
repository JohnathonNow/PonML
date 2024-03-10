import ast
debugging = False

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
    if debugging:
        return
    print(text, end='')

def process(element):
    if debugging:
        debug(element)

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
    elif isinstance(element, ast.Mult):
        emit(" * ")
    elif isinstance(element, ast.Div):
        emit(" / ")
    elif isinstance(element, ast.Mod):
        emit(" % ")
    elif isinstance(element, ast.Pow):
        emit(" ^ ")
    elif isinstance(element, ast.Add):
        emit(" + ")
    elif isinstance(element, ast.Name):
        emit(element.id)
    elif isinstance(element, ast.Constant):
        emit(repr(element.value))
    elif isinstance(element, ast.For):
        emit("for ")
        process(element.target)
        emit(" in ")
        process(element.iter)
        emit(" do\n")
        process_body(element.body)
        emit("end")
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
        for i, n in enumerate(element.args):
            if i > 0:
                emit(", ")
            process(n)
        emit("))")
    elif isinstance(element, ast.FunctionDef):
        name = element.name
        args = ", ".join([x.arg for x in element.args.args])
        emit(f'fun {name}({args}) do\n')
        process_body(element.body)
        emit(f'end')

def process_body(body, newlines=True):
    enter_scope()
    for element in body:
        process(element)
        if newlines:
            emit("\n")
    exit_scope()

def process_all(body):
    emit("fun range(i, j, k) do if k then (i .. j by k) else (i .. j) end\n")

    process_body(body)
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(
        prog='PonML',
        description='Transpiles a subset of Python into minilang')
    p.add_argument('-f', '--file', required=False)
    p.add_argument('-d', '--debug', default=False, const=True, nargs='?')
    args = p.parse_args()
    with open(args.file or "test.py", "r") as f:
        x = ast.parse(f.read())
    debugging = args.debug
    process_all(x.body)
