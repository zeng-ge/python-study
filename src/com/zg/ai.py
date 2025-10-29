import asyncio

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import  HumanMessage
from langchain.tools import tool

load_dotenv()
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
#
# class add(TypedDict):
#     """Add two integers."""
#
#     # Annotations must have the type and can optionally include a default value and description (in that order).
#     a: Annotated[int, ..., "First integer"]
#     b: Annotated[int, ..., "Second integer"]
#
#
# class multiply(TypedDict):
#     """Multiply two integers."""
#
#     a: Annotated[int, ..., "First integer"]
#     b: Annotated[int, ..., "Second integer"]

@tool
def add(a: int, b: int) -> int:
    """Add a to b"""
    print("add", a, b)
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a to b"""
    print("multiply", a, b)
    return a * b

tools = [add, multiply]

llmWithTools = llm.bind_tools(tools)
query = "What is 3 * 12? Also, what is 11 + 49 ?"
messages = [HumanMessage(query)]
ai_msg = llmWithTools.invoke(messages)
print(ai_msg.tool_calls)
print(ai_msg)
messages.append(ai_msg)
for tool_call in ai_msg.tool_calls:
    selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)
print(messages)
result = llmWithTools.invoke(messages)
print("--------", result)
chunks = []

async def execute():
    async for chunk in llmWithTools.astream(messages):
        chunks.append(chunk)
        print(chunk.content, end="|", flush=True)
asyncio.run(execute())



