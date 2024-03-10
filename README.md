# PonML
A Python to Minilang transpiler

Meant as an April Fools joke, takes Python and turns it into an equivalent [minilang](https://github.com/wrapl/minilang) script.

Early work in progress.

### Functionality  

Currently supports:  
- Variables
- For loops
- Many operators
- Functions
- Function calls
- Strings, ints, and floats
- Imports

Planned to support:  
- More operators (booleans, comparisons)
- Lists and maps
- fStrings
- try.. except...
- Conditionals
- While loops

No support planned:  
- Classes
- Methods

### Examples

#### Imports
```python
import x
import y.x
from y import x
from .y import x
from ..y import x
```
becomes
```minilang
fun range(i, j, k) do if k then (i .. j by k) else (i .. j) end
import: x("x.mini")
import: x("y/x.mini")
import: x("y/x.mini")
import: x("./y/x.mini")
import: x("../y/x.mini")
```

Notice that it inserts a range function - this is for
compatibility with python, as range is just a function.
It could dynamically determine whether to
include any compatibility functions, but right now it does not.

#### Functions
```python
def test(a, b, c):
    return a + b + c

test(1, 2, 3)
test('a', 'b', 'c')

```

becomes

```minilang
fun range(i, j, k) do if k then (i .. j by k) else (i .. j) end
fun test(a, b, c) do
ret ((a + b) + c)
end
(test(1, 2, 3))
(test('a', 'b', 'c'))
```

Notice that all expressions are wrapped with parens. This is to ensure python's
order of operations is preserved.

#### More Stuff
```python
x = 10
for i in range(1, 10):
    print(i * x)
x = 20
print(x ** 2)
```

becomes

```minilang
fun range(i, j, k) do if k then (i .. j by k) else (i .. j) end
var x = 10
for i in (range(1, 10)) do
(print((i * x)))
end
x = 20
(print((x ^ 2)))
```

### References  
[Python AST](https://docs.python.org/3/library/ast.html)  
[Minilang Docs](https://minilang.readthedocs.io/en/latest/)
