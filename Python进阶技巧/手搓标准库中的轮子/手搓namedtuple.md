手搓namedtuple
================================================================================

namedtuple本质上也就是动态生成的类型，为动态生成的类型的 `__init__` 函数指定与字段数量一样的参数即可实现namedtuple。

一种方式是使用函数动态生成类型。

```python
# 测试版本：Python3.10.8

import sys
import types

def namedtuple(name, attrs):
    syms = list(filter(lambda _: _, attrs.split()))
    def __init__(self, *args):
        assert len(args) == len(syms)
        for s, a in zip(syms, args):
            setattr(self, s, a)
    d = {"__init__": __init__}
    t = types.new_class(name, (), {}, lambda ns: ns.update(d))
    t.__module__ = sys._getframe(1).f_globals["__name__"]
    return t

if __name__ == "__main__":
    NT = namedtuple("Man", "name age")
    foo = NT("Foo", 23)
    bar = NT("Bar", 24)
    print(foo.name, foo.age)
    print(bar.name, bar.age)
```

以继承的方式更加优雅。

```python
import operator

class NamedTupleMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n, name in enumerate(cls._fields):
            setattr(cls, name, property(operator.itemgetter(n)))

class NamedTuple(tuple, metaclass=NamedTupleMeta):
    _fields = []
    def __new__(cls, *args):
        if len(args) != len(cls._fields):
            raise ValueError('{} arguments required'.format(len(cls._fields)))
        return super().__new__(cls,args)

if __name__ == "__main__":
    class NT(NamedTuple): _fields = ["x", "y", "z"]
    spam = NT(1, 2, 3)
    print(spam.x, spam.y, spam[2])
```
