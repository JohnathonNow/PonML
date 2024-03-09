import ast

x = ast.parse("""
import bob.x
from x import y
import z
def bob(i):
    print('hi')
""")

for element in x.body:
    #print(element)
    if isinstance(element, ast.Import):
        path = element.names[0].name.split(".")
        name = element.names[0].asname or path[-1]
        path = "/".join(path) + ".mini"
        print(f'import: {name}("{path}")')
    if isinstance(element, ast.FunctionDef):
        name = element.name
        args = ", ".join([x.arg for x in element.args.args])
        print(f'fun {name}({args}) do')
        print(f'end')
