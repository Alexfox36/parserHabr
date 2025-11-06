import logging
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint

main_page = "https://habr.com/ru/articles/top/daily/"

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def get_url_html(url: str) -> str:
    res = requests.get(
        url,
        headers={
            "User-Agent": UserAgent().google,
        })
    return res.text


def get_soup(html_text: str) -> BeautifulSoup:
    return BeautifulSoup(html_text, "lxml")


@dataclass
class ArticleData:
    title: str
    views: str
    url: str
    text: str


def get_all_posts(soup: BeautifulSoup) -> list[ArticleData]:
    posts_data = []
    all_articles_soup = soup.find_all("article", class_="tm-articles-list__item")
    for article_soup in all_articles_soup:
        articles_title = article_soup.find("a", class_="tm-title__link").find("span").text
        articles_views = article_soup.find("span", class_="tm-icon-counter__value").text
        article_url: str = article_soup.find('a', class_='tm-title__link')['href']
        article_url = 'https://habr.com' + article_url
        article_text: str = get_article_text(article_url)
        posts_data.append(ArticleData(
            title=articles_title,
            views=articles_views,
            url=article_url,
            text=article_text,
        ))
    return posts_data



def get_article_text(url: str) -> str:
    try:
        article_html = get_url_html(url)
        soup = get_soup(article_html)
        article_text = soup.find('article', class_='tm-article-presenter__content')
        if article_text:
            logger.info(f"получение данных")
            return article_text.get_text(strip=True)
        return "Текст статьи не найден"
    except Exception as e:
        return f"Ошибка при получении текста: {str(e)}"


def main():
    html = get_url_html(main_page)
    soup = get_soup(html)
    posts = get_all_posts(soup)
    pprint(posts)
    logger.info(f"таска завершена")


if __name__ == "__main__":
    main()
