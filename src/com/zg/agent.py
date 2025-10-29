from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()
search_tool = TavilySearch()
# search_res = search_tool.invoke("python学习")
# print(search_res)

@tool
def get_word_length(word: str):
    """计算单词的长度"""
    return len(word)

tools = [search_tool, get_word_length]

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature = 0)

# 2. 创建提示：从LangChain Hub拉取一个为Gemini优化的提示模板
# 这个提示专门用于指导Gemini如何使用工具
prompt = hub.pull("hwchase17/openai-functions-agent")
print(prompt.messages)

# 3. 创建Agent：使用为Gemini设计的构造函数
# create_google_genai_tools_agent 会将LLM、工具和提示正确地组合起来
agent = create_tool_calling_agent(llm, tools, prompt)

# 4. 创建Agent执行器
# AgentExecutor 的逻辑是通用的，与具体LLM无关
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({
    "input": "单词'Pydantic'有多长？"
})

for chunk in agent_executor.stream({
    "input": "python coroutine的实现原理"
}):
    print(chunk)



