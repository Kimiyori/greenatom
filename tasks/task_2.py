# Вопрос: Какие ты видишь проблемы в следующем фрагменте кода? Как его следует исправить? Исправь ошибку и перепиши код ниже с использованием типизации.
from typing import Callable


def create_handlers(callback: Callable[[int], any]) -> list[Callable[[int], any]]:
    return [lambda i=i: callback(i) for i in range(5)]


def execute_handlers(handlers: list[Callable[[int], any]]):
    for handler in handlers:
        print(handler())


def test():
    def test_callback(i: int) -> int:
        return i**2

    handlers = create_handlers(test_callback)
    execute_handlers(handlers)


if __name__ == "__main__":
    test()
# Output:
# 0
# 1
# 4
# 9
# 16