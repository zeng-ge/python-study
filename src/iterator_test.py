books = ["java", "python", "c++"]

booksIter = iter(books)

print(books)
print(booksIter, type(booksIter))
print(next(booksIter), next(booksIter), next(booksIter))


# 看起来for if 这种语法只能用于赋值, 推导式可以为list、dict、set服务， [x for], {x: xx for], {x for}
abc = [item for item in books if item != "java"]
print(type(abc), abc)

# 生成器, ()括号包起来的是生成器
generatorIns = (item for item in books if item != "java")
print(type(generatorIns), generatorIns, next(generatorIns))

class Card:
    def __init__(self, count):
        self.count = count
    def __iter__(self):
        return self
    def __next__(self):
        if self.count > 0:
            current = self.count
            self.count -= 1
            return current
        else:
            raise StopIteration
print(Card(2).__next__())
for card in Card(10):
    print(f"card {card}")
