
"""
    添加__call__方法后，类的实例还可以当函数执行

    在Python中，只要一个实例的类定义了一个名为 __call__ 的特殊“魔术方法”（dunder method），那么这个实例就成为了可调用对象 (Callable Object)。
    __call__ 方法的作用就是定义当一个类的实例被“调用”时，应该执行什么代码。
"""

class Computer:

    def __call__(self, *args):
        print("Computer called", args)
        return self

computer = Computer()
computer()
print(computer("hello", "world"))
