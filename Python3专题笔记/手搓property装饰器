手搓property装饰器
================================================================================

__测试版本__：Python3.10.8

--------------------------------------------------------------------------------

Python的 `property` 装饰器事实上是生成一个描述符(descriptor)协议的对象，将其放到类属性中，对实例的访问会被自动代理到描述符对象上。

```python
class Property:

    def __init__(self, fget, fset=None, fdel=None):
        self.name = fget.__name__
        self.getter(fget)
        self.setter(fset)
        self.deleter(fdel)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        if self.fget:
            return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError(f"can't set attribute '{self.name}'")
        self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError(f"can't delete attribute '{self.name}'")
        self.fdel(instance)

    def getter(self, func):
        self.fget = func
        return self

    def setter(self, func):
        self.fset = func
        return self

    def deleter(self, func):
        self.fdel = func
        return self


if __name__ == "__main__":

    class Example:

        def __init__(self, name, idn):
            self.name = name
            self.identity = idn

        @Property
        def name(self):
            return self.__name

        @name.setter
        def name(self, value):
            """
            名称前面必须有Prefixed_
            """
            if not value.startswith("Prefixed_"):
                value = "Prefixed_" + value
            self.__name = value

        @name.deleter
        def name(self):
            """
            名称恢复默认
            """
            self.__name = "Prefixed_Default"

        def __identity_getter(self):
            return self.__identity

        def __identity_setter(self, value):
            """
            只接受偶数
            """
            if value % 2 != 0:
                value += 1
            self.__identity = value

        def __identity_deleter(self):
            """
            归
            """
            self.__identity = 0

        identity = Property(
            __identity_getter,
            __identity_setter,
            __identity_deleter,
            )


    e = Example("Example", 1)

    print(e.name)     # Prefixed_Example
    print(e.identity) # 2

    del e.name
    del e.identity

    print(e.name)     # Prefixed_Default
    print(e.identity) # 0
```
