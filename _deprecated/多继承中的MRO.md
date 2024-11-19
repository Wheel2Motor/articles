多继承中的MRO
================================================================================

__测试版本__：Python3.10.8

--------------------------------------------------------------------------------

### 方法解析顺序Method-Resolution-Order

Python中可以使用 `super().method()` 来调用父类的方法。

方法解析顺序在单继承中没有什么好关注的，一旦到了多继承，就会影响到获取的方法属于哪个父类。

Python3中采用了 __深度优先，从左到右，重复剔除__ 的原则，方法解析到第一个截止。

* __普通多继承__

  ```python
  class A:
      def say(self):
          print("I'm A")

  class B:
      def say(self):
          print("I'm B")

  class C(A, B):
      def say(self):
          super().say()

  c = C()
  c.say() # I'm A
  ```

* __菱形继承__

  ```python
  class A:
      def say(self):
          print("I'm A")

  class B(A):
      def say(self):
          print("I'm B")

  class C(A):
      def say(self):
          print("I'm,C")

  class D(B, C):
      def say(self):
          print("I'm,D")

  d = D()
  d.say() # I'm B
  ```

通过类的\_\_mro\_\_属性查看解析顺序
================================================================================

```python
class A:...
class B(A):...
class C(A):...
class D(B, C):...
print(D.__mro__) # D C B A object
```

调用父类方法
================================================================================

调用父类方法可以使用 `super().method()` 来根据MRO获取第一个父类方法。

也可以使用 `ParentClass.method(self)` 来指定调用哪个父类的方法。

```python
class A:
    def say(self):
        print("I'm A")

class B(A):
    def say(self):
        print("I'm B")

class C(A):
    def say(self):
        print("I'm,C")

class D(B, C):
    def say(self):
        super().say()     # I'm B
        B.say(self)       # I'm B
        C.say(self)       # I'm C

d = D()
d.say()
```
