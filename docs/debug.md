  方法1：使用 print 语句 (最简单)

  这是最直接的调试方法。你可以在你的代码（比如路由函数中）的任何地方添加 print() 语句。输出会直接显示在运行 uvicorn
  命令的终端里。

  示例:
  在你的一个路由函数里，比如 app/api/chat_routes.py，你可以这样做：

   1 @router.post("/chat", response_model=ChatResponse)
   2 async def chat_with_agent(request: ChatRequest, db: Session = Depends(get_db)):
   3     print(f"收到的请求数据: {request.dict()}")  # <--- 在这里添加 print
   4     # ... 你的其余代码
   5     user_message = request.messages[-1].content
   6     deal_id = request.deal_id
   7     print(f"用户消息: '{user_message}', Deal ID: {deal_id}") # <--- 在这里添加 print
   8
   9     # ...

  当你通过 API 发送一个请求到 /chat 时，你会在终端看到这些 print 语句的输出。

   - 优点: 简单、快速，不需要任何额外工具。
   - 缺点: 对于复杂问题，会把代码弄得很乱，而且功能有限。

  方法2：使用内置断点 breakpoint() (推荐)

  从 Python 3.7 开始，你可以使用内置的 breakpoint() 函数来设置一个断点。当代码执行到这里时，Uvicorn
  服务器会暂停，并在你的终端里启动一个 Python 调试器 (pdb)。

  步骤:

   1. 在你想要暂停代码的地方，插入 breakpoint()。
   2. 为了稳定的调试，建议暂时去掉 `--reload` 标志，像这样启动服务器：
   1     uvicorn app.main:app
      因为 --reload 会创建子进程，有时会干扰调试器的输入/输出。
   3. 发送一个会触发该代码的 API 请求。
   4. 你的终端会卡在 breakpoint() 的位置，并显示 (Pdb) 提示符。

  示例:

    1 @router.post("/chat", response_model=ChatResponse)
    2 async def chat_with_agent(request: ChatRequest, db: Session = Depends(get_db)):
    3     # ...
    4     user_message = request.messages[-1].content
    5     deal_id = request.deal_id
    6
    7     breakpoint() # <--- 在这里设置断点
    8
    9     # 在这里，你可以检查变量的值
   10     # ...

  在 `(Pdb)` 调试器中，你可以使用以下命令:
   * n (next): 执行下一行代码。
   * c (continue): 继续执行，直到下一个断点或程序结束。
   * p <variable_name> (print): 打印变量的值 (例如 p user_message)。
   * q (quit): 退出调试器并终止程序。
   * ll (long list): 查看当前函数的完整代码。

  方法3：使用 IDE 的调试器 (功能最强)

  这是最强大和高效的方法，特别是对于复杂的项目。我将以 VS Code 为例，因为它非常流行。

  步骤:

   1. 安装 Python 扩展: 确保你已经在 VS Code 中安装了 Microsoft 的 Python 扩展。

   2. 创建调试配置文件:
       * 点击 VS Code 左侧的 "Run and Debug" 图标 (一个带有播放按钮的虫子)。
       * 点击 "create a launch.json file"。
       * 选择 "Python" -> "Module"。
       * 当提示输入模块时，输入 uvicorn。
       * VS Code 会生成一个 .vscode/launch.json 文件。

   3. 修改 `launch.json` 文件:
      将其内容修改为如下所示，以告诉 VS Code如何启动 Uvicorn：

    1     {
    2         "version": "0.2.0",
    3         "configurations": [
    4             {
    5                 "name": "Python: FastAPI",
    6                 "type": "python",
    7                 "request": "launch",
    8                 "module": "uvicorn",
    9                 "args": [
   10                     "app.main:app",
   11                     "--host",
   12                     "127.0.0.1",
   13                     "--port",
   14                     "8000",
   15                     "--reload"
   16                 ],
   17                 "jinja": true // 如果你使用 Jinja2 模板，这个很有用
   18             }
   19         ]
   20     }

   4. 设置断点并开始调试:
       * 在你的代码文件中，在你想要暂停的行号左边点击，设置一个红点断点。
       * 回到 "Run and Debug" 视图。
       * 确保顶部的下拉菜单选中了 "Python: FastAPI"。
       * 点击绿色的播放按钮 ▶️ 开始调试。

  现在，当你发送一个 API 请求时，VS Code
  会在你的断点处暂停。你可以查看所有变量的值、调用堆栈、单步执行代码等，所有操作都在图形界面中完成，非常直观。

  总结:

   * 快速检查: 用 print()。
   * 在终端里交互式调试: 用 breakpoint() (记得去掉 --reload)。
   * 完整、高效的调试体验: 使用 IDE (如 VS Code) 的调试器。

  方法5 pycharm或intellij配置uvicorn调试
    1. edit configuration
    2. 将script切换成module, module给值uvicorn
    3. 配置启动参数为app.main:app --reload
    4. 配置工作目录，项目根目录
    5. 配置.env文件