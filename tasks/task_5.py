# Напиши Функцию на Python, выполняющую сравнение версий
from itertools import zip_longest


def compare(version1: str, version2: str) -> int:
    def split_ver(version: str):
        return (int(x) for x in version.split("."))

    for v1, v2 in zip_longest(split_ver(version1), split_ver(version2), fillvalue=0):
        if v1 > v2:
            return 1
        if v1 < v2:
            return -1
    return 0


if __name__ == "__main__":
    versions = [("1.10", "1.1"), ("1.1", "1.1"), ("1.1", "1.10")]
    answers = [1, 0, -1]
    for version, answer in zip(versions, answers):
        assert answer == compare(*version)
