from typing import TypeVar, Sequence

T = TypeVar("T")

def get_last(items: Sequence[T]) -> T:
    return items[-1]

last_item = get_last(["hellow", "world"])
print(last_item, last_item[-1])
