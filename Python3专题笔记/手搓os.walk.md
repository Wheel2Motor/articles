手搓os.walk
================================================================================

__测试版本__：Python3.10.8

--------------------------------------------------------------------------------

利用 `yield from` 语句可以在生成器的迭代过程中迭代另一个生成器。

```python
import os

def walk(root="."):
    prev = os.getcwd()
    os.chdir(root)
    contents = os.listdir()
    dirs = []
    files = []
    for c in contents:
        if os.path.isdir(c):
            dirs.append(c)
        elif os.path.isfile(c):
            files.append(c)
    os.chdir(prev)
    yield root, dirs, files
    for d in dirs:
        path = os.path.join(root, d)
        yield from walk(path)


if __name__ == "__main__":
    for root, dirs, files in walk():
        print("ROOT: ", root)
        for f in files:
            print("\tF - ", f)
        for d in dirs:
            print("\tD - ", d)
```
