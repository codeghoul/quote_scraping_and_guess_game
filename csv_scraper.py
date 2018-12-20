import requests
from bs4 import BeautifulSoup
from csv import DictWriter
from random import choice
from time import sleep

BASE_URL = "http://quotes.toscrape.com"


def scrape_quote_list():
    quote_list = []
    url = "/page/1"
    while url:
        request = requests.get(f"{BASE_URL}{url}")
        request.encoding = 'utf-8'
        soup = BeautifulSoup(request.text, 'html.parser')
        quotes = soup.select('.quote')
        for quote in quotes:
            quote_list.append({
                "text": quote.find(class_='text').get_text(),
                "author": quote.find(class_='author').get_text(),
                "bio-link": quote.find('a')['href']
            })
        next_btn = soup.find(class_='next')
        url = next_btn.find('a')['href'] if next_btn else None
        sleep(1)
    return quote_list


def write_quotes(quotes):
    with open("quotes.csv", "w", encoding='utf-8') as file:
        headers = ["text", "author", "bio-link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quote_list:
            csv_writer.writerow(quote)


if __name__ == '__main__':
    quotes = scrape_quote_list()
    write_quotes(quotes)
