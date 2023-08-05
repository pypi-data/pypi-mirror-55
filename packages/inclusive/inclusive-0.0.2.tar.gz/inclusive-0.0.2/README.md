
# inclusive

Provides **range** and **slice** with inclusive right boundary.

Examples for **range**:

```
from inclusive import range

list(range(5)) == [0, 1, 2, 3, 4]
list(range[5]) == [1, 2, 3, 4, 5]

list(range(2, 7)) == [2, 3, 4, 5, 6]
list(range[2, 7]) == [2, 3, 4, 5, 6, 7]

list(range(2, 11, 3)) == [2, 5, 8]
list(range[2, 11, 3]) == [2, 5, 8, 11]
```

Examples for **slice**:

```
from inclusive import slice

list(range(100)[slice(5)]) == [0, 1, 2, 3, 4]
list(range(100)[slice[5]]) == [1, 2, 3, 4, 5]

list(range(100)[slice(2, 7)]) == [2, 3, 4, 5, 6]
list(range(100)[slice[2, 7]]) == [2, 3, 4, 5, 6, 7]

list(range(100)[slice(2, 11, 3)]) == [2, 5, 8]
list(range(100)[slice[2, 11, 3]]) == [2, 5, 8, 11]
```
