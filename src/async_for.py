import asyncio

# 一个异步生成器，模拟一个缓慢的、分批次返回数据的数据源
async def fake_paginated_api_stream(total_pages: int):
    """
    模拟一个分页API，每秒返回一页数据。
    """
    for i in range(1, total_pages + 1):
        print(f"  (API: 正在准备第 {i} 页的数据...)")
        # 模拟网络延迟，这是非阻塞的等待
        await asyncio.sleep(2)
        # 使用 yield “生产”出数据，此时函数会暂停
        yield f"这是第 {i} 页的数据"

# 一个简单的并发任务，用于证明事件循环在 async for 等待时没有被阻塞
async def pinger():
    """每0.4秒打印一个点，证明程序还在“活着”"""
    print("executing pinger")
    while True:
        await asyncio.sleep(0.4)
        print(".", end="", flush=True)

async def main():
    print("程序开始...")

    # 并发运行我们的 pinger 和主逻辑
    pinger_task = asyncio.create_task(pinger())

    # 【核心】使用 async for 遍历异步生成器
    async for page_data in fake_paginated_api_stream(4):
        print(f"\n主程序收到: {page_data}")

    # 主逻辑完成后，取消 pinger 任务
    pinger_task.cancel()
    print("\n程序结束。")

# 运行主协程
asyncio.run(main())
