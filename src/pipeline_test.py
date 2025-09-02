from abc import abstractmethod, ABC
from typing import List, TypeVar
from functools import reduce

T = TypeVar('T')
""" 
    | 符号在Python中原本是按位或（bitwise OR）操作符，但通过重载，我们可以赋予它全新的、符合我们设计逻辑的含义
    核心魔法：__or__ 和 __ror__ 魔术方法
    
    __or__(self, other):
    当您的对象出现在 | 左侧时，这个方法会被调用。
    self 指的是管道符左侧的对象实例。
    other 指的是管道符右侧的对象实例。
    这个方法必须返回一个值，通常是代表了两者“链接”之后结果的新对象。
    
    如a | b 会调用a.__or__(b)
    ------------------------------------------------------
    
    __ror__(self, other):
    ror 代表 "reflected OR"。当您的对象出现在 | 右侧，而左侧的对象不支持与您的对象进行 | 操作时，这个方法会被调用。
    self 指的是管道符右侧的对象实例。
    other 指的是管道符左侧的对象实例。
    实现这个方法能让您的管道操作更具灵活性。
    
    __ror__ 的作用与调用时机
    __ror__ 的核心作用是定义当您的自定义对象出现在 | 操作符 右侧 时的行为，特别是当左侧的对象不知道如何处理您的对象时。
    当Python执行 x | y 这个表达式时，它会遵循以下步骤：
    首先，尝试调用左侧对象 x 的 __or__ 方法，即 x.__or__(y)。
    如果 x 没有实现 __or__ 方法，或者 x.__or__(y) 返回了一个特殊值 NotImplemented，那么Python不会立即报错。
    相反，它会“反过来”尝试调用右侧对象 y 的 __ror__ 方法，即 y.__ror__(x)。
    如果 y 实现了 __ror__ 并返回一个有效结果，那么操作成功。
    如果 __ror__ 也没有实现或返回 NotImplemented，此时Python才会抛出 TypeError。
    一句话比喻：__ror__就像是在说：“如果左边的家伙不知道怎么跟我‘管道’连接，那就由我（右边的家伙）来主动处理吧！”

"""
class Pipable(ABC):
    """管道操作基类"""
    def __or__(self, other):
        return Pipeline([self, other])

    """ 左边参数不支持pipable时会调用右边参数的ror """
    def __ror__(self, other):
        self.target = other
        return Pipeline([self])

    @abstractmethod
    def run(self, data: T) -> T:
        raise NotImplementedError

class Pipeline:
    """管道执行类"""

    def __init__(self, items: List[Pipable]):
        self.items = items

    def __or__(self, other):
        return Pipeline(self.items + [other])

    def run(self, data):
        result = data
        for item in self.items:
            result = item.run(result)
        return result

class UppercasePipeline(Pipable):
    def run(self, data: str) -> str:
        return data.upper()

class PrefixPipeline(Pipable):
    def run(self, data: str) -> str:
        return f"Prefix {data}"

class SuffixPipeline(Pipable):
    def run(self, data: str) -> str:
        return f"{data} Suffix"

uppercase = UppercasePipeline()
prefix = PrefixPipeline()
suffix = SuffixPipeline()

uppercase_prefix = uppercase | prefix
print(uppercase_prefix)
print(uppercase_prefix.run("hello world"))

uppercase_prefix_suffix_pipeline = uppercase_prefix | suffix
print(uppercase_prefix_suffix_pipeline)
print(uppercase_prefix_suffix_pipeline.run("hello world"))

class Pipeline2:
    """
    一个可链接、可执行的处理管道。
    """
    def __init__(self, *funcs):
        # 存储管道中的所有处理函数
        self.funcs = funcs

    def __call__(self, data):
        """让管道实例可以像函数一样被调用，执行处理流程。"""
        # 使用 reduce 依次将函数应用到数据上
        return reduce(lambda val, func: func(val), self.funcs, data)

    def __or__(self, other):
        """
        定义 `pipeline | other_pipeline` 的行为。
        用于将两个管道合并成一个更长的管道。
        """
        if isinstance(other, Pipeline2):
            # 返回一个新的Pipeline实例，包含双方的所有函数
            return Pipeline2(*(self.funcs + other.funcs))
        return NotImplemented

    def __ror__(self, other):
        """
        定义 `data | pipeline` 的行为。
        这是让普通数据流入管道的入口。
        """
        # 左侧的 'other' 就是我们的输入数据，直接调用自己来处理它
        print(f"--- __ror__ 被调用: 左侧数据流入管道 ---")
        return self(other)

# --- 定义一些简单的处理函数 ---
def to_uppercase(data: dict) -> dict:
    print("  - 执行: to_uppercase")
    data['text'] = data['text'].upper()
    return data

def add_prefix(prefix: str):
    def inner(data: dict) -> dict:
        print(f"  - 执行: add_prefix with '{prefix}'")
        data['text'] = f"{prefix}{data['text']}"
        return data
    return inner

def extract_text(data: dict) -> str:
    print("  - 执行: extract_text")
    return data['text']


# --- 创建管道实例 ---
# 第一个管道，只包含一个步骤
format_pipeline = Pipeline2(to_uppercase)

# 第二个管道，包含两个步骤
add_prefix_pipeline = Pipeline2(add_prefix("INFO: "), extract_text)


# --- 演示 __ror__ ---
print("--- 演示 __ror__ (数据 | 管道) ---")
input_data = {'text': 'hello from Xi an'}
# 因为 input_data (dict) 没有 __or__ 方法，所以会调用 format_pipeline.__ror__(input_data)
result1 = input_data | format_pipeline
print(f"结果1: {result1}\n")


# --- 演示 __or__ ---
print("--- 演示 __or__ (管道 | 管道) ---")
# format_pipeline.__or__(add_prefix_pipeline) 被调用
full_pipeline = format_pipeline | add_prefix_pipeline
print(f"合并后的管道包含 {len(full_pipeline.funcs)} 个步骤。\n")


# --- 演示完整的链式调用 ---
print("--- 演示完整调用链 (数据 | 管道 | 管道) ---")
# 表达式会从左到右计算:
# 1. `input_data | format_pipeline` 先执行 (__ror__), 得到一个处理后的字典
# 2. `{'text': 'HELLO FROM XI AN'} | add_prefix_pipeline` 再执行 (__ror__), 得到最终结果
final_result = input_data | format_pipeline | add_prefix_pipeline
print(f"最终结果: {final_result}")
