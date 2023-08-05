# Fitipy

This small python module used for automatic synchronization of a Python data type
with a file. Typically, this is useful in places where a small amount of data is
stored.

## Installation

```bash
pip3 install fitipy
```

## Example

```python
from fitipy import FSet

users = FSet('data', 'users.txt')
users.add('sue')
```

Compared to raw code that does a similar function:

```python
from os import makedirs
from os.path import isfile, join

if isfile(join('data', 'users.txt')):
    with open(join('data', 'users.txt')) as f:
        users = set(f.read().split('\n'))
else:
    users = set()
users.add('sue')
makedirs('data', exist_ok=True)
with open(join('data', 'users.txt'), 'w') as f:
    f.write('\n'.join(users))
```
