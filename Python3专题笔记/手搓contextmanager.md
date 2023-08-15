手搓contextmanager
================================================================================

__测试版本__：Python3.10.8

--------------------------------------------------------------------------------

标准库的contextmanager事实上是对生成器函数以 `yield` 为界两个阶段的调用，生成器会被 `next` 两次。

第一阶段就是yield之前，对应 `__enter__` 方法，可以用 `yield` 返回一个值提供给 `with` 语句的 `as` 作为结果。

第二阶段执行结束返回，对应 `__exit__` 方法，生成器成功返回后会引发 `StopIteration` ，忽略即可。

第一阶段无论是否引发异常，都必须能够确保第二阶段能够进入 `try` 块的 `finally` 语句。

```python
import types

def contextmanager(func):
    def __init__(self, *args):
        self.iter = func(*args)
    def __enter__(self):
        return next(self.iter)
    def __exit__(self, exc_typ, exc_val, tb):
        try:
            next(self.iter)
        except StopIteration:
            pass
    meta = {
        "__init__": __init__,
        "__enter__": __enter__,
        "__exit__": __exit__,
        }
    cls = types.new_class("ctx", (), {}, lambda ns: ns.update(meta))
    return cls

if __name__ == "__main__":

    @contextmanager
    def test(path):
        try:
            f = open(path, "w")
            yield f
        finally:
            f.close()

    with test("test.txt") as f:
        f.write("Hello World")
```
