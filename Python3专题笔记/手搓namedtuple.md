手搓namedtuple
================================================================================

__测试版本__：Python3.10.8

--------------------------------------------------------------------------------

namedtuple本质上也就是动态生成的类型，为动态生成的类型的 `__init__` 函数指定与字段数量一样的参数即可实现namedtuple。

```python
import types

def namedtuple(name, attrs):
    syms = attrs.split()
    def __init__(self, *args):
        assert len(args) == len(syms)
        for s, a in zip(syms, args):
            setattr(self, s, a)
    d = {"__init__": __init__}
    return types.new_class(name, (), {}, lambda ns: ns.update(d))

NT = namedtuple("Man", "name age")

foo = NT("Foo", 23)
print(foo.name, foo.age)

bar = NT("Bar", 24)
print(bar.name, bar.age)
```
