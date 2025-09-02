def concat(*args):
    """
        1. 在函数定义中 (In a Function Definition) - 打包参数 (Packing)
        当用在函数定义的参数列表中时，它们的作用是收集和打包传入的多余参数。

        *args - 打包位置参数 (Positional Arguments)
        一个星号 * 会将所有未被匹配的位置参数“打包”成一个元组 (tuple)。
    """
    print(type(args), args)
    return args[0] + " " + args[1]

def substitute(**kwargs):
    """
        **kwargs - 打包关键字参数 (Keyword Arguments)
        两个星号 ** 会将所有未被匹配的关键字参数“打包”成一个字典 (dict)。

        作用：让函数可以接收任意数量的关键字参数。

        惯例：我们通常将其命名为 **kwargs (keyword arguments的缩写)。
    """
    print(type(kwargs), kwargs, kwargs.items())
    print(type(list(kwargs)), list(kwargs))

print(concat("hello", "world")) # 未匹配的位置参数都打包进args中，作为一个tuple
print(substitute(name="tod", age=21))

tupleIns = "hello", "world", "welcome"
print(type(tupleIns), tupleIns, len(tupleIns), list(tupleIns))

def unpack(name, age) -> None:
    """
        2. 在函数调用中 (In a Function Call) - 解包参数 (Unpacking)
        当用在函数调用的参数位置时，它们的作用正好相反，是解开和分散一个集合中的元素。

        * - 解包可迭代对象 (Unpacking Iterables)
        一个星号 * 会将一个可迭代对象（如列表 list、元组 tuple、字符串 str）“解包”，将其中的每个元素作为独立的位置参数传入函数。
    """
    print("unpack list, tuple:",name, age)

unpack(*["tod", "21"])
unpack(*("tod", "21"))

def unpack_dict(name, age)->None:
    """
        ** - 解包字典 (Unpacking Dictionaries)
        两个星号 ** 会将一个字典“解包”，将其中的每个键值对作为独立的关键字参数传入函数。字典的键（必须是字符串）对应参数名，值对应参数值。
    """
    print(f"unpackDict name: {name}, age: {age}")
unpack_dict(**{"name": "tod", "age": 22})

# python没有块级作用域，可以产生作用域的：函数、类、模块、推导式或生成器表达式
def scope_test(none: None | str):
    if None:
        var_test = "none"
    else:
        var_test = "bbb"
    print(var_test)
scope_test(None)
scope_test("abc")
