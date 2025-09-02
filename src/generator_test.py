import asyncio


def fib(max):
    print("fib start")
    prev, current = 0, 1
    while(max > 0):
        max -= 1
        print("before yield")
        # 第一次调用next时会执行到yield语名并返回值，再次调用next时才会执行后面的语句
        # 然后从循环中开始执行直到yield执行并返回时停止
        yield current
        print("after yield")
        prev, current = current, prev + current
print("invoke fib before")
generatorIns = fib(10)
print("invoke fib after")
print(type(generatorIns), generatorIns)

# 在调用next之前，fib函数内的代码并不会执行

print("before invoke next")
value = next(generatorIns)
print("after invoke next", value)

print("before invoke next 2")
value = next(generatorIns)
print("after invoke next 2", value)

# print(next(generatorIns), next(generatorIns), next(generatorIns), next(generatorIns))
