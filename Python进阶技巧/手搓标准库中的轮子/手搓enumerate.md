手搓enumerate
================================================================================

我们手搓一个跟标准库差不多的enumerate。

同时，我们还可以手搓一个可以对字典的键值对同时迭代的enumerate。

```python
#  测试版本：Python3.10.8

def Enumerate(seq, idxstart=0):
    idx = idxstart
    for item in seq:
        yield idx, item
        idx += 1

def EnumerateDict(seq, idxstart=0):
    idx = idxstart
    for k, v in seq.items():
        yield idx, k, v
        idx += 1

if __name__ == "__main__":
    s = ["zhansan", "lisi", "wangwu"]
    for idx, name in Enumerate(s):
        print(idx, name)

    d = {"zhansan": 29, "lisi": 27, "wangwu": 25}
    for idx, name, age in EnumerateDict(d):
        print(idx, name, age)
```
