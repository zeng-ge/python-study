import asyncio
from datetime import datetime

print(datetime.now())
async def test_coroutine():
    print("start")
    await asyncio.sleep(1)
    print("end")

# 并不会执行函数内容，可以看出start并没有被打印面来
print("before invoke test_coroutine")
coroutineInstance = test_coroutine()
print("after invoke test_coroutine", coroutineInstance, coroutineInstance.__class__)

async def main():
    print("execute main start")
    # await 用于暂停协程的执行，等待另一个协程完成，并获取其结果。await 后面必须跟随一个可等待对象
    # 这里的await会先暂停main这个coroutine的执行，然后等待coroutineInstance的执行完成
    await coroutineInstance # await后 test_coroutine内的代码才开始执行
    print("execute main end")

asyncio.run(main())
