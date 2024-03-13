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
for i in range(1, 10):
    print(i)
    print(i * 5)

z.bar()
"bob".count()

a = [1, 2, 3]
a = {"a": 1, "b": 2, "c": 400}
a = 4
b = f'{a}""\'\''

try:
    pass
except Exception as e:
    pass
except:
    pass
