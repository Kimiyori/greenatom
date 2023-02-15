# Вопрос: Сколько HTML тагов в коде главной страницы сайта greenatom.ru? Сколько из них содержит атрибуты? Напиши скрипт на Python, который выводит ответы на вопросы ниже?

from bs4 import BeautifulSoup
import requests

URL = "https://greenatom.ru"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
    "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept_Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
    "Referer": "https://google.com",
    "DNT": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.75",
}


def get_page(link: str) -> BeautifulSoup:
    response = requests.get(link, headers=HEADERS)
    return BeautifulSoup(response.text, "html.parser")


def count_tags(
    page: BeautifulSoup,
) -> int:
    return len(page.findAll())


def count_tags_with_attrs(
    page: BeautifulSoup,
) -> int:
    return len([tag for tag in page.findAll() if len(tag.attrs)])


if __name__ == "__main__":
    page = get_page(URL)
    tags_all = count_tags(page)
    tags_with_attrs = count_tags_with_attrs(page)
    print(tags_all, tags_with_attrs)
